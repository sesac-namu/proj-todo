import { password as bunPassword } from "bun";

const algorithm: Parameters<typeof bunPassword.hash>[1] = {
  algorithm: "argon2id",
  memoryCost: 4,
  timeCost: 3,
};

async function hash(password: string) {
  return await bunPassword.hash(password, algorithm);
}

async function verify(password: string, hash: string) {
  return await bunPassword.verify(password, hash, "argon2id");
}

export { hash, verify };
