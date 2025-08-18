from django.shortcuts import render
from django.core.paginator import Paginator
from core.services import get_top_rated_books, get_authors_table, get_top_selling_books
from mongoengine.queryset.visitor import Q 
from core.services import search_books_by_summary 
from urllib.parse import urlencode

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

def top_rated(request):
    ctx = {"items": get_top_rated_books()}
    return render(request, "tables/topRated.html", ctx)

def search_books(request):
    q = (request.GET.get("q") or "").strip()
    qs = search_books_by_summary(q)
    paginator = Paginator(list(qs), 20)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "search.html", {"q": q, "page_obj": page_obj})

def top_selling(request):
    ctx = {"items": get_top_selling_books()}
    return render(request, "tables/topSelling.html", ctx)
