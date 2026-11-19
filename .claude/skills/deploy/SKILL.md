---
name: deploy
description: 把 AURA 官网的改动发布到正式站（aurainstitute.com）。当用户说"发布""上线""推上去""deploy""部署""更新官网""发到测试站"时使用。
---

# 发布 AURA 官网到正式站

改动**合并到 `main` 后自动发布**到 <https://aurainstitute.com>（正式站，`www.` 跳转到裸域）。
你没有、也不需要任何服务器登录或密钥——发布只通过 GitHub 完成。

流程：**本地检查 → 提交到分支 → 提 PR → 合并到 main → 确认正式站真的更新了**。

> **合并即上线**：正式站没有单独的测试环境，合并前要确认改动是用户想发的。域名、证书、Nginx 不在这里做，不要尝试。

## 一、看清楚要发布什么

```bash
git status --short
```

```bash
git diff --stat
```

用人话告诉用户改了哪几页、改了什么，确认是他想发的。

## 二、本地检查（两个都要过）

```bash
pnpm typecheck
```

```bash
pnpm build
```

## 三、安全检查（公开仓库）

```bash
git diff | grep -nE '^\+.*(sk-|ghp_|gho_|AKIA|BEGIN [A-Z ]*PRIVATE KEY|172\.2[0-9]|192\.168)'
```

```bash
git status --short | grep -E '\.env'
```

命中就停下来问用户，不要提交。写死的图片已压缩、放在 `app/assets/img/`，写死的内容旁有 `CMS-TODO` 标记。

## 四、提交、提 PR

不要直接推 `main`：

```bash
git switch -c <分支名>
```

```bash
git add <改动的文件>
```

```bash
git commit -m "<一句话说清楚改了什么>"
```

```bash
git push -u origin <分支名>
```

```bash
gh pr create --fill
```

PR 上会自动跑「check」（类型检查 + 构建）。**合并由负责人做**；用户明确说"合并"时才执行：

```bash
gh pr merge --squash
```

## 五、确认正式站更新了（必须做）

合并后「Deploy to staging」自动开始，通常几分钟：

```bash
gh run list --workflow=deploy-staging.yml --limit 1
```

```bash
gh run watch
```

要看到 `completed success`。这个流程最后一步会一直等到服务器确实切换到这次的提交才算成功，所以成功就代表已上线。再核对一次：

```bash
curl -s https://aurainstitute.com/_deploy/status.json
```

`current` 应该等于 `git rev-parse origin/main`。然后打开改动过的页面看一眼。**流程成功、页面也看过了，才能说"发布成功"。**

## 失败了怎么办

- **「check」或构建失败**：`gh run view --log-failed` 看日志，修代码再推。
- **最后一步"等服务器切换"失败并打印了应用日志**：新版本在服务器上起不来，正式站**仍在运行上一个版本**。按日志修复后重新合并。
- **等了 15 分钟超时**：服务器的拉取任务可能没运行，不是代码问题，联系负责人。

## 回退

在 Actions 页面手动运行「Deploy to staging」，`ref` 填要回到的提交号；或：

```bash
gh workflow run deploy-staging.yml -f ref=<提交号>
```

要彻底撤销某次改动，另外提一个 revert 的 PR。

## 不要做的事

不要登录服务器、改 Nginx 或证书、改 `.github/workflows/`、改 Release「staging」里的文件，除非负责人同意。
