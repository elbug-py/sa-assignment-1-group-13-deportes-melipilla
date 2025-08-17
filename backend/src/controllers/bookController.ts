import { Request, Response } from "express";
import Book from "../models/Book";

export const getBooks = async (req: Request, res: Response) => {
  try {
    const books = await Book.find().populate("author");
    res.json(books);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch books" });
  }
};

export const createBook = async (req: Request, res: Response) => {
  try {
    const book = new Book(req.body);
    const saved = await book.save();
    res.status(201).json(saved);
  } catch (err) {
    res.status(400).json({ error: "Failed to create book" });
  }
};

export const getBookById = async (req: Request, res: Response) => {
  try {
    const book = await Book.findById(req.params.id).populate("author");
    if (!book) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json(book);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch book" });
  }
};

export const updateBook = async (req: Request, res: Response) => {
  try {
    const updated = await Book.findByIdAndUpdate(req.params.id, req.body, {
      new: true,
    });
    if (!updated) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json(updated);
  } catch (err) {
    res.status(400).json({ error: "Failed to update book" });
  }
};

export const deleteBook = async (req: Request, res: Response) => {
  try {
    const deleted = await Book.findByIdAndDelete(req.params.id);
    if (!deleted) {
      return res.status(404).json({ error: "Book not found" });
    }
    res.json({ message: "Book deleted" });
  } catch (err) {
    res.status(500).json({ error: "Failed to delete book" });
  }
};

export const getBooksByAuthor = async (req: Request, res: Response) => {
  try {
    const books = await Book.find({ author: req.params.authorId }).populate(
      "author",
    );
    res.json(books);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch books by author" });
  }
};
