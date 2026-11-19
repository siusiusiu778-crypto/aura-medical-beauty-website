/**
 * 界面功能性文案（表单校验与提交状态、无障碍标签）：模板里直接写英文。页面内容全部来自 CMS，见 usePageContent。
 * 首发只有英文站；双语内容（L10n）按 en 取，en 缺失时回退 zh。
 */
export function useTx() {
  const tx = (english: string) => english;
  /** 双语内容取英文；缺了回退中文 */
  const bi = (value: { en?: string; zh?: string } | null | undefined): string => (value ? value.en || value.zh || "" : "");
  return { tx, bi };
}
