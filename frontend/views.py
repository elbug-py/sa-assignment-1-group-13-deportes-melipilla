from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from core.services import get_top_rated_books, get_authors_table, get_top_selling_books
from mongoengine.queryset.visitor import Q
from core.services import search_books_by_summary
from core.models import Author, Book, Review, Sale
from core.search import search_books as es_search_books
from urllib.parse import urlencode
from datetime import datetime


def home(request):
    return render(request, "home.html")


def authors_table(request):
    filters = {
        "name": (request.GET.get("name") or "").strip(),
        "country": (request.GET.get("country") or "").strip(),
    }
    sort = request.GET.get("sort")
    order = request.GET.get("order")
    data = get_authors_table(filters, sort, order)
    paginator = Paginator(data, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    base_params = {k: v for k, v in filters.items() if v}
    base_qs = urlencode(base_params)

    ctx = {
        "page_obj": page_obj,
        "filters": filters,
        "sort": sort,
        "order": order,
        "base_qs": base_qs,
    }
    return render(request, "tables/authorsTable.html", ctx)


def author_create(request):
    if request.method == "POST":
        try:
            author = Author()
            author.name = request.POST.get("name", "").strip()

            birthday = request.POST.get("birthday", "").strip()
            if birthday:
                author.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()

            author.origin_country = request.POST.get("origin_country", "").strip()
            author.description = request.POST.get("description", "").strip()

            author.save()
            messages.success(request, f"Autor '{author.name}' creado exitosamente.")
            return redirect("authors_table")
        except Exception as e:
            messages.error(request, f"Error al crear autor: {str(e)}")

    return render(request, "authors/create.html")


def author_detail(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        messages.error(request, "Autor no encontrado.")
        return redirect("authors_table")

    return render(request, "authors/detail.html", {"author": author})


def author_edit(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        messages.error(request, "Autor no encontrado.")
        return redirect("authors_table")

    if request.method == "POST":
        try:
            author.name = request.POST.get("name", "").strip()

            birthday = request.POST.get("birthday", "").strip()
            if birthday:
                author.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
            else:
                author.birthday = None

            author.origin_country = request.POST.get("origin_country", "").strip()
            author.description = request.POST.get("description", "").strip()

            author.save()
            messages.success(
                request, f"Autor '{author.name}' actualizado exitosamente."
            )
            return redirect("author_detail", author_id=author.id)
        except Exception as e:
            messages.error(request, f"Error al actualizar autor: {str(e)}")

    return render(request, "authors/edit.html", {"author": author})


def author_delete(request, author_id):
    try:
        author = Author.objects.get(id=author_id)
    except Author.DoesNotExist:
        messages.error(request, "Autor no encontrado.")
        return redirect("authors_table")

    if request.method == "POST":
        try:
            author_name = author.name
            author.delete()
            messages.success(request, f"Autor '{author_name}' eliminado exitosamente.")
            return redirect("authors_table")
        except Exception as e:
            messages.error(request, f"Error al eliminar autor: {str(e)}")

    return render(request, "authors/delete.html", {"author": author})


# CRUD DE LIBROS
def books_table(request):
    filters = {
        "name": (request.GET.get("name") or "").strip(),
        "author": (request.GET.get("author") or "").strip(),
    }

    qs = Book.objects.all()

    if filters.get("name"):
        qs = qs.filter(name__icontains=filters["name"])
    if filters.get("author"):
        qs = qs.filter(author__name__icontains=filters["author"])

    sort = request.GET.get("sort")
    order = request.GET.get("order")

    if sort == "name":
        qs = qs.order_by("-name" if order == "desc" else "name")
    elif sort == "author":
        qs = qs.order_by("-author__name" if order == "desc" else "author__name")
    elif sort == "date":
        qs = qs.order_by("-publication_date" if order == "desc" else "publication_date")
    else:
        qs = qs.order_by("name")

    paginator = Paginator(list(qs), 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    base_params = {k: v for k, v in filters.items() if v}
    base_qs = urlencode(base_params)

    ctx = {
        "page_obj": page_obj,
        "filters": filters,
        "sort": sort,
        "order": order,
        "base_qs": base_qs,
    }
    return render(request, "tables/booksTable.html", ctx)


def book_create(request):
    authors = Author.objects.all().order_by("name")

    if request.method == "POST":
        try:
            book = Book()
            book.name = request.POST.get("name", "").strip()

            author_id = request.POST.get("author", "").strip()
            if author_id:
                book.author = Author.objects.get(id=author_id)

            publication_date = request.POST.get("publication_date", "").strip()
            if publication_date:
                book.publication_date = datetime.strptime(
                    publication_date, "%Y-%m-%d"
                ).date()

            book.summary = request.POST.get("summary", "").strip()

            book.save()
            messages.success(request, f"Libro '{book.name}' creado exitosamente.")
            return redirect("books_table")
        except Exception as e:
            messages.error(request, f"Error al crear libro: {str(e)}")

    return render(request, "books/create.html", {"authors": authors})


def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    # Calcular estadísticas de ventas
    sales = Sale.objects(book=book)
    total_sales = sum(s.count for s in sales)
    sales_by_year = {}
    for s in sales:
        sales_by_year[s.year] = sales_by_year.get(s.year, 0) + s.count

    ctx = {
        "book": book,
        "total_sales": total_sales,
        "sales_count": sales.count(),
        "sales_by_year": dict(sorted(sales_by_year.items(), reverse=True)),
    }
    return render(request, "books/detail.html", ctx)


def book_edit(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    authors = Author.objects.all().order_by("name")

    if request.method == "POST":
        try:
            book.name = request.POST.get("name", "").strip()

            author_id = request.POST.get("author", "").strip()
            if author_id:
                book.author = Author.objects.get(id=author_id)

            publication_date = request.POST.get("publication_date", "").strip()
            if publication_date:
                book.publication_date = datetime.strptime(
                    publication_date, "%Y-%m-%d"
                ).date()
            else:
                book.publication_date = None

            book.summary = request.POST.get("summary", "").strip()

            book.save()
            messages.success(request, f"Libro '{book.name}' actualizado exitosamente.")
            return redirect("book_detail", book_id=book.id)
        except Exception as e:
            messages.error(request, f"Error al actualizar libro: {str(e)}")

    return render(request, "books/edit.html", {"book": book, "authors": authors})


def book_delete(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    if request.method == "POST":
        try:
            book_name = book.name
            book.delete()
            messages.success(request, f"Libro '{book_name}' eliminado exitosamente.")
            return redirect("books_table")
        except Exception as e:
            messages.error(request, f"Error al eliminar libro: {str(e)}")

    return render(request, "books/delete.html", {"book": book})


# CRUD DE RESEÑAS
def book_reviews(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    # Obtener reseñas ordenadas por score descendente y luego por up_votes descendente
    reviews = Review.objects(book=book).order_by("-score", "-up_votes")

    # Calcular estadísticas
    total_reviews = reviews.count()
    avg_score = 0
    if total_reviews > 0:
        total_score = sum(r.score for r in reviews)
        avg_score = round(total_score / total_reviews, 2)

    # Paginación
    paginator = Paginator(list(reviews), 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    ctx = {
        "book": book,
        "page_obj": page_obj,
        "total_reviews": total_reviews,
        "avg_score": avg_score,
    }
    return render(request, "reviews/book_reviews.html", ctx)


def review_create(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    if request.method == "POST":
        try:
            score = request.POST.get("score", "").strip()
            up_votes = request.POST.get("up_votes", "").strip()

            if not score:
                messages.error(request, "El puntaje es obligatorio.")
                return render(request, "reviews/create.html", {"book": book})

            review = Review()
            review.book = book
            review.score = int(score)
            review.up_votes = int(up_votes) if up_votes else 0

            review.save()
            messages.success(
                request, f"Reseña agregada exitosamente al libro '{book.name}'."
            )
            return redirect("book_reviews", book_id=book.id)
        except ValueError:
            messages.error(request, "Los valores ingresados no son válidos.")
        except Exception as e:
            messages.error(request, f"Error al crear reseña: {str(e)}")

    return render(request, "reviews/create.html", {"book": book})


# CRUD DE VENTAS
def book_sales(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    # Obtener ventas ordenadas por año descendente
    sales = Sale.objects(book=book).order_by("-year")

    # Calcular estadísticas
    total_sales = sum(s.count for s in sales)
    sales_years = sales.count()
    avg_per_year = round(total_sales / sales_years, 1) if sales_years > 0 else 0

    # Paginación
    paginator = Paginator(list(sales), 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    ctx = {
        "book": book,
        "page_obj": page_obj,
        "total_sales": total_sales,
        "sales_years": sales_years,
        "avg_per_year": avg_per_year,
    }
    return render(request, "sales/book_sales.html", ctx)


def sale_create(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, "Libro no encontrado.")
        return redirect("books_table")

    if request.method == "POST":
        try:
            year = request.POST.get("year", "").strip()
            count = request.POST.get("count", "").strip()

            if not year or not count:
                messages.error(request, "El año y la cantidad son obligatorios.")
                return render(request, "sales/create.html", {"book": book})

            year_int = int(year)
            count_int = int(count)

            if count_int <= 0:
                messages.error(request, "La cantidad debe ser mayor a 0.")
                return render(request, "sales/create.html", {"book": book})

            # Verificar si ya existe una venta para ese año
            existing_sale = Sale.objects(book=book, year=year_int).first()
            if existing_sale:
                # Actualizar la venta existente
                existing_sale.count += count_int
                existing_sale.save()
                messages.success(
                    request,
                    f"Se agregaron {count_int} ventas al año {year_int}. Total: {existing_sale.count} ventas.",
                )
            else:
                # Crear nueva venta
                sale = Sale()
                sale.book = book
                sale.year = year_int
                sale.count = count_int
                sale.save()
                messages.success(
                    request, f"Se agregaron {count_int} ventas para el año {year_int}."
                )

            return redirect("book_sales", book_id=book.id)
        except ValueError:
            messages.error(request, "Los valores ingresados no son válidos.")
        except Exception as e:
            messages.error(request, f"Error al agregar ventas: {str(e)}")

    return render(request, "sales/create.html", {"book": book})


def top_rated(request):
    ctx = {"items": get_top_rated_books()}
    return render(request, "tables/topRated.html", ctx)


def search_books(request):
    q = (request.GET.get("q") or "").strip()
    results = []
    if q:
        results = es_search_books(q)  # returns list of dicts normalized for template

    print("results", results)
    paginator = Paginator(results, 20)  # paginate ES results like before
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "search.html", {"q": q, "page_obj": page_obj})


def top_selling(request):
    ctx = {"items": get_top_selling_books()}
    return render(request, "tables/topSelling.html", ctx)
