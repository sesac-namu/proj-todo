import { int, sqliteTable, text } from "drizzle-orm/sqlite-core";

const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  username: text("username").unique(),
  passwordHash: text("password_hash").notNull(),
  email: text("email").default(""),
  createdAt: int("created_at", { mode: "timestamp" }).default(new Date()),
  updatedAt: int("updated_at", { mode: "timestamp" }).default(new Date()),
});

type User = typeof users.$inferSelect;

const sessions = sqliteTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("user_id").references(() => users.id),
  expiresAt: int("expires_at", { mode: "timestamp" })
    .notNull()
    .default(new Date(Date.now() + 1000 * 60 * 60 * 24 * 7)),
});

type Session = typeof sessions.$inferSelect;

const todos = sqliteTable("todos", {
  id: text("id").primaryKey(),
  userId: text("user_id").references(() => users.id),
  title: text("title").notNull(),
  contents: text("contents"),
  checked: int("checked", { mode: "boolean" }).default(false),
  createdAt: int("created_at", { mode: "timestamp" }).default(new Date()),
  updatedAt: int("updated_at", { mode: "timestamp" }).default(new Date()),
});

type Todo = typeof todos.$inferSelect;

export { users, sessions, todos, type User, type Session, type Todo };
