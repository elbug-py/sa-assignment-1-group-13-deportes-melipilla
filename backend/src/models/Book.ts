import { Schema, model, Document } from "mongoose";

export interface IBook extends Document {
  name: string;
  summary: string;
  publication_date: Date;
  author: Schema.Types.ObjectId;
  total_sales: number;
}

const bookSchema = new Schema<IBook>({
  name: { type: String, required: true },
  summary: { type: String, required: true },
  publication_date: { type: Date, required: true },
  author: { type: Schema.Types.ObjectId, ref: "Author", required: true },
  total_sales: { type: Number, default: 0, min: 0 },
});

// Text index for full-text search
bookSchema.index({ name: "text", summary: "text" });

export default model<IBook>("Book", bookSchema);
