from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
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


def bulk_index_books(books):
    actions = [
        {
            "_index": "books",
            "_id": str(book.id),
            "_source": {
                "name": book.name,
                "summary": book.summary,
                "author": book.author.name if book.author else None,
                "publication_date": str(book.publication_date),
            },
        }
        for book in books
    ]
    bulk(es, actions)


def index_author(author):
    es.index(
        index="authors",
        id=str(author.id),
        document={
            "id": str(author.id),
            "name": author.name,
            "country": author.origin_country,  # <- match template
            "books_published": getattr(author, "books_published", 0),
            "avg_score": getattr(author, "avg_score", 0),
            "total_sales": getattr(author, "total_sales", 0),
        },
    )


def bulk_index_authors(authors):
    actions = [
        {
            "_index": "authors",
            "_id": str(author.id),
            "_source": {
                "id": str(author.id),
                "name": author.name,
                "country": author.origin_country,
                "books_published": getattr(author, "books_published", 0),
                "avg_score": getattr(author, "avg_score", 0),
                "total_sales": getattr(author, "total_sales", 0),
            },
        }
        for author in authors
    ]
    bulk(es, actions)


def index_review(review):
    es.index(
        index="reviews",
        id=str(review.id),
        document={
            "book": str(review.book.id) if review.book else None,
            "score": review.score,
            "up_votes": review.up_votes,
        },
    )


def bulk_index_reviews(reviews):
    actions = [
        {
            "_index": "reviews",
            "_id": str(review.id),
            "_source": {
                "book": str(review.book.id) if review.book else None,
                "score": review.score,
                "up_votes": review.up_votes,
            },
        }
        for review in reviews
    ]
    bulk(es, actions)


def index_sale(sale):
    es.index(
        index="sales",
        id=str(sale.id),
        document={
            "book": str(sale.book.id) if sale.book else None,
            "count": sale.count,
            "year": sale.year,
        },
    )


def bulk_index_sales(sales):
    actions = [
        {
            "_index": "sales",
            "_id": str(sale.id),
            "_source": {
                "book": str(sale.book.id) if sale.book else None,
                "count": sale.count,
                "year": sale.year,
            },
        }
        for sale in sales
    ]
    bulk(es, actions)


def search_books(query, sort="name", order="asc"):
    sort_field = f"{sort}.keyword" if sort in ["name", "author"] else sort
    sort_clause = [{sort_field: {"order": order}}] if sort else None

    res = es.search(
        index="books",
        query={
            "multi_match": {
                "query": query,
                "fields": ["name", "author", "summary"],
                "fuzziness": "AUTO",
            }
        },
        sort=sort_clause,
        size=100,
    )
    return [{**hit["_source"], "id": hit["_id"]} for hit in res["hits"]["hits"]]


def search_authors(query, sort="name", order="asc"):
    sort_field = f"{sort}.keyword" if sort in ["name", "country"] else sort

    sort_clause = [{sort_field: {"order": order}}] if sort else None

    res = es.search(
        index="authors",
        query={
            "multi_match": {
                "query": query,
                "fields": ["name", "country"],
                "fuzziness": "AUTO",
            }
        },
        sort=sort_clause,
        size=100,
    )

    return [{**hit["_source"], "id": hit["_id"]} for hit in res["hits"]["hits"]]


def search_reviews(query):
    res = es.search(
        index="reviews",
        query={"multi_match": {"query": query, "fields": ["book", "score"]}},
    )
    return [hit["_source"] for hit in res["hits"]["hits"]]


def search_sales(query):
    res = es.search(
        index="sales",
        query={"multi_match": {"query": query, "fields": ["book", "year"]}},
    )
    return [hit["_source"] for hit in res["hits"]["hits"]]
