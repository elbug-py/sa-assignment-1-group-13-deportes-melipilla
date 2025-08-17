import swaggerUi from "swagger-ui-express";
import swaggerJsdoc from "swagger-jsdoc";
import { Application } from "express";
import path from "path";

export function setupSwagger(app: Application) {
  const options = {
    definition: {
      openapi: "3.0.0",
      info: {
        title: "Book Review API",
        version: "1.0.0",
      },
    },
    apis: [path.join(__dirname, "routes/*.ts")], // ✅ absolute path
  };

  const swaggerSpec = swaggerJsdoc(options);
  app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
}
