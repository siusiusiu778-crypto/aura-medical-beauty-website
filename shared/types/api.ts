/** 与 docs/api-contract.md 一一对应。接口变化先改契约，再改这里。 */

export interface L10n {
  en?: string;
  zh?: string;
}

export interface Media {
  id: number;
  url: string;
  kind: "image" | "video";
  alt: L10n;
  width: number | null;
  height: number | null;
  posterUrl: string | null;
  /** CSS object-position，例如 "50% 45%" */
  focus?: string | null;
}

export interface Seo {
  title: L10n;
  description: L10n;
  keywords: L10n;
  ogImage: Media | null;
  noindex: boolean;
}

export interface PageContent {
  key: string;
  content: Record<string, unknown>;
  seo: Seo;
  updatedAt: string;
}

export interface NavTreatment {
  slug: string;
  name: L10n;
}

export interface NavGroup {
  name: L10n | null;
  treatments: NavTreatment[];
}

export interface NavCategory {
  key: string;
  name: L10n;
  tag: L10n | null;
  link: { type: "none" | "page" | "treatment"; target: string } | null;
  groups: NavGroup[];
}

export interface TreatmentSummary {
  slug: string;
  name: L10n;
  category: string;
  group: L10n | null;
  summary: L10n;
  card: Media | null;
  copyComplete: boolean;
}

export interface TreatmentDetail {
  slug: string;
  name: L10n;
  category: { key: string; name: L10n };
  group: L10n | null;
  summary: L10n;
  card: Media | null;
  content: Record<string, unknown>;
  seo: Seo;
  copyComplete: boolean;
  updatedAt: string;
  related: { slug: string; name: L10n; card: Media | null }[];
}

export interface GoalSummary {
  slug: string;
  name: L10n;
  summary: L10n;
  card: Media | null;
}

export interface GoalDetail extends GoalSummary {
  content: Record<string, unknown>;
  seo: Seo;
  treatments: { slug: string; name: L10n; summary: L10n; card: Media | null }[];
  updatedAt: string;
}

export interface SitemapData {
  pages: { key: string; updatedAt: string | null; noindex: boolean }[];
  treatments: { slug: string; updatedAt: string | null; noindex: boolean }[];
  goals: { slug: string; updatedAt: string | null }[];
}
