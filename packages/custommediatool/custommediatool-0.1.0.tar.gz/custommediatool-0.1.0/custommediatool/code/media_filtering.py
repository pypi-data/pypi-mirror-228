import warnings

warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv

abs_directory = os.path.dirname(os.path.abspath(__file__))
env_file = os.path.join(abs_directory, "../../env.env")
load_dotenv(env_file)

import os
import concurrent.futures
import pickle
import re
import pandas as pd
import requests
import numpy as np
from numpy import dot
from numpy.linalg import norm
import gensim
from gensim.models import Word2Vec
import nltk
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
from nltk.corpus import stopwords
from deep_translator import GoogleTranslator
from langdetect import detect
import statistics
from azure.data.tables import TableClient
from datetime import datetime
from datetime import date, timedelta
from gensim.models import Word2Vec
from joblib import Parallel, delayed

np.random.seed(2018)
nltk.download("wordnet")
stemmer = SnowballStemmer("english")


resources_path = os.path.join(abs_directory, "../resources")
media_intel = os.environ.get("media_intel")

path = os.path.join(resources_path, "stop_words_v1.pkl")
with open(path, "rb") as file_content:
    stop_words_v1 = pickle.load(file_content, encoding="latin1")
path = os.path.join(resources_path, "non_maritime_words.pkl")
with open(path, "rb") as file_content:
    non_maritime_words = pickle.load(file_content, encoding="latin1")
path = os.path.join(resources_path, "marine_life_sea_sports_related_words.pkl")
with open(path, "rb") as file_content:
    irrelevant_keywords = pickle.load(file_content, encoding="latin1")

similarity_labels = ["Highly Relevant", "Moderately Relevant", "Less Relevant"]

word2vec_model_path = os.path.join(resources_path, "Word2Vec Trained Model")


def strip_urls(text):
    # Remove URLs from a text string
    return re.sub(r"http\S+|www.\S+", "", text, flags=re.MULTILINE)


def process_description(description, txt_lang=""):
    if not description:
        return description

    description = strip_urls(description)  # remove URLs

    if len(description) > 30:
        try:
            if txt_lang == "":
                txt_lang = detect(description)
            if txt_lang != "en" and (txt_lang == "nld" or txt_lang == "deu"):
                if len(description) > 4999:
                    description = description[0:4999]
                return GoogleTranslator(source="auto", target="en").translate(
                    text=description
                )
        except ValueError as e:
            print(f"Error in detecting language: {str(e)}")
    return description


def remove_stopwords_and_special_chars(
    df_column: pd.core.series.Series,
) -> pd.core.series.Series:
    """
    This function removes stopwords and special characters from a DataFrame column.
    It extends the basic English stopwords list with two custom lists: 'non_maritime_words' and 'stop_words_v1'.
    """

    stop_words = set(stopwords.words("english") + non_maritime_words + stop_words_v1)
    stop_words = {word.lower() for word in stop_words}

    pattern = re.compile(r"\b[^a-zA-Z ]\b")

    df_column = df_column.apply(remove_short_words)
    df_column = df_column.apply(lambda x: pattern.sub("", x))
    df_column = df_column.apply(
        lambda x: " ".join(word for word in x.split() if word.lower() not in stop_words)
    )

    return df_column


def remove_short_words(text: str) -> str:
    exceptions = ["Van", "Oord", "Jan", "De", "Nul", "CCCC", "DEME"]
    words = re.findall(r"\b\w+\b", text)
    filtered_words = [word for word in words if len(word) > 3 or word in exceptions]
    return " ".join(filtered_words)


def lemmatize_stemming(text):
    """
    This function performs lemmatization and stemming on a given text.

    Lemmatization is the process of reducing inflected (or sometimes derived) words to their word base or dictionary form.
    Stemming is the process of reducing inflected (or sometimes derived) words to their word stem, base or root form.
    """
    return stemmer.stem(WordNetLemmatizer().lemmatize(text, pos="v"))


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            if token == "xxxx":
                continue
            result.append(lemmatize_stemming(token))

    return result


def check_url(url):
    if isinstance(url, str) and (
        url.startswith("http://") or url.startswith("https://")
    ):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                return url
        except (requests.ConnectionError, requests.Timeout):
            return None
    return None


def filter_invalid_urls(df):
    urls = df["url"].values

    # checks for valid responses from urls (HTTP status code 200) in a parallelized way
    with concurrent.futures.ThreadPoolExecutor() as executor:
        urls_valid = list(executor.map(check_url, urls))

    urls_valid = [url for url in urls_valid if url]

    return df[df["url"].isin(urls_valid)].reset_index(drop=True)


