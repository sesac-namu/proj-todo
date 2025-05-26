import { defineConfig } from "drizzle-kit";
import "./compression-polyfill";

export default defineConfig({
  dialect: "sqlite",
  schema: "./src/db/schema.ts",
  dbCredentials: {
    url: "database.db",
  },
});
