#!/bin/bash
# 原站点基线：接入 AURA 前后各跑一次，两份输出 diff 应当只有 /aura-institute/ 相关行不同。
# 在目标服务器本机运行；不改任何东西，只发几个 GET 请求并记录状态码与关键响应头。
#
# 用法：wp-baseline.sh <原域名> > baseline-before.txt     （接入后：> baseline-after.txt，再 diff）
set -uo pipefail
HOST=${1:?用法：wp-baseline.sh <原域名>}
PATHS=(
  "/"
  "/wp-login.php"
  "/wp-admin/"
  "/robots.txt"
  "/favicon.ico"
  "/wp-includes/js/jquery/jquery.min.js"
  "/aura-baseline-not-exist-$(date +%Y)"
  "/aura-institute/"
  "/aura-institude/"
)
for p in "${PATHS[@]}"; do
  echo "== $p"
  # --resolve 直连本机 443，不经过 CDN/DNS；-D- 输出响应头，去掉每次都会变的头
  curl -sk -o /dev/null -m 15 -D- --resolve "$HOST:443:127.0.0.1" "https://$HOST$p" \
    | tr -d '\r' | grep -i -E '^(HTTP/|location:|content-type:|cache-control:|x-robots-tag:|set-cookie:|x-powered-by:|server:|link:)' \
    | sed -E 's/(set-cookie: [^=]+)=[^;]*/\1=<value>/I' | sort
done
