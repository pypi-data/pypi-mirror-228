import warnings

warnings.filterwarnings("ignore")
import pandas as pd
from eventregistry import *
import os
from dotenv import load_dotenv

abs_directory = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(abs_directory, "../../env.env")
load_dotenv(env_file)


def create_dataframe_from_newsapi_ai_articles(media_articles, query, bims_oppr=""):
    columns_list = [
        "query",
        "uri",
        "lang",
        "isDuplicate",
        "date",
        "time",
        "dateTime",
        "dateTimePub",
        "dataType",
        "sim",
        "url",
        "title",
        "body",
        "source",
        "dataType",
        "sentiment",
        "wgt",
        "relevance",
        "image",
    ]

    if bims_oppr != "":
        columns_list.append("BIMS Project")

        df = pd.DataFrame(columns=columns_list)

    data = []
    for media_file in media_articles:
        if media_file["isDuplicate"] == False:
            new_row = {
                "query": query,
                "uri": media_file["uri"],
                "lang": media_file["lang"],
                "isDuplicate": media_file["isDuplicate"],
                "date": media_file["date"],
                "sim": media_file["sim"],
                "url": media_file["url"],
                "title": media_file["title"],
                "body": media_file["body"],
                "source": media_file["source"]["uri"],
                "sentiment": media_file["sentiment"],
                "wgt": media_file["wgt"],
                "relevance": media_file["relevance"],
                "image": media_file["image"],
            }

            if bims_oppr != "":
                new_row["BIMS Project"] = bims_oppr
            data.append(new_row)

    df = pd.DataFrame(data)

    return df


def get_companies_news(newsapikey, company, nmax=10, company_wiki=""):
    """
    This function fetches and processes company-related news articles.
    If a Wikipedia URI for the company is provided, it's used as a query filter;
    otherwise, the company name is used.

    Extra articles are retrieved using additional keywords ('vessel', 'dredger', 'dredging').

    The articles retrieved are transformed into a dataframe,
    duplicates based on url, title, and body are removed.

    Args:
        company (str): The company to search articles for.
        nmax (int, optional): Maximum articles per query to retrieve. Defaults to 10.
        company_wiki (str, optional): Wikipedia URI of the company. Defaults to "".

    Returns:
        pandas.DataFrame: DataFrame of unique articles.

    """
    er = EventRegistry(apiKey=newsapikey, allowUseOfArchive=False)
    articles = []
    if len(company_wiki) > 0:
        query = {
            "$query": {"conceptUri": company_wiki},
            "$filter": {
                "forceMaxDataTimeWindow": "31",
                "dataType": ["news", "pr", "blog"],
                "isDuplicate": "skipDuplicates",
            },
        }

    else:
        query = {
            "$query": {
                "keyword": company,
                "keywordSearchMode": "exact",
            },
            "$filter": {
                "forceMaxDataTimeWindow": "31",
                "dataType": ["news", "pr", "blog"],
                "isDuplicate": "skipDuplicates",
            },
        }
    q = QueryArticlesIter.initWithComplexQuery(query)
    for article in q.execQuery(er, maxItems=nmax):
        articles.append(article)
    query = {
        "$query": {
            "keyword": company + " AND (vessel OR dredger OR dredging)",
            "keywordSearchMode": "exact",
        },
        "$filter": {
            "forceMaxDataTimeWindow": "31",
            "dataType": ["news", "pr", "blog"],
            "isDuplicate": "skipDuplicates",
        },
    }
    q = QueryArticlesIter.initWithComplexQuery(query)
    for article in q.execQuery(er, maxItems=nmax):
        articles.append(article)
    dataframe = create_dataframe_from_newsapi_ai_articles(articles, company)
    dataframe = dataframe.drop_duplicates(subset="url")
    dataframe = dataframe.drop_duplicates(subset="title")
    dataframe = dataframe.drop_duplicates(subset="body")
    return dataframe


