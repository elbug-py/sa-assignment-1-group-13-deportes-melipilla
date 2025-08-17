import { Router } from "express";
import { getAuthors, createAuthor } from "../controllers/authorController";

const router = Router();

/**
 * @swagger
 * tags:
 *   name: Authors
 *   description: Author management
 */

/**
 * @swagger
 * /api/authors:
 *   get:
 *     summary: Get all authors
 *     tags: [Authors]
 *     responses:
 *       200:
 *         description: List of authors
 *   post:
 *     summary: Create a new author
 *     tags: [Authors]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               name:
 *                 type: string
 *               date_of_birth:
 *                 type: string
 *                 format: date
 *               country:
 *                 type: string
 *               description:
 *                 type: string
 *     responses:
 *       201:
 *         description: Author created
 */
router.get("/", getAuthors);
router.post("/", createAuthor);

export default router;
