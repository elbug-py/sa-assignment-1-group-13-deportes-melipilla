import swaggerUi from "swagger-ui-express";
import swaggerJsdoc from "swagger-jsdoc";
import { Application } from "express";

export function setupSwagger(app: Application) {
  const options = {
    definition: {
      openapi: "3.0.0",
      info: {
        title: "Book Review API",
        version: "1.0.0",
      },
    },
    apis: ["./src/routes/*.ts"], // you can document routes with JSDoc comments
  };

  const swaggerSpec = swaggerJsdoc(options);

  app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
}
