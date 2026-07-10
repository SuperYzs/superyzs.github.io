# SuperYzs' Blog

这是 <https://superyzs.github.io/> 的 Hexo 源码仓库，使用 NexT 主题并通过 GitHub Actions 构建和部署到 GitHub Pages。

## 本地使用

需要 Node.js 20 或更高版本；持续集成使用 Node.js 22。

```bash
npm ci
npm run check
npm run server
```

- `npm run build`：生成站点到 `public/`。
- `npm run check`：清理、重新生成并检查历史 URL、搜索索引和站点地图。
- `npm run server`：在本地预览站点。

## 目录结构

- `source/_posts/`：文章源码；恢复文章为原样 HTML，新文章可使用 Markdown。
- `source/about/`、`source/404/`：独立页面。
- `source/images/`：站点静态图片。
- `_config.yml`：Hexo 配置。
- `_config.next.yml`：NexT 主题配置。
- `.github/workflows/pages.yml`：GitHub Pages 构建与部署流程。
- `build-tools/`：构建后检查和站点地图辅助脚本。
- `tools/recover_hexo_source.py`：从历史静态站点恢复源码时使用的留档工具。

## 发布流程

1. 在独立分支修改源码并运行 `npm run check`。
2. 创建 Draft Pull Request，等待人工审核。
3. 合并到 `main` 后，GitHub Actions 自动构建并部署 `public/`。

仓库不再提交生成后的 `public/` 内容。首次合并前，需要在 GitHub 仓库的 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。

## 源码恢复说明

当前文章由 2024 年发布的静态站点反向恢复。恢复文章使用带 front matter 的 `.html` 源文件，以原样保留代码块、表格、公式和图片布局。原始 Markdown 的空行、插件语法和未发布草稿无法从静态产物完整还原。
