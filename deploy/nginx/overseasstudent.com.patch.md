> **状态：已撤除（2026-11-19）。** AURA 已迁到正式域名 `aurainstitute.com`，下面的四行与片段文件已按第四节撤除，原站点配置与接入前一致。本文留作记录。

# 对原站点 `overseasstudent.com` 配置的改动（接入、撤除、核对）

对应 `docs/refactor-plan.md` 第 5、7 节。本文是变更记录与操作规程，不是部署源；内网地址、主机名、目录以 `<占位>` 表示，真实值只在服务器上。

## 一、改动范围（只有这一处，约 4 行）

原站点文件：`<nginx 目录>/sites.d/www.overseasstudent.com.conf`，在 **443 端口、`server_name overseasstudent.com;` 的那个 server 块**里，紧跟 `server_name` 之后加入：

```nginx
    # AURA-BEGIN 子目录 /aura-institute/（见 aura-institute.location.conf）
    if ($uri ~ ^/aura-institu[dt]e) { break; }
    include <nginx 目录>/aura/aura-institute.location.conf;
    # AURA-END
```

- 第一行 `if … break`：原站点在 server 级有一串 `rewrite`（例如把几乎所有不存在的路径改写到 WordPress 的 `/index.php`），它们在 location 匹配**之前**执行；`break` 让这些 rewrite 对 AURA 路径直接跳过。写法与 uswoo.com 已有的接口放行行相同。
- 第二行：把我们自己的 location 片段整体引入。片段文件放在 `<nginx 目录>/aura/`，**不能**放进 `sites.d/`（那里是 http 级自动 include）。
- 不改 `www.overseasstudent.com` 的 301 块、不改证书、不改 `nginx.conf`、不动其他站点文件、不动 WordPress 目录。

## 二、接入前（每次改动前都要做，因为这个文件会被别人修改）

```bash
# 1 重新读取最新内容，确认没有别人刚改过、也确认 AURA-BEGIN 还不存在
grep -n "AURA-BEGIN" <nginx 目录>/sites.d/www.overseasstudent.com.conf
stat -c '%y %U:%G %a' <nginx 目录>/sites.d/www.overseasstudent.com.conf

# 2 备份（带时间戳，放在 backup/，不要放进 sites.d/）
cp -p <nginx 目录>/sites.d/www.overseasstudent.com.conf <nginx 目录>/backup/www.overseasstudent.com.conf.$(date +%Y%m%d-%H%M%S).pre-aura

# 3 基线：记录原站点现状（状态码与关键响应头）
bash wp-baseline.sh overseasstudent.com > /root/aura-baseline-before.txt
```

基线覆盖：首页、`/wp-login.php`、`/wp-admin/`、`/robots.txt`、`/favicon.ico`、一个 WordPress 静态资源、一个不存在的路径，以及 `/aura-institute/`（接入前应是 WordPress 的 404）。

## 三、接入

1. 把 `aura-institute.location.conf` 安装到 `<nginx 目录>/aura/`（把 `<Vectra 内网地址>`、`<Vectra 后端主机名>` 换成真实值）。
2. 在原站点文件里加入第一节的四行。
3. `nginx -t`，通过后 `nginx -s reload`（平滑重载，不断开连接）。**`nginx -t` 失败就还原备份，不要重载。**
4. 立即核对：

```bash
bash wp-baseline.sh overseasstudent.com > /root/aura-baseline-after.txt
diff /root/aura-baseline-before.txt /root/aura-baseline-after.txt
```

期望：差异**只出现在** `/aura-institute/`、`/aura-institude/` 两段；其余全部一致。AURA 容器尚未启动时 `/aura-institute/` 返回 502 属正常。

## 四、撤除（换正式域名、过渡期满后；对应方案第 7 节第 5 步）

```bash
# 1 重新读取并备份当前文件
cp -p <nginx 目录>/sites.d/www.overseasstudent.com.conf <nginx 目录>/backup/www.overseasstudent.com.conf.$(date +%Y%m%d-%H%M%S).pre-remove
# 2 删除 AURA-BEGIN 到 AURA-END 之间（含两行标记）
sed -i '/# AURA-BEGIN/,/# AURA-END/d' <nginx 目录>/sites.d/www.overseasstudent.com.conf
# 3 检查、平滑重载
nginx -t && nginx -s reload
# 4 删除片段
rm <nginx 目录>/aura/aura-institute.location.conf
```

然后核对原域名恢复：

```bash
# 与接入前备份比较：应当没有任何 AURA 相关差异（他人的无关改动除外）
diff <nginx 目录>/backup/www.overseasstudent.com.conf.<接入前时间戳>.pre-aura <nginx 目录>/sites.d/www.overseasstudent.com.conf
grep -rn "aura" <nginx 目录>/sites.d/www.overseasstudent.com.conf   # 应无输出
bash wp-baseline.sh overseasstudent.com > /root/aura-baseline-final.txt
diff /root/aura-baseline-before.txt /root/aura-baseline-final.txt     # 只剩 /aura-institute/ 两段（此时都是 WordPress 404）
```

## 五、回滚（任意一步出问题）

把接入前的备份放回、`nginx -t`、`nginx -s reload`。AURA 容器停掉（`docker stop aura-institute`）不影响任何其他站点。

## 六、过渡期的旧入口

换正式域名后到撤除前，把片段里的 ④（应用本体）改成 301 到新域名同路径，保留约 30 天，让已分享出去的测试链接继续可用；期满后按第四节撤除。
