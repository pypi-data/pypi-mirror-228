# Dredging Media Retrieval Pipeline

This repository contains code for retrieving targeted media news about dredging, specific dredging projects, and news about competitors within the dredging industry.

## Overview

The repo utilizes a Python script, `media_pipeline.py`, that collects and filters news data. It uses different functions provided within the repo to:

- Retrieve news
- Filter irrelevant articles
- Update an Azure table with the filtered news data, separated into categories, namely:
  - General Dredging projects, 
  - Boskalis Intelligence Marketing System (BIMS) Projects, 
  - Companies (competitors within the dredging industry)

## Installation

1. Install the BKWMediaTool library using `pip`:

```bash
   pip install bkwmediatool
```
To instantiate the BKWMediaTool class, follow these steps:

1. Import the BKWMediaTool class from the bkwmediatool.code module:
 ```bash

from bkwmediatool.code import BKWMediaTool
```
2. Create an instance of the BKWMediaTool class and give the newsapi.ai key as an input:
```python
bkw_tool = BKWMediaTool(newsapikey)
```
## Repository Content

- Main Python function: retrieve_media()
- Other support functions to fetch and filter data (media_retrieval.py and media_filtering.py)

```python
def retrieve_media():
    """
    Args: 
        None

    Prints: 
        Statements indicating the updating of each Azure Table.

    Returns: 
        None
    """
```
This function retrieves and processes different types of news related to dredging. 

It retrieves 'BIMS Projects News', 'Companies News', and 'General Dredging News' using the get_media_news() function. The function then returns a dictionary mapping these categories to their respective datasets.

The returned new articles are then filtered using the filter_media_articles() function, which removes irrelevant articles.

The processed news data is then stored in different Azure tables ('GenDredgMediaNews', 'CompaniesMediaNews', and 'BIMSProjMediaNews'). 'Companies News' is further divided into English and foreign-language categories using language identification before filtering and storing.

Each Azure Table updating operation completion will be indicated with a print statement.

```python
def prepare_reference_data(in_dataframes, get_bims)
"""    
    Args:
    in_dataframes (list): A list of DataFrame(s) to be processed.
    get_bims (bool): A flag that determines if BIMS data needs to be appended to the dataframes.

    Returns:
    pd.DataFrame: The final dataframe obtained after processing all provided dataframes and appending the BIMS dataframe.
    
    """
```
This function prepares reference data from multiple dataframes, processing each dataframe and appending a Business Information Management System (BIMS) dataframe, if required.
```python
def update_reference_data(df):
    """
    Args:
        df (pd.DataFrame): An input dataframe containing media articles which needs to be processed and stored.

    Returns:
        pd.DataFrame: The final dataframe obtained after processing the input dataframe and updating the Azure table.
    """
```
This function processes a given dataframe, updates the Azure table 'MediaReferenceData' with the cleaned data, and ensures there are no duplicates of the same URL within the Azure table. Referennce data only has the columns: processed_content and url, however the function processes the body of the articles if this has not been done before passing the dataframe to the function.

```python
def get_media_reference_data():
    """
    Args:
        None

    Returns:
        pandas.DataFrame: DataFrame containing data retrieved from Azure Table Storage.
    """
```
This function retrieves Media ReferenceData from Azure Table Storage then converts them into a pandas DataFrame object.

```python
def filter_media_articles(articles, train_model=True):
    """    
    Args:
        articles (pandas.DataFrame): dataframe of articles.
        train_model (boolean): option for training the model. Default True. 

    Returns:
        filtered_articles (pandas.DataFrame): dataframe with articles filtered by similarity and irrelevance.
    """
```
This function filters media articles through a two-stage process ensuring only relevant and valid articles are captured.
```python
def get_media_news(queries=[], bims_queries=[]):
    """
    Retrieve and process media news related to dredging companies, industry and specific BIMS projects.
    
    Args:
        queries (list): Optional. A list of additional search queries for 'General Industry Related News'.
        bims_queries (list): Optional. A list queries for 'BIMS Projects News', each element consists of a tuple containing a query and the name of the BIMS projects e.g. ("Baggerproject Surinamerivier","Suriname River Dredging - Phase 2") . 
        Default is an empty list.

    Returns:
        dict: A dictionary containing three DataFrames: 
              'BIMS Projects News': News articles specific to BIMS projects. 
              'Companies News': News articles about predefined companies.
              'General Dredging News': News articles related to general dredging industry.
    """
```
This function retrieves and processes media news articles related to various dredging companies, the general dredging industry, and specific BIMS projects. After collecting and processing targeted news articles, it generates a dictionary with three DataFrames. Each DataFrame holds news about 'BIMS Projects', 'Companies', and 'General Dredging' respectively.


```python
def update_azure_table_from_dataframe(table_name, df, other_table_names, bims_proj=False):
    """
    Args:
        table_name (str): The name of the table to be updated.
        df (pandas.DataFrame): The DataFrame whose data is intended to be added to the Azure tables.
        other_table_names (list[str]): List of two other table names in which duplicate URLs should not exist.
        bims_proj (bool, optional): A flag to determine if the 'BIMS Project' column of the DataFrame is to be included in the Azure entity. Defaults to False.

    Prints:
        States a success message indicating the name of the updated table after operation completion.

    Returns:
        None
    """
```
This function updates an Azure Table with DataFrame content while checking for duplicated URLs in this table including two other specified tables. These tables store content for media articles related to general dredging news, specific BIMS projects, and articles related to various dredging companies. 
