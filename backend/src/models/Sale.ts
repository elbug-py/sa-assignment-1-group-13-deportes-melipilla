import { Schema, model, Document } from "mongoose";

export interface ISale extends Document {
  book: Schema.Types.ObjectId;
  year: number;
  sales: number;
}

const saleSchema = new Schema<ISale>({
  book: { type: Schema.Types.ObjectId, ref: "Book", required: true },
  year: { type: Number, required: true },
  sales: { type: Number, required: true, min: 0 },
});

export default model<ISale>("Sale", saleSchema);
