import { encodeBase32LowerCaseNoPadding } from "@oslojs/encoding";
import { createId } from "@paralleldrive/cuid2";
import { eq } from "drizzle-orm";
import { db } from "~/db";
import { sessions, users } from "~/db/schema";
import { hash, verify } from "~/lib/password";

function sha3_512(data: string) {
  const hasher = new Bun.CryptoHasher("sha3-512");

  hasher.update(data);
  const hash = hasher.digest("base64");

  return hash;
}

function generateToken() {
  const bytes = new Uint8Array(20);
  crypto.getRandomValues(bytes);
  const token = encodeBase32LowerCaseNoPadding(bytes);

  return token;
}

async function createUser(
  username: string,
  password: string,
  email: string = "",
) {
  try {
    const res = await db
      .insert(users)
      .values({
        id: createId(),
        passwordHash: await hash(password),
        username,
        email,
      })
      .returning();

    if (res.length === 0) {
      return { ok: false, error: "User already exists" };
    }

    return {
      ok: true,
      data: {
        id: res[0]!.id,
        username: res[0]!.username,
        email: res[0]!.email,
        createdAt: res[0]!.createdAt,
        updatedAt: res[0]!.updatedAt,
      },
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function updateUserPassword(userId: string, password: string) {
  try {
    const res = await db
      .update(users)
      .set({
        passwordHash: await hash(password),
      })
      .where(eq(users.id, userId))
      .returning();

    if (res.length === 0) {
      return { ok: false, error: "User not found" };
    }

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

async function updateUserEmail(userId: string, email: string) {
  try {
    const res = await db
      .update(users)
      .set({
        email,
      })
      .where(eq(users.id, userId))
      .returning();

    if (res.length === 0) {
      return { ok: false, error: "User not found" };
    }

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

async function login(username: string, password: string) {
  try {
    const res = await db
      .select()
      .from(users)
      .where(eq(users.username, username));

    const user = res[0];

    if (!user) {
      return { ok: false, error: "Invalid username or password" };
    }

    const hashed = await verify(password, user.passwordHash);

    if (!hashed) {
      return { ok: false, error: "Invalid username or password" };
    }

    return {
      ok: true,
      data: {
        id: user.id,
        username: user.username,
        email: user.email,
        createdAt: user.createdAt,
        updatedAt: user.updatedAt,
      },
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function createSession(token: string, userId: string) {
  try {
    const res = await db
      .insert(sessions)
      .values({
        id: sha3_512(token),
        userId,
      })
      .returning();

    if (res.length === 0) {
      return { ok: false, error: "Session already exists" };
    }

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

async function validateSession(token: string) {
  try {
    const res = await db
      .select({
        user: users,
        session: sessions,
      })
      .from(sessions)
      .innerJoin(users, eq(sessions.userId, users.id))
      .where(eq(sessions.id, sha3_512(token)));

    if (res.length === 0) {
      return {
        ok: true,
        data: {
          session: null,
          user: null,
        },
      };
    }

    const { session, user } = res[0]!;

    if (Date.now() >= session.expiresAt.getTime() - 1000 * 6 * 60 * 24 * 3.5) {
      session.expiresAt = new Date(Date.now() + 1000 * 60 * 60 * 24 * 7);

      await db
        .update(sessions)
        .set({
          expiresAt: session.expiresAt,
        })
        .where(eq(sessions.id, session.id));
    }

    return {
      ok: true,
      data: {
        session,
        user,
      },
    };
  } catch (e) {
    return {
      ok: false,
      error: e,
    };
  }
}

async function invalidateSession(sessionId: string) {
  try {
    await db.delete(sessions).where(eq(sessions.id, sessionId));

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

async function invalidateAllSessions(userId: string) {
  try {
    await db.delete(sessions).where(eq(sessions.userId, userId));

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
  createUser,
  updateUserEmail,
  updateUserPassword,
  login,
  createSession,
  validateSession,
  invalidateSession,
  invalidateAllSessions,
  generateToken,
  sha3_512,
};
