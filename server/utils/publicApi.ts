import type { H3Event } from "h3";

/**
 * 服务端路由里请求公开接口（站点地图等）。与页面里的 useApi 走同一组地址：
 * 配了内网基址就直连 Vectra 后端，否则走 public.apiBase（本地 mock 时是站内路径）。
 */
export async function publicApi<T>(event: H3Event, path: string): Promise<T> {
  const config = useRuntimeConfig(event);
  const serverBase = String(config.apiBaseServer || "");
  const publicBase = String(config.public.apiBase);
  const base = (serverBase || publicBase).replace(/\/$/, "");
  const headers: Record<string, string> = {};
  if (serverBase && config.apiHostHeader) headers.host = String(config.apiHostHeader);
  // 站内路径（mock）走本进程内部请求
  const target = base.startsWith("http") ? `${base}${path}` : `${base}${path}`;
  const response = await $fetch<{ status: string; data: T; message?: string }>(target, { headers, timeout: 10000 });
  if (response?.status !== "success") throw createError({ statusCode: 502, statusMessage: response?.message || "Upstream error" });
  return response.data;
}