def get_dredging_news(newsapikey, target_query, bims_oppr="", nmax=10):
    """
    This function fetches and deduplicates dredging-related news articles given a search keyword ('target_query').
    It uses exact match for its search.
    It retrieves a maximum of 'nmax' articles (defaulted to 10) from data sources of type "news", "pr", or "blog".

    The retrieved articles are processed into a pandas dataframe with duplicates removed based on url, title, and body.

    Args:
        target_query (str): keyword to search for.
        nmax (int, optional): Maximum articles to retrieve. Defaults to 10.

    Returns:
        pandas.DataFrame : DataFrame of unique articles.
    """
    er = EventRegistry(apiKey=newsapikey, allowUseOfArchive=False)
    query = {
        "$query": {
            "keyword": target_query,
            "keywordSearchMode": "exact",
        },
        "$filter": {
            "forceMaxDataTimeWindow": "31",
            "dataType": ["news", "pr", "blog"],
            "isDuplicate": "skipDuplicates",
        },
    }
    q = QueryArticlesIter.initWithComplexQuery(query)
    articles = []
    for article in q.execQuery(er, maxItems=nmax):
        articles.append(article)
    dataframe = create_dataframe_from_newsapi_ai_articles(
        articles, target_query, bims_oppr
    )
    dataframe = dataframe.drop_duplicates(subset="url")
    dataframe = dataframe.drop_duplicates(subset="title")
    dataframe = dataframe.drop_duplicates(subset="body")
    return dataframe


def get_media_news(newsapikey, queries=[], bims_queries=[]):
    """
    This function retrieves and processes media news articles related to various
    dredging companies, the general dredging industry, and specific BIMS projects.

    It cycles through a predefined list of companies, general dredging related queries,
    and predefined BIMS project-specific queries, obtaining and processing targeted news
    articles by calling the functions 'get_companies_news' and 'get_dredging_news'.

    A final dataframe is created by concatenating all the dataframes obtained from each targeted search query.

    Returns:
        dict: A dictionary containing three elements:
            'BIMS Projects News': a DataFrame of news articles specific to BIMS projects.
            'Companies News': a DataFrame of news articles about predefined companies.
            'General Dredging News': a DataFrame of news articles related to general dredging industry.
    """

    # ------------------------------------------------------------------------------------------------------------------------------------ Companies
    companies_news_dataframes = []

    comapnies = [
        "Boskalis",
        "Van Oord",
        "Jan De Nul",
        "National Marine Dredging Company",
        "CCCC",
        "DEME",
        '"Rohde Nielsen" OR "Rohde Nielsen A/S"',
    ]

    companies_wiki = {
        "Boskalis": "http://en.wikipedia.org/wiki/Boskalis",
        "Van Oord": "http://en.wikipedia.org/wiki/Van_Oord",
        "Jan De Nul": "http://en.wikipedia.org/wiki/Jan_De_Nul",
        "National Marine Dredging Company": "",
        "CCCC": "http://en.wikipedia.org/wiki/China_Harbour_Engineering_Company",
        "DEME": "https://en.wikipedia.org/wiki/DEME",
        '"Rohde Nielsen" OR "Rohde Nielsen A/S"': "",
    }

    for company in comapnies:
        companies_news_dataframes.append(
            get_companies_news(newsapikey, company, 20, companies_wiki.get(company))
        )

    comnpanies_news_df = pd.concat(companies_news_dataframes)

    # ------------------------------------------------------------------------------------------------------------------------------------ General Industry Related News
    if len(queries) > 0:
        gen_dredg_queries = gen_dredg_queries + queries

    gen_dredg_queries = [
        '("Funding for construction" AND dredging) OR ("dredging contract" AND cost)',
        '"reclamation project" AND cost AND hectares',
        "Beach AND replenishment AND Dredging",
        "Canal AND Dredging AND Port AND Infrastructure",
        '"Construction of" AND quay AND dredge',
        '(jetty AND construction AND dredging) OR (award AND "dredging contract")',
        'Dredging AND "contract worth"',
        "marine AND dredging AND project AND announce",
        '"dredging project" AND company AND construction AND (million OR billion OR $)',
    ]

    general_dredg_news_dataframes = []

    for query in gen_dredg_queries:
        general_dredg_news_dataframes.append(get_dredging_news(newsapikey, query, 20))

    general_dredg_news_df = pd.concat(general_dredg_news_dataframes)

    # ------------------------------------------------------------------------------------------------------------------------------------ BIMS Projects News
    if len(bims_queries) > 0:
        bims_projects_news_dataframes = []

        for query in bims_queries:
            bims_projects_news_dataframes.append(
                get_dredging_news(newsapikey, query[0], query[1], 20)
            )

        bims_projects_news_df = pd.concat(bims_projects_news_dataframes)

    return {
        "BIMS Projects News": bims_projects_news_df.reset_index(drop=True),
        "Companies News": comnpanies_news_df.reset_index(drop=True),
        "General Dredging News": general_dredg_news_df.reset_index(drop=True),
    }
