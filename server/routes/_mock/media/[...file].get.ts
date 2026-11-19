import { existsSync, statSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { basename, extname, resolve } from "node:path";

const TYPES: Record<string, string> = { ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".webp": "image/webp", ".mp4": "video/mp4", ".svg": "image/svg+xml" };

/** 开发用 mock：把 mediaKey 对应的文件从 legacy/site 读出来（NUXT_MOCK_API=1 才存在）。只取文件名，不允许路径穿越。 */
export default defineEventHandler(async event => {
  if (process.env.NUXT_MOCK_API !== "1") throw createError({ statusCode: 404 });
  const name = basename(String(getRouterParam(event, "file") ?? ""));
  const file = resolve(process.cwd(), "legacy/site", name);
  const type = TYPES[extname(name).toLowerCase()];
  if (!type || !existsSync(file) || !statSync(file).isFile()) throw createError({ statusCode: 404 });
  setHeader(event, "content-type", type);
  setHeader(event, "cache-control", "public, max-age=3600");
  return readFile(file);
});
