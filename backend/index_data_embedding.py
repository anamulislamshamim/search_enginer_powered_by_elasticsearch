import torch
from typing import List
from config import INDEX_NAME_EMBEDDING
from utils import get_es_client
from elasticsearch import Elasticsearch, ConnectionTimeout, ConnectionError, TransportError
from tqdm import tqdm
import json
from pprint import pprint
from sentence_transformers import SentenceTransformer
import time


def index_data(documents: List[dict], model: SentenceTransformer):
    es = get_es_client(max_retries=1, sleep_time=0)
    _ = _create_index(es=es)
    _ = _insert_documents(es=es, documents=documents, model=model)
    
    pprint(
        f'Indexed {len(documents)} documents into Elasticsearch index "{INDEX_NAME_EMBEDDING}"'
    )

def _create_index(es: Elasticsearch) -> dict:
    index_name = INDEX_NAME_EMBEDDING

    _ = es.indices.delete(index=index_name, ignore_unavailable=True)
    
    return es.indices.create(
        index=index_name,
        mappings={
            "properties": {
                "embedding": {
                    "type": "dense_vector",
                }
            }
        }
    )


def _insert_documents(es: Elasticsearch, documents: List[dict], model: SentenceTransformer) -> dict:
    INDEX_NAME = INDEX_NAME_EMBEDDING
    operations = []

    for document in tqdm(documents, total=len(documents), desc="Indexing documents.."):
        operations.append({"index": {"_index": INDEX_NAME}}) # action
        operations.append({
            **document,
            "embedding": model.encode(document["explanation"])
        })
    
    MAX_RETRIES = 3
    RETRY_DELAY = 5
    
    for attempt in range(MAX_RETRIES):
        try:
            response = es.bulk(operations=operations, request_timeout=60)
            if response.get("errors"):
                print("⚠️ Some documents failed to index.")
            return response
        
        except (ConnectionTimeout, ConnectionError, TransportError) as e:
            print(f"⚠️ Attempt {attempt+1}/{MAX_RETRIES} failed: {e}")
            time.sleep(RETRY_DELAY)
            
            # Optional reconnect
            es = Elasticsearch(es.transport.hosts)
    
    raise RuntimeError("❌ Failed to insert documents after multiple retries.")


if __name__ == "__main__": 
    with open("../../../data/apod.json") as f:
        documents = json.load(f)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SentenceTransformer("all-MiniLM-L6-v2").to(device)
    index_data(documents=documents, model=model)