import { Router } from "express";
import Author from "../models/Author";
import Book from "../models/Book";
import Review from "../models/Review";

const router = Router();

// Author CRUD
router.get("/authors", async (req, res) => {
  const authors = await Author.find();
  res.json(authors);
});

router.get("/authors/:id", async (req, res) => {
  const author = await Author.findById(req.params.id);
  if (!author) return res.status(404).send("Author not found");
  res.json(author);
});

router.post("/authors", async (req, res) => {
  const author = new Author(req.body);
  await author.save();
  res.status(201).json(author);
});

router.put("/authors/:id", async (req, res) => {
  const author = await Author.findByIdAndUpdate(req.params.id, req.body, { new: true });
  if (!author) return res.status(404).send("Author not found");
  res.json(author);
});

router.delete("/authors/:id", async (req, res) => {
  const author = await Author.findByIdAndDelete(req.params.id);
  if (!author) return res.status(404).send("Author not found");
  res.json(author);
});

// Book CRUD
router.get("/books", async (req, res) => {
  const books = await Book.find();
  res.json(books);
});

router.get("/books/:id", async (req, res) => {
  const book = await Book.findById(req.params.id);
  if (!book) return res.status(404).send("Book not found");
  res.json(book);
});

router.post("/books", async (req, res) => {
  const book = new Book(req.body);
  await book.save();
  res.status(201).json(book);
});

router.put("/books/:id", async (req, res) => {
  const book = await Book.findByIdAndUpdate(req.params.id, req.body, { new: true });
  if (!book) return res.status(404).send("Book not found");
  res.json(book);
});

router.delete("/books/:id", async (req, res) => {
  const book = await Book.findByIdAndDelete(req.params.id);
  if (!book) return res.status(404).send("Book not found");
  res.json(book);
});

// Review CRUD
router.get("/reviews", async (req, res) => {
  const reviews = await Review.find();
  res.json(reviews);
});

router.get("/reviews/:id", async (req, res) => {
  const review = await Review.findById(req.params.id);
  if (!review) return res.status(404).send("Review not found");
  res.json(review);
});

router.post("/reviews", async (req, res) => {
  const review = new Review(req.body);
  await review.save();
  res.status(201).json(review);
});

router.put("/reviews/:id", async (req, res) => {
  const review = await Review.findByIdAndUpdate(req.params.id, req.body, { new: true });
  if (!review) return res.status(404).send("Review not found");
  res.json(review);
});

router.delete("/reviews/:id", async (req, res) => {
  const review = await Review.findByIdAndDelete(req.params.id);
  if (!review) return res.status(404).send("Review not found");
  res.json(review);
});

export default router;