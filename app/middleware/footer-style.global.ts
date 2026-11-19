/** 每次路由切换先把页脚恢复成完整版；需要原型里那种一行简版页脚的页面在自己的 setup 里调用 useFooterStyle(true) */
export default defineNuxtRouteMiddleware(() => {
  useState<boolean>("footer-simple", () => false).value = false;
});
