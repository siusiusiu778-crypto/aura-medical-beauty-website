/**
 * 标题、段落里允许的少量内联标记。先整体转义，再只把白名单里的标记还原，
 * 所以内容里即使混入其他 HTML 也只会被当成文字显示。
 */
const ALLOWED = [
  /&lt;br\s*\/?&gt;/g,
  /&lt;span&gt;/g,
  /&lt;\/span&gt;/g,
  /&lt;(?:em|strong|b|i|ul|ol|li|p)&gt;/g,
  /&lt;\/(?:em|strong|b|i|ul|ol|li|p|a)&gt;/g,
  /&lt;a href=&quot;(?:https?:\/\/|\/|#|mailto:|tel:)(?:(?!&quot;|&lt;|&gt;)[\s\S])*&quot;(?: target=&quot;_blank&quot;)?(?: rel=&quot;noopener&quot;)?&gt;/g
];

export function escapeHtml(text: string): string {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
}

export function richHtml(text: string): string {
  let html = escapeHtml(text);
  for (const pattern of ALLOWED) {
    html = html.replace(pattern, match => match.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"'));
  }
  // 内容里本来就写成实体的字符（&amp; &shy; &nbsp; &#8217; 等）被转义成了 &amp;amp; 之类，还原回实体：实体只会变成一个字符，不会引入标签
  return html.replace(/&amp;(?=(?:amp|lt|gt|quot|shy|nbsp|mdash|ndash|hellip|rsquo|lsquo|ldquo|rdquo|reg|trade|copy|middot|bull|times|deg|#\d{1,6}|#x[0-9a-fA-F]{1,5});)/g, "&");
}
