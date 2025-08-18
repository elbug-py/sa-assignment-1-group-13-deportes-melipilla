# Core API Documentation

This API provides CRUD operations for Authors, Books, Reviews, and Sales using Django and MongoDB (mongoengine).

## Base URL

All endpoints are prefixed with `/api/` (e.g., `http://localhost:8000/api/authors/`).

---

## Endpoints

### Authors

- **List all authors**
  - `GET /api/authors/`
- **Create a new author**
  - `POST /api/authors/new/`
  - Body:
    ```json
    {
      "name": "Author Name",
      "birthday": "YYYY-MM-DD",
      "origin_country": "Country",
      "description": "Bio"
    }
    ```
- **Get author by ID**
  - `GET /api/authors/<author_id>/`
- **Edit author**
  - `PUT /api/authors/<author_id>/edit/`
  - Body: same as creation, fields optional
- **Delete author**
  - `DELETE /api/authors/<author_id>/delete/`

---

### Books

- **List all books**
  - `GET /api/books/`
- **Create a new book**
  - `POST /api/books/new/`
  - Body:
    ```json
    {
      "author": "<author_id>",
      "name": "Book Title",
      "summary": "Summary",
      "publication_date": "YYYY-MM-DD"
    }
    ```
- **Get book by ID**
  - `GET /api/books/<book_id>/`
- **Edit book**
  - `PUT /api/books/<book_id>/edit/`
  - Body: same as creation, fields optional
- **Delete book**
  - `DELETE /api/books/<book_id>/delete/`

---

### Reviews

- **List all reviews**
  - `GET /api/reviews/`
- **Create a new review**
  - `POST /api/reviews/new/`
  - Body:
    ```json
    {
      "book": "<book_id>",
      "score": 5,
      "up_votes": 10
    }
    ```
- **Get review by ID**
  - `GET /api/reviews/<review_id>/`
- **Edit review**
  - `PUT /api/reviews/<review_id>/edit/`
  - Body: same as creation, fields optional
- **Delete review**
  - `DELETE /api/reviews/<review_id>/delete/`

---

### Sales

- **List all sales**
  - `GET /api/sales/`
- **Create a new sale**
  - `POST /api/sales/new/`
  - Body:
    ```json
    {
      "book": "<book_id>",
      "count": 100,
      "year": 2024
    }
    ```
- **Get sale by ID**
  - `GET /api/sales/<sale_id>/`
- **Edit sale**
  - `PUT /api/sales/<sale_id>/edit/`
  - Body: same as creation, fields optional
- **Delete sale**
  - `DELETE /api/sales/<sale_id>/delete/`

---

## Notes

- All POST and PUT requests require `Content-Type: application/json`.
- Replace `<author_id>`, `<book_id>`, `<review_id>`, `<sale_id>` with actual IDs from your database.
- All endpoints return JSON responses.

---

**See the main project README for Docker