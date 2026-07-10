#!/usr/bin/env python3
"""Recover a minimal Hexo source tree from generated static blog files.

Inputs expected in current directory:
- search.xml
- posts/*.html

Outputs:
- recovered_source/
  - _config.yml
  - package.json
  - source/_posts/*.md
"""
from __future__ import annotations

import html
import json
import re
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SEARCH_XML = ROOT / "search.xml"
POSTS_DIR = ROOT / "posts"
OUT_DIR = ROOT / "recovered_source"


def slugify(name: str) -> str:
    name = name.strip().lower()
    name = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name or "post"


def parse_post_meta(html_text: str) -> dict[str, str]:
    meta = {}
    patterns = {
        "published": r'<meta property="article:published_time" content="([^"]+)"',
        "updated": r'<meta property="article:modified_time" content="([^"]+)"',
        "description": r'<meta name="description" content="([^"]*)"',
        "author": r'<meta property="article:author" content="([^"]+)"',
        "site_name": r'<meta property="og:site_name" content="([^"]+)"',
    }
    for key, pattern in patterns.items():
        m = re.search(pattern, html_text)
        meta[key] = html.unescape(m.group(1)).strip() if m else ""

    page_json_match = re.search(
        r'<script class="next-config" data-name="page" type="application/json">(.*?)</script>',
        html_text,
        re.S,
    )
    meta["page_title"] = ""
    if page_json_match:
        try:
            page_data = json.loads(page_json_match.group(1))
            meta["page_title"] = page_data.get("title", "")
        except json.JSONDecodeError:
            pass

    main_json_match = re.search(
        r'<script class="next-config" data-name="main" type="application/json">(.*?)</script>',
        html_text,
        re.S,
    )
    meta["main_config_json"] = main_json_match.group(1).strip() if main_json_match else ""
    return meta


def clean_html_content(raw_html: str) -> str:
    # Strip heading anchors injected by renderer.
    cleaned = re.sub(r'<a class="markdownIt-Anchor"[^>]*></a>\s*', "", raw_html)
    # Normalize blank lines around block tags for readability.
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()
    return cleaned


