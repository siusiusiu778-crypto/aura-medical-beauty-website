/** 页脚样式：目标页、Journal、占位治疗页在原型里用的是一行简版页脚（site.footer.simple.text），其余页面用完整页脚 */
export function useFooterStyle(simple: boolean) {
  useState<boolean>("footer-simple", () => false).value = simple;
}