def word2vec_model(processed_docs):
    """
    This function creates and trains a Word2Vec model using a list of pre-processed documents.

    Args:
    processed_docs (list): A list of pre-processed documents, where each document is a list of tokens.

    Returns:
    Word2Vec: A trained Word2Vec model.
    """
    w2v_model = Word2Vec(
        min_count=1,
        window=5,
        vector_size=300,
        sample=6e-5,
        alpha=0.03,
        min_alpha=0.0005,
        negative=15,
    )

    w2v_model.build_vocab(processed_docs)
    w2v_model.train(
        processed_docs,
        total_examples=w2v_model.corpus_count,
        epochs=300,
        report_delay=1,
    )

    return w2v_model


def prepare_and_train_model(processed_docs):
    """
    This function performs preprocessing on entire content, trains word2vec model on it
    and returns the wordembeddings object.

    Args:
    df: dataframe

    Returns:
    emb_vec: wordembeddings vectors
    """
    processed_docs = list(processed_docs)

    w2v_model = word2vec_model(processed_docs)
    w2v_model.save(word2vec_model_path + "//w2v_model.model")
    emb_vec = w2v_model.wv

    return emb_vec


def find_similarity(sen1, sen2, model):
    """
    Computes the cosine similarity between two sentences.

    This function takes two sentences, preprocesses them and then, converts them
    to vectors having a size of 300 using the provided word embedding model.
    Afterwards, it calculates and returns the cosine similarity between these two vectors.

    Args:
    sen1 (str): The first sentence to compare.
    sen2 (str): The second sentence to compare.
    model (Word2VecKeyedVectors): Word2Vec model used for generating vector representations of sentences.

    Returns:
    float: Cosine similarity between `sen1` and `sen2`.
    """

    p_sen1 = preprocess(sen1)
    p_sen2 = preprocess(sen2)

    sen_vec1 = np.zeros(300)
    sen_vec2 = np.zeros(300)

    for val in p_sen1:
        sen_vec1 = np.add(sen_vec1, model[val])

    for val in p_sen2:
        sen_vec2 = np.add(sen_vec2, model[val])

    return dot(sen_vec1, sen_vec2) / (norm(sen_vec1) * norm(sen_vec2))


def has_irrelevant_keyword(text, irrelevant_keywords):
    for keyword in irrelevant_keywords:
        if keyword in text:
            return True
    return False


def filter_by_similarity(df):
    average_sim = statistics.mean(df["computed_similarity"])
    relevant_articles = df[df["computed_similarity"] > average_sim]

    return relevant_articles


def filter_invalid_and_irrelevant(df, irrelevant_keywords):
    """
    This function filters out invalid and irrelevant articles based on URL and title

    Args:
    df: dataframe
    irrelevant_keywords: list of irrelevant keywords

    Returns:
    df: dataframe with only relevant and valid articles
    """
    df = filter_invalid_urls(df)
    df["is_irrelevant"] = df["title"].apply(
        lambda x: has_irrelevant_keyword(x.lower(), irrelevant_keywords)
    )
    df = df[df["is_irrelevant"] == False]

    return df


def update_and_train_w2v_model(df, model_path):
    """This function updates the trained word2Vec model with new corpus."""
    processed_docs = df["processed_content"].map(preprocess)
    processed_docs = list(processed_docs)

    loaded_model = Word2Vec.load(model_path)

    loaded_model.build_vocab(processed_docs, update=True)

    loaded_model.train(
        processed_docs,
        total_examples=loaded_model.corpus_count,
        epochs=loaded_model.epochs,
    )

    emb_vec = loaded_model.wv

    return emb_vec


