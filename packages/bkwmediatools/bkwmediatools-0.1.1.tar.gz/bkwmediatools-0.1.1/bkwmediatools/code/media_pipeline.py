import warnings

warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv

abs_directory = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(abs_directory, "../../env.env")
load_dotenv(env_file)
from eventregistry import *
import numpy as np

np.random.seed(2018)

from media_retrieval import get_media_news
from media_filtering import filter_media_articles


# Global Variables
media_intel = os.environ.get("media_intel")

from azure.data.tables import TableClient
from datetime import datetime
import os


def sanitize_property_name(name):
    invalid_chars = ["/", "\\", "#", "?"]
    for char in invalid_chars:
        name = name.replace(char, "")
    if name[0] in ["/", "_"]:
        name = name[1:]
    return name


def update_azure_table_from_dataframe(
    table_name, df, other_table_names, bims_proj=False
):
    """
    This function updates an Azure Table with DataFrame content. It checks for duplicate URLs in this table as well as two others


    Args:
        table_name(str): The name of the table that needs to be updated.
        df(pandas.DataFrame): The dataframe whose data needs to be added to the tables.
        other_table_names(list[string]): Names of two other tables in which duplicate URLs should not be present.
    """

    import nltk
    import re
    from nltk.tokenize import sent_tokenize, word_tokenize
    from heapq import nlargest

    # Connect to Azure table
    main_table_client = TableClient.from_connection_string(media_intel, table_name)

    other_table_clients = [
        TableClient.from_connection_string(media_intel, table_name)
        for table_name in other_table_names
    ]

    # compute News Highlights
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
            sum([1 for word in word_tokenize(sentence.lower()) if word in title_words])
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

        # Construct the summary from the chosen sentences
        summary = " ".join(chosen_sentences)
        summary = summary.replace("\n", " ")
        return summary

    if "News Highlights" not in df.columns:
        paragraphs = df["body"]
        titles = df["title"]
        num_sentences = 2  # Update to select 3 most related sentences
        summaries = []
        for paragraph, title in zip(paragraphs, titles):
            summary = summarize_paragraph(paragraph, title, num_sentences)
            summaries.append(summary)

        df["News Highlights"] = summaries

    main_table_urls = [entity["url"] for entity in main_table_client.list_entities()]

    # Extract URLs from the other tables
    other_tables_urls = []
    for table_client in other_table_clients:
        other_tables_urls.extend(
            [entity["url"] for entity in table_client.list_entities()]
        )

    # Combine URLs
    existing_urls = main_table_urls + other_tables_urls

    for _, row in df.iterrows():
        if row["url"] not in existing_urls:
            max_length = 32768
            if len(row["processed_content"].encode("utf-16")) > 65536:
                print("yes")
                row["processed_content"] = row["processed_content"][:max_length]

            if len(row["body"].encode("utf-16")) > 65536:
                row["body"] = row["body"][:max_length]

            if len(row["News Highlights"].encode("utf-16")) > 65536:
                row["News Highlights"] = row["News Highlights"][:max_length]

            entity = {
                "PartitionKey": datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"),
                "RowKey": datetime.today().strftime("%Y-%m-%d"),
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


def hasValues(df):
    return df.shape[0] > 0


def retrieve_media(queries=[], bims_queries=[]):
    news_dict = get_media_news(queries, bims_queries)

    bims_projects_news = news_dict["BIMS Projects News"]
    companies_news = news_dict["Companies News"]
    general_dredg_news = news_dict["General Dredging News"]

    if hasValues(general_dredg_news):
        general_dredg_news_filtered = filter_media_articles(general_dredg_news)
        if hasValues(general_dredg_news_filtered):
            update_azure_table_from_dataframe(
                "GenDredgMediaNews",
                general_dredg_news_filtered,
                ["BIMSProjMediaNews", "CompaniesMediaNews"],
            )
    if hasValues(companies_news):
        companies_news_eng = companies_news[companies_news["lang"] == "eng"]

        if hasValues(companies_news_eng):
            companies_news_eng_filtered = filter_media_articles(
                companies_news_eng, train_model=False
            )
            if hasValues(companies_news_eng_filtered):
                update_azure_table_from_dataframe(
                    "CompaniesMediaNews",
                    companies_news_eng_filtered,
                    ["BIMSProjMediaNews", "GenDredgMediaNews"],
                )
        companies_news_foreign = companies_news[
            companies_news["lang"].isin(["nld", "deu"])
        ]
        if hasValues(companies_news_foreign):
            companies_news_foreign_filtered = filter_media_articles(
                companies_news_foreign, train_model=False
            )
            if hasValues(companies_news_foreign_filtered):
                update_azure_table_from_dataframe(
                    "CompaniesMediaNews",
                    companies_news_foreign_filtered,
                    ["BIMSProjMediaNews", "GenDredgMediaNews"],
                )

    if hasValues(bims_projects_news):
        bims_projects_news_filtered = filter_media_articles(
            bims_projects_news, train_model=False
        )
        if hasValues(bims_projects_news_filtered):
            update_azure_table_from_dataframe(
                "BIMSProjMediaNews",
                bims_projects_news_filtered,
                ["CompaniesMediaNews", "GenDredgMediaNews"],
            )
