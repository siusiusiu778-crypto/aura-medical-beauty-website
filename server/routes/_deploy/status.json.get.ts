import { readFile } from "node:fs/promises";

/**
 * 发布状态：拉取脚本把每次尝试的结果写到挂载进容器的状态文件，这里原样公布，
 * 发布流程读它来确认新版本是否已经切换。文件路径来自 NUXT_STATUS_FILE（默认 /status/status.json）。
 * 只含提交号、时间、成败和报错，不含密钥。
 */
export default defineEventHandler(async (event) => {
  setHeader(event, "Cache-Control", "no-store");
  setHeader(event, "Content-Type", "application/json; charset=utf-8");
  const file = process.env.NUXT_STATUS_FILE || "/status/status.json";
  try {
    return await readFile(file, "utf8");
  } catch {
    // 第一次发布之前文件还不存在：返回空状态，发布流程会继续等待
    return JSON.stringify({ current: "", lastAttempt: null });
  }
});
