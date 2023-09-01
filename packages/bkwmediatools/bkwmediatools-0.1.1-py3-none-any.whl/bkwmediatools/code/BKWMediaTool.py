import os
import re
import warnings
import nltk
import numpy as np
from dotenv import load_dotenv
from heapq import nlargest
from nltk.tokenize import sent_tokenize, word_tokenize
from azure.data.tables import TableClient

from eventregistry import *
from bkwmediatools.code.media_retrieval import get_media_news
from bkwmediatools.code.media_filtering import filter_media_articles
from datetime import datetime as dt


class BKWMediaTool:
    def __init__(self, newsapikey):
        # Load environment variables
        abs_directory = os.path.dirname(os.path.abspath(__file__))
        env_file = os.path.join(abs_directory, "../../env.env")
        load_dotenv(env_file)

        # Set global variables
        self.media_intel = os.environ.get("media_intel")
        self.newsapikey = newsapikey
        np.random.seed(2018)

    def sanitize_property_name(self, name):
        invalid_chars = ["/", "\\", "#", "?"]
        for char in invalid_chars:
            name = name.replace(char, "")
        if name[0] in ["/", "_"]:
            name = name[1:]
        return name

    def update_azure_table_from_dataframe(
        self, table_name, df, other_table_names, bims_proj=False
    ):
        """This function updates an Azure Table with DataFrame content. It checks for duplicate URLs in this table as well as two others"""
        # Import required modules

        # Connect to Azure table
        main_table_client = TableClient.from_connection_string(
            self.media_intel, table_name
        )
        other_table_clients = [
            TableClient.from_connection_string(self.media_intel, table_name)
            for table_name in other_table_names
        ]

        # Define helper functions
        def has_hyperlinks(sentence):
            return bool(
                re.search(
                    r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                    sentence,
                )
            )

        def summarize_paragraph(paragraph, title, num_sentences):
            sentences = sent_tokenize(paragraph)
            title_words = word_tokenize(title.lower())
            scores = [
                sum(
                    [
                        1
                        for word in word_tokenize(sentence.lower())
                        if word in title_words
                    ]
                )
                for sentence in sentences
            ]

            chosen_sentences = []
            for score_index in nlargest(
                num_sentences, range(len(scores)), key=scores.__getitem__
            ):
                sentence = sentences[score_index]
                sentence_tokens = word_tokenize(sentence)
                if (
                    len(sentence_tokens) >= 6
                    and len(" ".join(chosen_sentences + [sentence]).split()) <= 80
                    and not has_hyperlinks(sentence)
                ):
                    chosen_sentences.append(sentence)

            if not chosen_sentences:
                top_score_index = max(range(len(scores)), key=scores.__getitem__)
                chosen_sentences.append(sentences[top_score_index])

            summary = " ".join(chosen_sentences)
            summary = summary.replace("\n", " ")
            return summary

        if "News Highlights" not in df.columns:
            paragraphs = df["body"]
            titles = df["title"]
            num_sentences = 2
            summaries = []
            for paragraph, title in zip(paragraphs, titles):
                summary = summarize_paragraph(paragraph, title, num_sentences)
                summaries.append(summary)

            df["News Highlights"] = summaries

        main_table_urls = [
            entity["url"] for entity in main_table_client.list_entities()
        ]

        other_tables_urls = []
        for table_client in other_table_clients:
            other_tables_urls.extend(
                [entity["url"] for entity in table_client.list_entities()]
            )

        existing_urls = main_table_urls + other_tables_urls

        for _, row in df.iterrows():
            if row["url"] not in existing_urls:
                max_length = 32768
                if len(row["processed_content"].encode("utf-16")) > 65536:
                    row["processed_content"] = row["processed_content"][:max_length]
                if len(row["body"].encode("utf-16")) > 65536:
                    row["body"] = row["body"][:max_length]
                if len(row["News Highlights"].encode("utf-16")) > 65536:
                    row["News Highlights"] = row["News Highlights"][:max_length]

                entity = {
                    "PartitionKey": dt.now().strftime("%Y-%m-%d-%H:%M:%S.%f"),
                    "RowKey": dt.today().strftime("%Y-%m-%d"),
                    "query": str(row["query"]),
                    "lang": str(row["lang"]),
                    "date": str(row["date"]),
                    "sim": str(row["sim"]),
                    "url": str(row["url"]),
                    "title": str(row["title"]),
                    "body": str(row["body"]),
                    "source": str(row["source"]),
                    "sentiment": str(row["sentiment"]),
                    "relevance": str(row["relevance"]),
                    "image": str(row["image"]),
                    "processed_content": str(row["processed_content"]),
                    "computed_similarity": str(row["computed_similarity"]),
                    "NewsHighlights": str(row["News Highlights"]),
                }

                if bims_proj:
                    entity["BIMSProject"] = str(row["BIMS Project"])

                main_table_client.create_entity(entity)

        print(f"Successfully updated the table {table_name}.")

    def hasValues(self, df):
        return df.shape[0] > 0

    def retrieve_media(self, queries=[], bims_queries=[]):
        news_dict = get_media_news(self.newsapikey, queries, bims_queries)

        bims_projects_news = news_dict["BIMS Projects News"]
        companies_news = news_dict["Companies News"]
        general_dredg_news = news_dict["General Dredging News"]

        if self.hasValues(general_dredg_news):
            general_dredg_news_filtered = filter_media_articles(general_dredg_news)
            if self.hasValues(general_dredg_news_filtered):
                self.update_azure_table_from_dataframe(
                    "GenDredgMediaNews",
                    general_dredg_news_filtered,
                    ["BIMSProjMediaNews", "CompaniesMediaNews"],
                )

        if self.hasValues(companies_news):
            companies_news_eng = companies_news[companies_news["lang"] == "eng"]
            if self.hasValues(companies_news_eng):
                companies_news_eng_filtered = filter_media_articles(
                    companies_news_eng, train_model=False
                )
                if self.hasValues(companies_news_eng_filtered):
                    self.update_azure_table_from_dataframe(
                        "CompaniesMediaNews",
                        companies_news_eng_filtered,
                        ["BIMSProjMediaNews", "GenDredgMediaNews"],
                    )

            companies_news_foreign = companies_news[
                companies_news["lang"].isin(["nld", "deu"])
            ]
            if self.hasValues(companies_news_foreign):
                companies_news_foreign_filtered = filter_media_articles(
                    companies_news_foreign, train_model=False
                )
                if self.hasValues(companies_news_foreign_filtered):
                    self.update_azure_table_from_dataframe(
                        "CompaniesMediaNews",
                        companies_news_foreign_filtered,
                        ["BIMSProjMediaNews", "GenDredgMediaNews"],
                    )

        if self.hasValues(bims_projects_news):
            bims_projects_news_filtered = filter_media_articles(
                bims_projects_news, train_model=False
            )
            if self.hasValues(bims_projects_news_filtered):
                self.update_azure_table_from_dataframe(
                    "BIMSProjMediaNews",
                    bims_projects_news_filtered,
                    ["CompaniesMediaNews", "GenDredgMediaNews"],
                )
