/** 页面键 → 官网路由（与 docs/api-contract.md §6 一致） */
export const PAGE_PATHS: Record<string, string> = {
  home: "/",
  about: "/about",
  membership: "/membership",
  "facial-blueprint": "/facial-blueprint",
  "journal-faq": "/journal/faq",
  "journal-botox-vs-xeomin": "/journal/botox-vs-xeomin"
};

export const pagePath = (key: string) => PAGE_PATHS[key] ?? "/";
export const treatmentPath = (slug: string) => `/treatments/${slug}`;
export const goalPath = (slug: string) => `/goals/${slug}`;
