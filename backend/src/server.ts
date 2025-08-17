import express, { Application, Request, Response } from "express";
import apiRouter from "./routes/api";
import mongoose from "mongoose";
import { setupSwagger } from "./swagger";
import cors from "cors";
import morgan from "morgan";
import dotenv from "dotenv";

dotenv.config();

const app: Application = express();

// Middleware
app.use(cors());
app.use(express.json());
app.use(morgan("dev"));

// Test route
app.get("/", (req: Request, res: Response): void => {
  res.send("📚 Book Review API (TS) is running 🚀");
});

// API routes
app.use("/api", apiRouter);

// Mongo connection
mongoose
  .connect(process.env.MONGO_URI || "")
  .then((): void => {
    console.log("✅ MongoDB connected");
    app.listen(process.env.PORT || 3000, (): void => {
      console.log(`🚀 Server running on port ${process.env.PORT || 3000}`);
    });
  })
  .catch((err: ErrorEvent): void => console.error("❌ MongoDB error:", err));

// Swagger setup
setupSwagger(app);
