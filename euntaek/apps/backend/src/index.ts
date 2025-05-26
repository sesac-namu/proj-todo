import { logger } from "@bogeychan/elysia-logger";
import { swagger } from "@elysiajs/swagger";
import { Elysia, t } from "elysia";
import {
  createSession,
  createUser,
  generateToken,
  invalidateAllSessions,
  invalidateSession,
  login,
  validateSession,
} from "./server/auth";
import {
  createTodo,
  deleteTodo,
  readTodos,
  updateTodoChecked,
  updateTodoContents,
  updateTodoTitle,
} from "./server/todos";

const authService = new Elysia({ name: "Service.Auth" })
  .derive(
    {
      as: "scoped",
    },
    async ({ cookie: { session } }) => {
      if (!session) {
        return {
          session: null,
          user: null,
        };
      }

      const res = await validateSession(session.value!);

      if (res.ok) {
        const data = res.data;

        if (!data) {
          return {
            session: null,
            user: null,
          };
        }

        return data;
      } else {
        return {
          session: null,
          user: null,
        };
      }
    },
  )
  .macro(({ onBeforeHandle }) => ({
    // This is declaring a service method
    isSignIn(value: boolean) {
      if (!value) {
        return;
      }
      onBeforeHandle(({ user, status }) => {
        if (!user) {
          return status(401);
        }
      });
    },
  }));

const app = new Elysia()
  .use(
    logger({
      transport: {
        target: "pino-pretty",
      },
    }),
  )
  .use(swagger({ path: "/docs" }))
  .use(authService)
  .get("/", () => "Hello Elysia")
  .post(
    "/signup",
    async ({ body, status }) => {
      const res = await createUser(body.username, body.password, body.email);

      if (res.ok) {
        return status(200, {
          ok: true,
          data: res.data!,
        });
      } else {
        return status(400, {
          ok: false,
          error: "Cannot create user",
        });
      }
    },
    {
      body: t.Object({
        username: t.String(),
        password: t.String(),
        email: t.Optional(t.String()),
      }),
      isSignIn: false,
    },
  )
  .post(
    "/login",
    async ({ body, cookie: { session }, status }) => {
      const res = await login(body.username, body.password);

      if (!res.ok) {
        return status(400, res.error);
      }

      const user = res.data!;

      await invalidateAllSessions(user.id);

      const newToken = generateToken();
      const sessionRes = await createSession(newToken, user.id);

      if (!sessionRes.ok) {
        return status(400, res.error);
      }

      session.value = newToken;

      return {
        ok: true,
        data: {
          token: newToken,
        },
      };
    },
    {
      body: t.Object({
        username: t.String(),
        password: t.String(),
      }),
      cookie: t.Cookie({
        session: t.Optional(t.String()),
      }),
      isSignIn: false,
    },
  )
  .post(
    "/logout",
    async ({ cookie: { session: sessionCookie }, session, status }) => {
      await invalidateSession(session!.id);
      sessionCookie.value = null;
    },
    {
      cookie: t.Cookie({
        session: t.Nullable(t.String()),
      }),
      isSignIn: true,
    },
  )
  .get(
    "/todos/get",
    async ({ user, status }) => {
      const res = await readTodos(user!.id);

      console.log(res);

      if (!res.ok) {
        return status(400, res.error);
      }

      return res;
    },
    {
      isSignIn: true,
    },
  )
  .post(
    "/todos/create",
    async ({ body, user, status }) => {
      const res = await createTodo(user!.id, body.title, body.contents);

      if (!res.ok) {
        return status(400, res.error);
      }

      return res;
    },
    {
      body: t.Object({
        title: t.String(),
        contents: t.Optional(t.String()),
      }),
      isSignIn: true,
    },
  )
  .patch(
    "/todos/update/title/by_id/:id",
    async ({ body, params, status }) => {
      const res = await updateTodoTitle(params.id, body.title);

      if (!res.ok) {
        return status(400, res);
      }

      return res;
    },
    {
      body: t.Object({
        title: t.String(),
      }),
      params: t.Object({
        id: t.String(),
      }),
      isSignIn: true,
    },
  )
  .patch(
    "/todos/update/contents/by_id/:id",
    async ({ body, params, status }) => {
      const res = await updateTodoContents(params.id, body.contents);

      if (!res.ok) {
        return status(400, res);
      }

      return res;
    },
    {
      body: t.Object({
        contents: t.String(),
      }),
      params: t.Object({
        id: t.String(),
      }),
      isSignIn: true,
    },
  )
  .patch(
    "/todos/update/checked/by_id/:id",
    async ({ body, params, status }) => {
      const res = await updateTodoChecked(params.id, body.checked === "true");

      if (!res.ok) {
        return status(400, res);
      }

      return res;
    },
    {
      body: t.Object({
        checked: t.String(),
      }),
      params: t.Object({
        id: t.String(),
      }),
      isSignIn: true,
    },
  )
  .delete(
    "/todos/delete/by_id/:id",
    async ({ params, status }) => {
      const res = await deleteTodo(params.id);

      if (!res.ok) {
        return status(400, res);
      }

      return res;
    },
    {
      params: t.Object({
        id: t.String(),
      }),
      isSignIn: true,
    },
  )
  .listen(3000);

console.log(`🦊 Elysia is running at ${app.server?.url}`);
