import { Request, Response } from "express";
import Author from "../models/Author";

export const getAuthors = async (req: Request, res: Response) => {
  try {
    const authors = await Author.find();
    res.json(authors);
  } catch (err) {
    res.status(500).json({ error: "Failed to fetch authors" });
  }
};

export const createAuthor = async (req: Request, res: Response) => {
  try {
    const author = new Author(req.body);
    const saved = await author.save();
    res.status(201).json(saved);
  } catch (err) {
    res.status(400).json({ error: "Failed to create author" });
  }
};
