from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from core.models import Book, Author


@csrf_exempt
@require_http_methods(["GET"])
def book_list(request):
    books = Book.objects.all()
    data = [
        {
            "id": str(book.id),
            "author": str(book.author.id) if book.author else None,
            "name": book.name,
            "summary": book.summary,
            "publication_date": book.publication_date,
        }
        for book in books
    ]
    return JsonResponse({"books": data})


@csrf_exempt
@require_http_methods(["POST"])
def book_create(request):
    import json
    try:
        data = json.loads(request.body)
        author_id = data.get("author")
        name = data.get("name")
        summary = data.get("summary")
        publication_date = data.get("publication_date")
        author = Author.objects.get(id=author_id)
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or Author not found")

    book = Book(author=author, name=name, summary=summary, publication_date=publication_date)
    book.save()
    return JsonResponse({
        "id": str(book.id),
        "author": str(book.author.id),
        "name": book.name,
        "summary": book.summary,
        "publication_date": book.publication_date,
    }, status=201)


@csrf_exempt
@require_http_methods(["PUT"])
def book_edit(request, book_id):
    import json
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound("Book not found")
    try:
        data = json.loads(request.body)
        if "author" in data:
            book.author = Author.objects.get(id=data["author"])
        book.name = data.get("name", book.name)
        book.summary = data.get("summary", book.summary)
        book.publication_date = data.get("publication_date", book.publication_date)
        book.save()
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or Author not found")
    return JsonResponse({
        "id": str(book.id),
        "author": str(book.author.id),
        "name": book.name,
        "summary": book.summary,
        "publication_date": book.publication_date,
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def book_delete(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound("Book not found")
    book.delete()
    return JsonResponse({"result": "deleted"})


@csrf_exempt
@require_http_methods(["GET"])
def book_detail(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return HttpResponseNotFound("Book not found")
    data = {
        "id": str(book.id),
        "author": str(book.author.id) if book.author else None,
        "name": book.name,
        "summary": book.summary,
        "publication_date": book.publication_date,
    }
    return JsonResponse(data)
