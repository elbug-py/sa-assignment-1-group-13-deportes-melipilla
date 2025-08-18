
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from core.models import Author


@csrf_exempt
@require_http_methods(["GET"])
def author_list(request):
    authors = Author.objects.all()
    data = [
        {
            "id": str(author.id),
            "name": author.name,
            "birthday": author.birthday,
            "origin_country": author.origin_country,
            "description": author.description,
        }
        for author in authors
    ]
    return JsonResponse({"authors": data})


@csrf_exempt
@require_http_methods(["POST"])
def author_create(request):
    import json
    try:
        data = json.loads(request.body)
        name = data.get("name")
        birthday = data.get("birthday")
        origin_country = data.get("origin_country")
        description = data.get("description")
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    author = Author(name=name, birthday=birthday, origin_country=origin_country, description=description)
    author.save()
    return JsonResponse({
        "id": str(author.id),
        "name": author.name,
        "birthday": author.birthday,
        "origin_country": author.origin_country,
        "description": author.description,
    }, status=201)


@csrf_exempt
@require_http_methods(["PUT"])
def author_edit(request, author_id):
    import json
    author = get_object_or_404(Author, id=author_id)
    try:
        data = json.loads(request.body)
        author.name = data.get("name", author.name)
        author.birthday = data.get("birthday", author.birthday)
        author.origin_country = data.get("origin_country", author.origin_country)
        author.description = data.get("description", author.description)
        author.save()
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")
    return JsonResponse({
        "id": str(author.id),
        "name": author.name,
        "birthday": author.birthday,
        "origin_country": author.origin_country,
        "description": author.description,
    })


@csrf_exempt
@require_http_methods(["DELETE"])
def author_delete(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    author.delete()
    return JsonResponse({"result": "deleted"})