def get_bims_data(industry_segments=None):
    """
    This function retrieves and preprocesses data from the 'BIMS' table in an Azure Table Storage.
    It only considers entities added within the last year, filters for certain industry segments,
    groups every 100 descriptions of the same segment together,
    processes the description text, and returns processed content.

    Args:
        industry_segments (list): List of industry segments to consider. Defaults to None.
    Returns:
        pandas.DataFrame: DataFrame containing processed content.
    """

    cutoff_date = date.today() - timedelta(days=365)
    conn_string = os.getenv("conn_string_bims")
    my_filter = f"RowKey gt ''" + cutoff_date
    table_client = TableClient.from_connection_string(
        conn_str=conn_string,
        table_name="BIMS",
    )

    entities = table_client.query_entities(my_filter)
    bims = pd.DataFrame(list(entities))

    if industry_segments is None:
        industry_segments = [
            "Port & Marine Services",
            "Port & Marine development",
            "Inland infrastructure",
            "O&G Refining/Processing",
            "Land Reclamation",
            "Coastal Protection",
            "Plant construction",
        ]

    important_columns = [
        "ProjectMaster_Description",
        "ProjectMaster_IndustrySegment_IndustrySegmentName",
    ]

    bims = bims[important_columns]
    bims = bims[
        bims["ProjectMaster_IndustrySegment_IndustrySegmentName"].isin(
            industry_segments
        )
    ]
    bims = bims.dropna()

    def group_descriptions(df):
        grouped_content = " ".join(df["ProjectMaster_Description"].tolist())
        return pd.Series({"processed_content": grouped_content})

    bims_grouped = (
        bims.groupby("ProjectMaster_IndustrySegment_IndustrySegmentName")
        .apply(
            lambda x: x.reset_index().groupby(x.index // 100).apply(group_descriptions)
        )
        .reset_index(drop=True)
    )

    bims_grouped["processed_content"] = bims_grouped["processed_content"].apply(
        process_description
    )

    bims_grouped["processed_content"] = remove_stopwords_and_special_chars(
        bims_grouped["processed_content"]
    )

    return bims_grouped[["processed_content"]]


def prepare_reference_data(in_dataframes, get_bims=False):
    """
    This function takes as input a list of dataframes and a boolean flag to decide whether to include BIMS data or not.

    Args:
    in_dataframes (list): A list of DataFrame(s) to be processed.
    get_bims (bool): A flag that determines if BIMS data needs to be appended to the dataframes.

    Returns:
    pd.DataFrame: The final dataframe obtained after processing all provided dataframes and appending the BIMS dataframe.

    """

    def process_df(filepath):
        df = pd.read_csv(filepath)

        if "processed_content" not in df.columns:
            df["processed_content"] = (
                df["body"]
                .apply(process_description)
                .pipe(remove_stopwords_and_special_chars)
            )

        if "url" not in df.columns:
            df["url"] = [""] * df.shape[0]

        return df[["processed_content", "url"]]

    if get_bims:
        bims = get_bims_data()

    dataframes = [process_df(df) for df in in_dataframes]
    dataframes.append(bims)

    reference_dataframe = pd.concat(dataframes).reset_index(drop=True)

    table_client = TableClient.from_connection_string(
        media_intel,
        "MediaReferenceData",
    )

    for i in range(len(reference_dataframe)):
        entity = {
            "PartitionKey": datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"),
            "RowKey": datetime.today().strftime("%Y-%m-%d"),
            "url": str(reference_dataframe.loc[i, "url"]),
        }

        processed_content = str(reference_dataframe.loc[i, "processed_content"])

        if len(processed_content.encode("utf-16")) <= 65536:
            entity["processed_content"] = processed_content
        else:
            entity["processed_content"] = processed_content[:32768]

        table_client.create_entity(entity)

    return reference_dataframe


def update_reference_data(df):
    """
    This function prepares the reference dataset through reading all articles CSV files in the given
    data directory, append a new column 'processed_content' to each dataframe after processing the 'body'
    column. The results are then combined into a single dataframe. Also it updates azure tables with
    entries and makes sure entries should not be duplicates of the same url in the azure table.

    Args:
        dir_path (str): The directory path where csv files are located

    Returns:
        pd.DataFrame: The final dataframe obtained after processing all CSVs and appending data to Azure Table Storage.
    """

    def process_df(df):
        if "processed_content" not in df.columns:
            df["processed_content"] = (
                df["body"]
                .apply(process_description)
                .pipe(remove_stopwords_and_special_chars)
            )

        if "url" not in df.columns:
            df["url"] = [""] * df.shape[0]

        return df[["processed_content", "url"]]

    reference_dataframe = process_df(df)

    table_client = TableClient.from_connection_string(
        media_intel,
        "MediaReferenceData",
    )

    for _, row in reference_dataframe.iterrows():
        entities = list(table_client.list_entities())
        entity_urls = [entity["url"] for entity in entities]

        if row["url"] not in entity_urls:
            entity = {
                "PartitionKey": datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"),
                "RowKey": datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f"),
                "url": str(row["url"]),
            }

            processed_content = str(row["processed_content"])

            if len(processed_content.encode("utf-16")) <= 65536:
                entity["processed_content"] = processed_content
            else:
                entity["processed_content"] = processed_content[:32768]

            table_client.create_entity(entity)

    return reference_dataframe


def get_media_reference_data():
    """
    This function retrieves Media ReferenceData from an Azure Table Storage and converts them into pandas DataFrame.

    Args:
        connection_string (str): The connection string to connect to Azure account.
        table_name (str): The name of the table to read from.

    Returns:
        pandas.DataFrame: DataFrame containing content from Azure Table Storage.
    """

    table_client = TableClient.from_connection_string(
        conn_str=media_intel, table_name="MediaReferenceData"
    )
    entities = table_client.list_entities()
    df = pd.DataFrame([entity for entity in entities])

    return df


def filter_media_articles(articles, train_model=True):
    """
    This function is a pipeline for media filtering: it orchestrates the process of reading
    and preparing the data, training the model, computing similarities, and returning
    the filtered results.

    Args:
    articles: dataframe of articles

    Returns:
    filtered_articles: dataframe with articles filtered by similarity and irrelevance
    """
    referece_data = get_media_reference_data()
    reference_data = referece_data.dropna(subset="processed_content")
    df_check = articles.copy()

    df_check["processed_content"] = df_check.apply(
        lambda row: process_description(row["body"], row["lang"]), axis=1
    )
    df_check["processed_content"] = remove_stopwords_and_special_chars(
        df_check["processed_content"]
    )

    urls_in_ref_df = referece_data["url"].dropna()
    df_check_conf = df_check[df_check["url"].isin(urls_in_ref_df)]

    # need to check whether df_check is empty or not after line 128
    complete_df = pd.concat([referece_data, df_check])
    complete_df = complete_df.dropna(subset="processed_content")
    processed_docs = complete_df["processed_content"].map(preprocess)
    if train_model:
        emb_vec = prepare_and_train_model(processed_docs)
    else:
        emb_vec = update_and_train_w2v_model(
            df_check, word2vec_model_path + "//w2v_model.model"
        )

    reference_data = reference_data[~reference_data["url"].isin(df_check["url"].values)]
    df_check = df_check.dropna(subset="processed_content")
    df_check = df_check[~df_check["url"].isin(urls_in_ref_df)]

    reference_data = reference_data[reference_data["url"] != ""]

    # --------------------------------------------------------------------------------------------- First Stage Filtering
    def calc_similarity(i, base_reference, emb_vec):
        s_total = sum(find_similarity(i, j, emb_vec) for j in base_reference)

        return s_total / len(base_reference)

    reference_data = reference_data.dropna(subset="processed_content")
    df_check = df_check.dropna(subset="processed_content")
    base_reference = reference_data["processed_content"].values
    xx = df_check["processed_content"].values

    num_cores = -1
    sim = Parallel(n_jobs=num_cores)(
        delayed(calc_similarity)(i, base_reference, emb_vec) for i in xx
    )

    df_check["computed_similarity"] = sim
    relevant_articles_stage1 = filter_by_similarity(df_check)
    relevant_articles_stage1 = filter_invalid_and_irrelevant(
        relevant_articles_stage1, irrelevant_keywords
    )
    relevant_articles_stage1 = relevant_articles_stage1.drop_duplicates(subset="url")
    # relevant_articles_stage1["similarity_label"] = relevant_articles_stage1[
    #     "computed_similarity"
    # ].apply(assign_label)

    # --------------------------------------------------------------------------------------------- Second Stage Filtering
    df_check_removed = df_check[~df_check["url"].isin(relevant_articles_stage1["url"])]
    xx = df_check_removed["processed_content"].values

    num_cores = -1
    sim = Parallel(n_jobs=num_cores)(
        delayed(calc_similarity)(i, base_reference, emb_vec) for i in xx
    )

    df_check_removed["computed_similarity"] = sim
    relevant_articles_stage2 = df_check_removed[
        df_check_removed["computed_similarity"]
        > statistics.mean(df_check_removed["computed_similarity"])
        + statistics.mean(df_check_removed["computed_similarity"]) / 3
    ]
    relevant_articles_stage2 = filter_invalid_and_irrelevant(
        relevant_articles_stage2, irrelevant_keywords
    )

    filtered_articles = pd.concat(
        [df_check_conf, relevant_articles_stage1, relevant_articles_stage2]
    )

    return filtered_articles
