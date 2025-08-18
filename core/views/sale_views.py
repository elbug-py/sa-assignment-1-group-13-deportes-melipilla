from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from core.models import Sale, Book

@csrf_exempt
@require_http_methods(["GET"])
def sale_list(request):
    sales = Sale.objects.all()
    data = [
        {
            "id": str(sale.id),
            "book": str(sale.book.id) if sale.book else None,
            "count": sale.count,
            "year": sale.year,
        }
        for sale in sales
    ]
    return JsonResponse({"sales": data})

@csrf_exempt
@require_http_methods(["POST"])
def sale_create(request):
    import json
    try:
        data = json.loads(request.body)
        book_id = data.get("book")
        count = data.get("count")
        year = data.get("year")
        book = Book.objects.get(id=book_id)
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or Book not found")

    sale = Sale(book=book, count=count, year=year)
    sale.save()
    return JsonResponse({
        "id": str(sale.id),
        "book": str(sale.book.id),
        "count": sale.count,
        "year": sale.year,
    }, status=201)

@csrf_exempt
@require_http_methods(["PUT"])
def sale_edit(request, sale_id):
    import json
    try:
        sale = Sale.objects.get(id=sale_id)
    except Sale.DoesNotExist:
        return HttpResponseNotFound("Sale not found")
    try:
        data = json.loads(request.body)
        if "book" in data:
            sale.book = Book.objects.get(id=data["book"])
        if "count" in data:
            sale.count = data["count"]
        if "year" in data:
            sale.year = data["year"]
        sale.save()
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or Book not found")
    return JsonResponse({
        "id": str(sale.id),
        "book": str(sale.book.id),
        "count": sale.count,
        "year": sale.year,
    })

@csrf_exempt
@require_http_methods(["DELETE"])
def sale_delete(request, sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
    except Sale.DoesNotExist:
        return HttpResponseNotFound("Sale not found")
    sale.delete()
    return JsonResponse({"result": "deleted"})

@csrf_exempt
@require_http_methods(["GET"])
def sale_detail(request, sale_id):
    try:
        sale = Sale.objects.get(id=sale_id)
    except Sale.DoesNotExist:
        return HttpResponseNotFound("Sale not found")
    data = {
        "id": str(sale.id),
        "book": str(sale.book.id) if sale.book else None,
        "count": sale.count,
        "year": sale.year,
    }
    return JsonResponse(data)