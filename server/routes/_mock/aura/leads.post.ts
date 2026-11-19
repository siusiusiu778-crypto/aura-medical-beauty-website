/** 开发用 mock：只回成功，不保存（NUXT_MOCK_API=1 才存在） */
export default defineEventHandler(async event => {
  if (process.env.NUXT_MOCK_API !== "1") throw createError({ statusCode: 404 });
  const body = await readBody(event);
  console.log("[mock lead]", JSON.stringify(body));
  setResponseStatus(event, 201);
  return { status: "success", data: { id: 1 }, message: "" };
});
