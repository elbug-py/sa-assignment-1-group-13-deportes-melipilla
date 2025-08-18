from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from core.models import Review, Book


@csrf_exempt
@require_http_methods(["GET"])
def review_list(request):
    reviews = Review.objects.all()
    data = [
        {
            "id": str(review.id),
            "book": str(review.book.id) if review.book else None,
            "score": review.score,
            "up_votes": review.up_votes,
        }
        for review in reviews
    ]
    return JsonResponse({"reviews": data})


@csrf_exempt
@require_http_methods(["POST"])
def review_create(request):
    import json
    try:
        data = json.loads(request.body)
        book_id = data.get("book")
        score = data.get("score")
        up_votes = data.get("up_votes", 0)
        book = Book.objects.get(id=book_id)
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or Book not found")

    review = Review(book=book, score=score, up_votes=up_votes)
    review.save()
    return JsonResponse({
        "id": str(review.id),
        "book": str(review.book.id),
        "score": review.score,
        "up_votes": review.up_votes,
    }, status=201)


@csrf_exempt
@require_http_methods(["PUT"])
def review_edit(request, review_id):
    import json
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review not found")
    try:
        data = json.loads(request.body)
        if "book" in data:
            review.book = Book.objects.get(id=data["book"])
        if "score" in data:
            review.score = data["score"]
        if "up_votes" in data:
            review.up_votes = data["up_votes"]
        review.save()
    except Exception:
        return HttpResponseBadRequest("Invalid JSON or Book not found")
    return JsonResponse({
        "id": str(review.id),
        "book": str(review.book.id),
        "score": review.score,
        "up_votes": review.up_votes,
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def review_delete(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review not found")
    review.delete()
    return JsonResponse({"result": "deleted"})


@csrf_exempt
@require_http_methods(["GET"])
def review_detail(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return HttpResponseNotFound("Review not found")
    data = {
        "id": str(review.id),
        "book": str(review.book.id) if review.book else None,
        "score": review.score,
        "up_votes": review.up_votes,
    }
    return JsonResponse(data)