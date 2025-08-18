from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from core.models import Book


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
        from core.models import Author
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
    book = get_object_or_404(Book, id=book_id)
    try:
        data = json.loads(request.body)
        if "author" in data:
            from core.models import Author
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
    book = get_object_or_404(Book, id=book_id)
    book.delete()
    return JsonResponse({"result": "deleted"})
