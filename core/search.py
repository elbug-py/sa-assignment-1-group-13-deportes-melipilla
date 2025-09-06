from elasticsearch import Elasticsearch
from django.conf import settings

es = Elasticsearch(settings.ELASTICSEARCH_URL)


def index_book(book):
    es.index(
        index="books",
        id=str(book.id),
        document={
            "name": book.name,
            "summary": book.summary,
            "author": book.author.name if book.author else None,
            "publication_date": str(book.publication_date),
        },
    )


def search_books(query):
    res = es.search(
        index="books",
        query={
            "multi_match": {"query": query, "fields": ["name", "author", "summary"]}
        },
    )
    return [hit["_source"] for hit in res["hits"]["hits"]]
