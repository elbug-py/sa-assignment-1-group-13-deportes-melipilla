from .author_views import (
    author_list,
    author_create,
    author_edit,
    author_delete,
    author_detail,
)

from .book_views import (
    book_list,
    book_create,
    book_edit,
    book_delete,
    book_detail,
)

from .review_views import (
    review_list,
    review_create,
    review_edit,
    review_delete,
    review_detail,
)

from .sale_views import (
    sale_list,
    sale_create,
    sale_edit,
    sale_delete,
    sale_detail,
)

from .elastic_views import (
    search_books_view,
    search_authors_view,
    search_reviews_view,
    search_sales_view,
)
