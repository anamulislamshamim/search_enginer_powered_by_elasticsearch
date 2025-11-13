![Video Explanation](https://raw.githubusercontent.com/anamulislam/search_enginer_powered_by_elasticsearch/main/video/elastic-search_z4k54XSR.mp4)
# 🧠 AI-Powered Search Engine with Elasticsearch

This project is a **multi-search engine** powered by **Elasticsearch** that combines traditional keyword-based search with **AI-powered semantic search**.
It demonstrates how to build intelligent and scalable search capabilities for modern applications.

---

## 🚀 Features

### 🔹 1. Full-Text Search (Standard Analyzer)

* Uses Elasticsearch’s built-in **standard tokenizer**.
* Performs classic **keyword matching** using `match` and `match_phrase` queries.
* Ideal for exact keyword lookups and structured text.

### 🔹 2. Partial Search (Edge N-Gram)

* Uses a custom **edge_ngram tokenizer** to support **prefix and partial word search**.
* Great for **autocomplete**, **suggestions**, and **instant search** features.
* Example: Searching for `"dev"` can match `"developer"`, `"device"`, etc.

### 🔹 3. Semantic Search (KNN + Embedding)

* Powered by **Hugging Face SentenceTransformer** embeddings.
* Embeddings are stored in Elasticsearch as **dense_vector** fields.
* Uses **KNN search** to find semantically similar results — even if the query doesn’t share exact keywords.
* Example: Query `"AI scientist"` can match `"Machine learning researcher"`.

---

## ⚙️ Tech Stack

| Component           | Technology                           |
| ------------------- | ------------------------------------ |
| **Search Engine**   | Elasticsearch 8.x                    |
| **Language**        | Python 3.x                           |
| **Embedding Model** | Hugging Face SentenceTransformer     |
| **API Framework**   | FastAPI                              |
| **Client**          | Elasticsearch Python Client          |

---

## 🧩 How It Works

### 1️⃣ Index Creation

Each index uses a different analyzer setup:

* **Standard Index:**

  ```json
  "analyzer": "standard"
  ```

* **N-Gram Index:**

  ```json
  "tokenizer": {
      "type": "edge_ngram",
      "min_gram": 2,
      "max_gram": 10
  }
  ```

* **Semantic Index:**

  ```json
  "properties": {
      "embedding": {
          "type": "dense_vector",
          "dims": 384
      }
  }
  ```

### 2️⃣ Query Flow

* **Standard / N-Gram Search:** Uses `match` or `multi_match` queries.
* **Semantic Search:** Converts query text → vector embedding → KNN similarity search.

### 3️⃣ Hybrid Possibility

These methods can later be **fused together** using **RRF (Reciprocal Rank Fusion)** for even better results.

---

## 🔍 Example Query

**Semantic Search:**

```python
query_vector = model.encode("AI in healthcare")

response = es.search(
    index="semantic_index",
    knn={
        "field": "embedding",
        "query_vector": query_vector,
        "k": 3,
        "num_candidates": 10
    }
)
```

**N-Gram Search:**

```python
response = es.search(
    index="ngram_index",
    query={
        "match": {
            "title": "dev"
        }
    }
)
```

---

## 💡 Why This Matters

Modern users expect **intelligent search** — one that understands *meaning*, not just *keywords*.
By integrating Elasticsearch with **AI embeddings**, this project demonstrates how to:

* Improve result **relevance**.
* Enable **semantic understanding** of queries.
* Support **autocomplete** and **context-aware retrieval**.
* Build **scalable, production-ready** search infrastructure.

---

## 🧠 Future Enhancements

* Add **Hybrid Search** (KNN + BM25) using **Reciprocal Rank Fusion (RRF)**.
* Integrate **synonym filters** for multilingual search.
* Add **analytics & metrics** (query trends, search relevance).
* Deploy as a **Dockerized microservice**.

---

## 📬 Acknowledgements

* [Elasticsearch](https://www.elastic.co/) for its powerful search capabilities.
* [Hugging Face](https://huggingface.co/) for SentenceTransformer models.
* [FastAPI](https://fastapi.tiangolo.com/) for building lightweight APIs.
