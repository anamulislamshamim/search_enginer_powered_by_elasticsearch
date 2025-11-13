from typing import List
from config import INDEX_NAME_RAW
from utils import get_es_client
from elasticsearch import Elasticsearch
from tqdm import tqdm
import json
from pprint import pprint


def index_data(documents: List[dict]):
    pipeline_name = "apod_raw_pipeline"
    es = get_es_client(max_retries=1, sleep_time=0)

    _ = _create_pipeline(es=es, pipeline_id=pipeline_name)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents, pipeline_id=pipeline_name)
    
    pprint(
        f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME_RAW}"'
    )

def _create_index(es: Elasticsearch) -> dict:
    index_name = INDEX_NAME_RAW

    _ = es.indices.delete(index=index_name, ignore_unavailable=True)
    return es.indices.create(
        index=index_name
    )


def _insert_documents(es: Elasticsearch, documents: List[dict], pipeline_id: str) -> dict:
    INDEX_NAME = INDEX_NAME_RAW
    operations = []

    for document in tqdm(documents, total=len(documents), desc="Indexing documents.."):
        operations.append({"index": {"_index": INDEX_NAME}}) # action
        operations.append(document)
    
    return es.bulk(operations=operations, pipeline=pipeline_id)


def _create_pipeline(es: Elasticsearch, pipeline_id: str):
    pipeline_body = {
        "description": "Pipeline that strips HTML tags from the explanation and title fields",
        "processors": [
            {
                "html_strip": {
                    "field": "explanation"
                }
            },
            {
                "html_strip": {
                    "field": "title"
                }
            }
        ]
    }

    return es.ingest.put_pipeline(id=pipeline_id, body=pipeline_body)


if __name__ == "__main__": 
    with open("../../../data/apod_raw.json") as f:
        documents = json.load(f)
        index_data(documents=documents)