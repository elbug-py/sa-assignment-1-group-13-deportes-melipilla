import random
from datetime import date
from django.core.management.base import BaseCommand
from faker import Faker
from mongoengine.connection import get_db
from dotenv import load_dotenv
import os

from core.models import Author, Book, Review, Sale
from core.search import (
    bulk_index_authors,
    bulk_index_books,
    bulk_index_reviews,
    bulk_index_sales,
)

faker = Faker()
load_dotenv()
ES_ENABLED = os.getenv("ES_ENABLED", "false").lower() == "true"


class Command(BaseCommand):
    help = "Seed MongoDB with authors, books, reviews, and sales."

    def handle(self, *args, **kwargs):
        db = get_db()

        self.stdout.write("⚡ Dropping old collections...")
        db.drop_collection("author")
        db.drop_collection("book")
        db.drop_collection("review")
        db.drop_collection("sale")

        self.stdout.write("⚡ Seeding Authors...")
        authors = []
        for _ in range(50):
            author = Author(
                name=faker.name(),
                birthday=faker.date_of_birth(minimum_age=30, maximum_age=75),
                origin_country=faker.country(),
                description=faker.sentence(),
            )
            author.save()
            authors.append(author)

        self.stdout.write("⚡ Seeding Books + Reviews + Sales...")
        for _ in range(300):
            author = random.choice(authors)

            book = Book(
                name=" ".join(faker.words(3)),
                summary=faker.paragraph(),
                publication_date=faker.date_between(
                    start_date="-30y", end_date="today"
                ),
                author=author,
            )
            book.save()

            # Reviews (1–10 per book)
            for _ in range(random.randint(1, 10)):
                Review(
                    book=book,
                    score=random.randint(1, 5),
                    up_votes=random.randint(0, 5000),
                ).save()

            # Sales (last 5 years)
            total_sales = 0
            current_year = date.today().year
            for y in range(5):
                year_sales = random.randint(1000, 100000)
                total_sales += year_sales
                Sale(book=book, year=current_year - y, count=year_sales).save()

            book.total_sales = total_sales
            book.save()

        print("Is Elasticsearch enabled?", ES_ENABLED)
        if not ES_ENABLED:
            self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))
            return

        self.stdout.write(self.style.SUCCESS("✅ Seeding complete!"))
        self.stdout.write("⚡ Indexing Books in Elasticsearch...")
        bulk_index_books(Book.objects)
        self.stdout.write("⚡ Indexing Authors in Elasticsearch...")
        bulk_index_authors(Author.objects)
        self.stdout.write("⚡ Indexing Reviews in Elasticsearch...")
        bulk_index_reviews(Review.objects)
        self.stdout.write("⚡ Indexing Sales in Elasticsearch...")
        bulk_index_sales(Sale.objects)
        self.stdout.write(self.style.SUCCESS("✅ Indexing complete!"))
