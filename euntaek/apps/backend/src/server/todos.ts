import { createId } from "@paralleldrive/cuid2";
import { eq } from "drizzle-orm";
import { db } from "~/db";
import { todos } from "~/db/schema";

async function createTodo(userId: string, title: string, contents?: string) {
  try {
    const res = await db
      .insert(todos)
      .values({
        id: createId(),
        userId,
        title,
        contents,
        checked: false,
      })
      .returning();

    return {
      ok: true,
      data: res[0],
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function readTodos(userId: string) {
  try {
    const res = await db.select().from(todos).where(eq(todos.userId, userId));

    return {
      ok: true,
      data: res,
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function updateTodoChecked(todoId: string, checked: boolean) {
  try {
    await db
      .update(todos)
      .set({
        checked,
      })
      .where(eq(todos.id, todoId));

    return {
      ok: true,
      data: null,
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function updateTodoTitle(todoId: string, title: string) {
  try {
    await db
      .update(todos)
      .set({
        title,
      })
      .where(eq(todos.id, todoId));

    return {
      ok: true,
      data: null,
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function updateTodoContents(todoId: string, contents: string) {
  try {
    await db
      .update(todos)
      .set({
        contents,
      })
      .where(eq(todos.id, todoId));

    return {
      ok: true,
      data: null,
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function deleteTodo(todoId: string) {
  try {
    await db.delete(todos).where(eq(todos.id, todoId));

    return {
      ok: true,
      data: null,
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

export {
  createTodo,
  readTodos,
  updateTodoChecked,
  updateTodoTitle,
  updateTodoContents,
  deleteTodo,
};
