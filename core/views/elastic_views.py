from django.http import JsonResponse
from django.views.decorators.http import require_GET
from core.search import search_books


@require_GET
def search_books_view(request):
    q = request.GET.get("q", "")
    if not q:
        return JsonResponse({"error": "Missing query"}, status=400)
    results = search_books(q)
    return JsonResponse({"results": results})
