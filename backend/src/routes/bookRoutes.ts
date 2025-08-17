import { Router } from "express";
import {
  getBooks,
  createBook,
  getBookById,
  updateBook,
  deleteBook,
} from "../controllers/bookController";

const router = Router();

/**
 * @swagger
 * tags:
 *   name: Books
 *   description: Book management
 */

/**
 * @swagger
 * /api/books:
 *   get:
 *     summary: Get all books
 *     tags: [Books]
 *     responses:
 *       200:
 *         description: List of books
 *   post:
 *     summary: Create a new book
 *     tags: [Books]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               summary:
 *                 type: string
 *               publication_date:
 *                 type: string
 *                 format: date
 *               author:
 *                 type: string
 *               description:
 *                 type: string
 *               total_sales:
 *                 type: number
 *     responses:
 *       201:
 *         description: Book created
 */

/**
 * @swagger
 * /api/books/{id}:
 *   get:
 *     summary: Get a book by ID
 *     tags: [Books]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The book ID
 *     responses:
 *       200:
 *         description: Book data
 *       404:
 *         description: Book not found
 *   put:
 *     summary: Update a book by ID
 *     tags: [Books]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The book ID
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               summary:
 *                 type: string
 *               publication_date:
 *                 type: string
 *                 format: date
 *               author:
 *                 type: string
 *               description:
 *                 type: string
 *               total_sales:
 *                 type: number
 *     responses:
 *       200:
 *         description: Book updated
 *       404:
 *         description: Book not found
 *   delete:
 *     summary: Delete a book by ID
 *     tags: [Books]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: string
 *         description: The book ID
 *     responses:
 *       200:
 *         description: Book deleted
 *       404:
 *         description: Book not found
 */

/**
 * @swagger
 * /api/books/author/{authorId}:
 *   get:
 *     summary: Get books by author ID
 *     tags: [Books]
 *     parameters:
 *       - in: path
 *         name: authorId
 *         required: true
 *         schema:
 *           type: string
 *         description: The author ID
 *     responses:
 *       200:
 *         description: List of books by the author
 */

/**
 * @swagger
 * /api/books/search:
 *   get:
 *     summary: Search books by query
 *     tags: [Books]
 *     parameters:
 *       - in: query
 *         name: q
 *         required: true
 *         schema:
 *           type: string
 *         description: The search query
 *     responses:
 *       200:
 *         description: List of books matching the query
 *       404:
 *         description: No books found
 */

/**
 * @swagger
 * /api/books/top-sales:
 *   get:
 *     summary: Get top 5 books by total sales
 *     tags: [Books]
 *     responses:
 *       200:
 *         description: List of top 5 books by total sales
 */

router.get("/", getBooks);
router.post("/", createBook);
router.get("/:id", getBookById);
router.put("/:id", updateBook);
router.delete("/:id", deleteBook);

export default router;
