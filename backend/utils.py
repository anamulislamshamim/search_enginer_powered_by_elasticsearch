import time 

from pprint import pprint 
from elasticsearch import Elasticsearch


def get_es_client(max_retries: int = 5, sleep_time: int = 5) -> Elasticsearch:
    i = 0
    while i < max_retries:
        try:
            es = Elasticsearch("http://localhost:9200")
            client_info = es.info()
            pprint("Connected to Elasticsearch successfully!")
            return es 
        except Exception as e:
            pprint("Sorry! Could not connect to Elasticsearch")
            pprint(str(e))
            # retry after waiting
            time.sleep(sleep_time)
            i += 1
    raise ConnectionError(f"Failed to connect to Elasticsearch after {max_retries} attempts!")