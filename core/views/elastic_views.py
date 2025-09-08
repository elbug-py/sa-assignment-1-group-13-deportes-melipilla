from django.http import JsonResponse
from django.views.decorators.http import require_GET
from core.search import search_books, search_authors, search_reviews, search_sales


@require_GET
def search_books_view(request):
    q = request.GET.get("q", "")
    if not q:
        return JsonResponse({"error": "Missing query"}, status=400)
    results = search_books(q)
    return JsonResponse({"results": results})


@require_GET
def search_authors_view(request):
    q = request.GET.get("q", "")
    if not q:
        return JsonResponse({"error": "Missing query"}, status=400)
    results = search_authors(q)
    return JsonResponse({"results": results})


@require_GET
def search_reviews_view(request):
    q = request.GET.get("q", "")
    if not q:
        return JsonResponse({"error": "Missing query"}, status=400)
    results = search_reviews(q)
    return JsonResponse({"results": results})


@require_GET
def search_sales_view(request):
    q = request.GET.get("q", "")
    if not q:
        return JsonResponse({"error": "Missing query"}, status=400)
    results = search_sales(q)
    return JsonResponse({"results": results})
