
from mongoengine.queryset.visitor import Q
from core.models import Author, Book, Review, Sale

def get_authors_table(filters: dict, sort: str | None, order: str | None):
    qs = Author.objects
    if filters.get("name"):
        qs = qs.filter(name__icontains=filters["name"])
    if filters.get("country"):
        qs = qs.filter(origin_country__icontains=filters["country"])

    authors = list(qs)
    enriched = []

    for a in authors:
        books_qs = Book.objects(author=a).only("id")
        book_ids = [b.id for b in books_qs]
        books_count = len(book_ids)

        if book_ids:
            rev_qs = Review.objects(book__in=book_ids).only("score")
            total_scores = sum(r.score for r in rev_qs)
            n_reviews = rev_qs.count()
            avg_score = (total_scores / n_reviews) if n_reviews else 0.0
        else:
            avg_score = 0.0

        total_sales = 0
        if book_ids:
            total_sales = sum(s.count for s in Sale.objects(book__in=book_ids).only("count"))

        enriched.append({
            "id": str(a.id),
            "name": a.name,
            "country": a.origin_country or "",
            "books_published": books_count,
            "avg_score": round(avg_score, 2),
            "total_sales": total_sales,
        })

    key_map = {
        "name": lambda x: x["name"].lower(),
        "country": lambda x: (x["country"] or "").lower(),
        "books": lambda x: x["books_published"],
        "score": lambda x: x["avg_score"],
        "sales": lambda x: x["total_sales"],
    }
    key = key_map.get((sort or "name"), key_map["name"])
    reverse = (order == "desc")
    enriched.sort(key=key, reverse=reverse)
    return enriched



def get_top_rated_books(limit=10):

    coll = Review._get_collection()
    pipeline = [
        {"$group": {"_id": "$book", "avg_score": {"$avg": "$score"}}},
        {"$sort": {"avg_score": -1, "_id": 1}},
        {"$limit": int(limit)},
    ]
    ranks = list(coll.aggregate(pipeline))

    items = []
    for row in ranks:
        book = Book.objects(id=row["_id"]).first()
        if not book:
            continue
        best = Review.objects(book=book).order_by("-score", "-up_votes").first()
        worst = Review.objects(book=book).order_by("score", "up_votes").first()
        items.append({
            "book": book,
            "avg_score": row["avg_score"],
            "best": best,
            "worst": worst,
        })
    return items


def get_top_selling_books(limit=50):
    coll = Sale._get_collection()
    pipeline = [
        {"$group": {"_id": "$book", "total_book_sales": {"$sum": "$count"}}},
        {"$sort": {"total_book_sales": -1, "_id": 1}},
        {"$limit": int(limit)},
    ]
    rows = list(coll.aggregate(pipeline))

    items = []
    for r in rows:
        book = Book.objects(id=r["_id"]).first()
        if not book:
            continue


        author_book_ids = [b.id for b in Book.objects(author=book.author).only("id")]
        author_total_sales = 0
        if author_book_ids:
            author_total_sales = sum(s.count for s in Sale.objects(book__in=author_book_ids).only("count"))

        in_top5_pub_year = False
        pub_year = book.publication_date.year if book.publication_date else None
        if pub_year:
            year_pipeline = [
                {"$match": {"year": int(pub_year)}},
                {"$group": {"_id": "$book", "s": {"$sum": "$count"}}},
                {"$sort": {"s": -1, "_id": 1}},
                {"$limit": 5},
            ]
            top5 = list(Sale._get_collection().aggregate(year_pipeline))
            top5_ids = {row["_id"] for row in top5}
            in_top5_pub_year = (book.id in top5_ids)

        items.append({
            "book": book,
            "total_book_sales": r.get("total_book_sales", 0),
            "author_total_sales": author_total_sales,
            "in_top5_pub_year": in_top5_pub_year,
        })
    return items


def search_books_by_summary(q: str):
    if not q:
        return Book.objects.order_by("name")
    words = [w for w in q.split() if w]
    cond = Q()
    for w in words:
        cond |= Q(summary__icontains=w)
    return Book.objects(cond).order_by("name")
