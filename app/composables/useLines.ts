/**
 * 多行标题：契约约定用 <br> 分隔，每一行包成一个 .ln 动画行（原型的 <span class="ln"><i>…</i></span>）。
 * 入参是已经过 ch() 的 html。
 */
export function splitLines(html: string): string[] {
  return html
    .split(/<br\s*\/?>/i)
    .map(line => line.trim())
    .filter(Boolean);
}

/** 去掉标签，给 aria-label 用 */
export function plainText(html: string): string {
  return html
    .replace(/<[^>]*>/g, "")
    .replace(/&amp;/g, "&")
    .replace(/&shy;/g, "")
    .replace(/&nbsp;/g, " ")
    .replace(/&#8217;|&rsquo;/g, "’")
    .trim();
}