def write_root_files(main_config: dict, site_meta: dict[str, str]) -> None:
    (OUT_DIR / "source" / "_posts").mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "source" / "about").mkdir(parents=True, exist_ok=True)

    hostname = main_config.get("hostname", "example.com")
    site_title = site_meta.get("site_name") or hostname
    author = site_meta.get("author") or "Recovered"

    config = textwrap.dedent(
        f"""\
        title: "{site_title}"
        subtitle: ""
        description: ""
        author: "{author}"
        language: zh-CN
        timezone: Asia/Shanghai

        url: https://{hostname}
        root: {main_config.get('root', '/')}
        permalink: posts/:title.html

        theme: next

        # Local search (restored)
        search:
          path: search.xml
          field: post
          format: html
          limit: 10000

        index_generator:
          path: ''
          per_page: 10
          order_by: -date

        archive_generator:
          per_page: 10
          yearly: true
          monthly: true

        category_generator:
          per_page: 10

        tag_generator:
          per_page: 10
        """
    )
    (OUT_DIR / "_config.yml").write_text(config, encoding="utf-8")

    about = textwrap.dedent(
        """\
        ---
        title: about
        comments: true
        ---
        """
    )
    (OUT_DIR / "source" / "about" / "index.md").write_text(about, encoding="utf-8")

    package_json = {
        "name": "recovered-hexo-blog",
        "private": True,
        "hexo": {},
        "scripts": {
            "clean": "node node_modules/hexo-cli/bin/hexo clean",
            "build": "node node_modules/hexo-cli/bin/hexo generate",
            "server": "node node_modules/hexo-cli/bin/hexo server",
        },
        "dependencies": {
            "hexo": "^7.0.0",
            "hexo-cli": "^4.3.2",
            "hexo-generator-archive": "^2.0.0",
            "hexo-generator-category": "^2.0.0",
            "hexo-generator-index": "^3.0.0",
            "hexo-generator-tag": "^2.0.0",
            "hexo-generator-search": "^2.4.0",
            "hexo-renderer-marked": "^6.0.0",
            "hexo-renderer-stylus": "^3.0.1",
            "hexo-server": "^3.0.0",
            "hexo-theme-next": "8.19.1",
            "css": "^3.0.0",
        },
    }
    (OUT_DIR / "package.json").write_text(
        json.dumps(package_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    readme = textwrap.dedent(
        """\
        # Recovered Hexo Source / Hexo 源码恢复说明

        本目录由已生成的静态博客反向恢复而来，主要输入是 `search.xml` 和 `posts/*.html`。

        ## 恢复结果

        - `source/_posts/*.md`：文章源文件，包含恢复出的 front matter。
        - `source/about/index.md`：根据现有 `about/index.html` 补出的页面骨架。
        - `_config.yml`：Hexo 主配置，保留站点域名、固定链接、分页、归档、分类、标签和本地搜索配置。
        - `_config.next.yml`：NexT 主题的最小可用配置。
        - `package.json`：Hexo 7、NexT 8.19.1、本地搜索和常用 generator 依赖。

        ## Usage

        ```bash
        cd recovered_source
        npm install
        npm run build
        npm run server
        ```

        ## 详细恢复方法

        1. 确认静态站点类型：从 HTML 中的 `<meta name="generator" content="Hexo 7.0.0">`、`/js/config.js`、NexT 资源和 `search.xml` 判断该站由 Hexo + NexT 生成。
        2. 使用搜索索引枚举文章：解析 `search.xml` 的每个 `<entry>`，读取 `title`、`url`、`categories`、`tags`，得到全部文章列表和分类/标签。
        3. 使用文章 HTML 修复正文：`search.xml` 中的中文内容存在编码损坏风险，因此正文优先从 `posts/*.html` 的 `<div class="post-body" itemprop="articleBody">` 提取。
        4. 恢复 front matter：从文章页 `<meta property="article:published_time">`、`article:modified_time`、`article:tag`、页面 JSON 配置和搜索索引恢复 `title`、`date`、`updated`、`description`、`categories`、`tags`。
        5. 保留正文 HTML：生成的 HTML 不能可靠还原为原始 Markdown，尤其是表格、图片、代码块和渲染器插件语法；因此文章体以 HTML 形式放进 `.md`，这是 Hexo 可接受且最少丢失格式的方案。
        6. 重建 Hexo 工程：生成 `package.json`、`_config.yml`、`_config.next.yml` 和 `source/_posts`，安装依赖后即可 `hexo generate`。
        7. 重新生成搜索：配置 `hexo-generator-search` 输出 `search.xml`，恢复原站的本地搜索功能。

        ## 注意事项

        - Post bodies are preserved in HTML form inside Markdown files to avoid losing formatting.
        - Front matter fields (`title`, `date`, `updated`, `tags`, `categories`) are restored from static pages where possible.
        - Local search is configured via `hexo-generator-search`.
        - 原始 Markdown 的空行、引用风格、短代码插件源码和未发布草稿无法从静态产物 100% 还原。
        - 如果需要完全复刻公开页面，还需要手工补充评论系统、统计代码、CDN、社交链接等 NexT 主题细节配置。
        """
    )
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    next_config = textwrap.dedent(
        """\
        # Recovered NexT theme config, matched to the generated site as closely as possible.
        scheme: Muse
        darkmode: false

        menu:
          home: / || fa fa-home
          about: /about/ || fa fa-user
          tags: /tags/ || fa fa-tags
          categories: /categories/ || fa fa-th
          archives: /archives/ || fa fa-archive

        menu_settings:
          icons: true
          badges: false

        sidebar:
          position: left
          display: post
          padding: 18
          offset: 12

        avatar:
          url: /images/avatar.gif
          rounded: false
          rotated: false

        site_state: true

        social:
          GitHub: https://github.com/SuperYzs || fab fa-github
          E-Mail: mailto:yezhansheng10@gmail.com || fa fa-envelope
          StackOverflow: https://stackoverflow.com/users/23611701/zhansheng-ye || fab fa-stack-overflow
          Bilibili: https://space.bilibili.com/501729919 || fab fa-bilibili

        social_icons:
          enable: true
          icons_only: false
          transition: false

        toc:
          enable: true
          number: true
          wrap: false
          expand_all: false
          max_depth: 6

        codeblock:
          copy_button:
            enable: true
            show_result: true
          fold:
            enable: false
            height: 500

        motion:
          enable: true
          async: false
          transition:
            menu_item: fadeInDown
            post_block: fadeIn
            post_header: fadeInDown
            post_body: fadeInDown
            coll_header: fadeInLeft
            sidebar: fadeInUp

        pace:
          enable: true
          color: blue
          theme: minimal

        comments:
          style: tabs
          active:
          storage: true
          lazyload: false
          nav:

        gitalk:
          enable: true
          github_id: SuperYzs
          repo: BlogComments
          client_id: 5c08e4832554e7a517fd
          client_secret: 160583afd57209fe1f8cda60cf9114e369a13104
          admin_user: SuperYzs
          distraction_free_mode: true
          proxy: https://cors-anywhere.azm.workers.dev/https://github.com/login/oauth/access_token

        local_search:
          enable: true
          trigger: auto
          top_n_per_article: 1
          unescape: false
          preload: false

        vendors:
          internal: local
          plugins: cdnjs
        """
    )
    (OUT_DIR / "_config.next.yml").write_text(next_config, encoding="utf-8")


def main() -> None:
    if not SEARCH_XML.exists():
        raise SystemExit(f"Missing {SEARCH_XML}")

    tree = ET.parse(SEARCH_XML)
    root = tree.getroot()

    entries = root.findall("entry")
    main_config: dict = {}
    site_meta: dict[str, str] = {}

    for entry in entries:
        title = (entry.findtext("title") or "").strip()
        url = (entry.findtext("url") or "").strip()
        content_node = entry.find("content")
        content_html = content_node.text if content_node is not None and content_node.text else ""

        tags = [n.text.strip() for n in entry.findall("./tags/tag") if n.text and n.text.strip()]
        categories = [
            n.text.strip() for n in entry.findall("./categories/category") if n.text and n.text.strip()
        ]

        post_rel = url.lstrip("/")
        post_file = ROOT / post_rel
        meta = {"published": "", "updated": "", "description": "", "page_title": ""}
        if post_file.exists():
            html_text = post_file.read_text(encoding="utf-8", errors="ignore")
            meta = parse_post_meta(html_text)
            if not site_meta:
                site_meta = {
                    "site_name": meta.get("site_name", ""),
                    "author": meta.get("author", ""),
                }
            if not main_config and meta.get("main_config_json"):
                try:
                    main_config = json.loads(meta["main_config_json"])
                except json.JSONDecodeError:
                    main_config = {}

        post_title = meta.get("page_title") or title
        slug = post_rel.replace("posts/", "").replace(".html", "")
        filename = f"{slugify(post_title)}-{slug}.md"

        def esc(v: str) -> str:
            return v.replace('\\', '\\\\').replace('\"', '\\\"')

        fm = ["---"]
        fm.append(f'title: "{esc(post_title)}"')
        if meta.get("published"):
            fm.append(f'date: "{meta["published"]}"')
        if meta.get("updated"):
            fm.append(f'updated: "{meta["updated"]}"')
        if meta.get("description"):
            fm.append(f'description: "{esc(meta["description"])}"')
        if categories:
            fm.append("categories:")
            fm.extend([f"  - {c}" for c in categories])
        if tags:
            fm.append("tags:")
            fm.extend([f"  - {t}" for t in tags])
        fm.append("---")

        body = clean_html_content(content_html)
        markdown = "\n".join(fm) + "\n\n" + body + "\n"

        out_file = OUT_DIR / "source" / "_posts" / filename
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(markdown, encoding="utf-8")

    write_root_files(main_config, site_meta)
    print(f"Recovered {len(entries)} posts into {OUT_DIR}")


if __name__ == "__main__":
    main()
