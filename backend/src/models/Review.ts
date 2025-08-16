import { Schema, model, Document } from "mongoose";

export interface IReview extends Document {
  book: Schema.Types.ObjectId;
  score: number;
  up_votes: number;
}

const reviewSchema = new Schema<IReview>({
  book: { type: Schema.Types.ObjectId, ref: "Book", required: true },
  score: { type: Number, required: true, min: 1, max: 5 },
  up_votes: { type: Number, default: 0 },
});

export default model<IReview>("Review", reviewSchema);
