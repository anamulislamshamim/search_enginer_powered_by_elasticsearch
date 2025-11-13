from typing import List
from config import INDEX_NAME_DEFAULT, INDEX_NAME_N_GRAM
from utils import get_es_client
from elasticsearch import Elasticsearch
from tqdm import tqdm
import json
from pprint import pprint


def index_data(documents: List[dict], use_n_gram_tokenizer: bool = False):
    es = get_es_client(max_retries=5, sleep_time=5)
    _ = _create_index(use_n_gram_tokenizer, es=es)
    _ = _insert_documents(use_n_gram_tokenizer, es=es, documents=documents)
    
    index_name = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT
    pprint(
        f'Indexed {len(documents)} documents into Elasticsearch index "{index_name}"'
    )

def _create_index(use_n_gram_tokenizer: bool, es: Elasticsearch) -> dict:
    tokenizer = 'n_gram_tokenizer' if use_n_gram_tokenizer else 'standard'
    index_name = INDEX_NAME_DEFAULT if tokenizer == 'standard' else INDEX_NAME_N_GRAM

    _ = es.indices.delete(index=index_name, ignore_unavailable=True)
    return es.indices.create(
        index=index_name,
        body={
            "settings": {
                "analysis": {
                    "analyzer": {
                        "default": {
                            "type": "custom",
                            "tokenizer": tokenizer
                        }
                    },
                    "tokenizer": {
                        'n_gram_tokenizer': {
                            "type": "edge_ngram",
                            "min_gram": 1,
                            "max_gram": 30,
                            "token_chars": ["letter", "digit"]
                        }
                    }
                }
            }
        }
    )


def _insert_documents(use_n_gram_tokenizer: bool, es: Elasticsearch, documents: List[dict]) -> dict:
    INDEX_NAME = INDEX_NAME_N_GRAM if use_n_gram_tokenizer else INDEX_NAME_DEFAULT
    operations = []

    for document in tqdm(documents, total=len(documents), desc="Indexing documents.."):
        operations.append({"index": {"_index": INDEX_NAME}}) # action
        operations.append(document)
    
    return es.bulk(operations=operations)


if __name__ == "__main__": 
    with open("../../../data/apod.json") as f:
        documents = json.load(f)
        index_data(documents=documents, use_n_gram_tokenizer=True)