import { Schema, model, Document } from "mongoose";

export interface IAuthor extends Document {
  name: string;
  date_of_birth: Date;
  country: string;
  description?: string;
}

const authorSchema = new Schema<IAuthor>({
  name: { type: String, required: true },
  date_of_birth: { type: Date, required: true },
  country: { type: String, required: true },
  description: { type: String, default: "" },
});

export default model<IAuthor>("Author", authorSchema);
