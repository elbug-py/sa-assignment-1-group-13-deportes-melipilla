import mongoose from "mongoose";
import dotenv from "dotenv";
import Author from "../models/Author";
import Book from "../models/Book";
import Review from "../models/Review";
import Sale from "../models/Sale";
import { faker } from "@faker-js/faker";

dotenv.config();

async function seed(): Promise<void> {
  try {
    await mongoose.connect(process.env.MONGO_URI || "");

    console.log("⚡ Clearing old data...");
    await Author.deleteMany({});
    await Book.deleteMany({});
    await Review.deleteMany({});
    await Sale.deleteMany({});

    console.log("⚡ Seeding Authors...");
    const authors = [];
    for (let i = 0; i < 50; i++) {
      authors.push(
        new Author({
          name: faker.person.fullName(),
          date_of_birth: faker.date.birthdate({
            min: 1950,
            max: 1995,
            mode: "year",
          }),
          country: faker.location.country(),
          description: faker.lorem.sentence(),
        }),
      );
    }
    const savedAuthors = await Author.insertMany(authors);

    console.log("⚡ Seeding Books + Reviews + Sales...");
    for (let i = 0; i < 300; i++) {
      const author = faker.helpers.arrayElement(savedAuthors);

      const book = await Book.create({
        name: faker.lorem.words(3),
        summary: faker.lorem.paragraph(),
        publication_date: faker.date.past({ years: 30 }),
        author: author._id,
        total_sales: 0, // will update later
      });

      // Reviews (1–10 per book)
      const reviews = [];
      const numReviews = faker.number.int({ min: 1, max: 10 });
      for (let j = 0; j < numReviews; j++) {
        reviews.push({
          book: book._id,
          review: faker.lorem.sentence(),
          score: faker.number.int({ min: 1, max: 5 }),
          up_votes: faker.number.int({ min: 0, max: 5000 }),
        });
      }
      await Review.insertMany(reviews);

      // Sales (5 years)
      let totalSales = 0;
      const currentYear = new Date().getFullYear();
      for (let y = 0; y < 5; y++) {
        const yearSales = faker.number.int({ min: 1000, max: 100000 });
        totalSales += yearSales;
        await Sale.create({
          book: book._id,
          year: currentYear - y,
          sales: yearSales,
        });
      }

      // Update total_sales on book
      book.total_sales = totalSales;
      await book.save();
    }

    console.log("✅ Seeding complete!");
    mongoose.connection.close();
  } catch (err) {
    console.error("❌ Seeding error:", err);
    process.exit(1);
  }
}

seed();
