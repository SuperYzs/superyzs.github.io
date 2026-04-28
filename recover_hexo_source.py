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


def write_root_files(main_config: dict) -> None:
    (OUT_DIR / "source" / "_posts").mkdir(parents=True, exist_ok=True)

    config = textwrap.dedent(
        f"""\
        title: "{main_config.get('hostname', 'Recovered Blog')}"
        subtitle: ""
        description: "Recovered from generated static files"
        author: "Recovered"
        language: zh-CN
        timezone: UTC

        url: https://{main_config.get('hostname', 'example.com')}
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

    package_json = {
        "name": "recovered-hexo-blog",
        "private": True,
        "scripts": {
            "clean": "hexo clean",
            "build": "hexo generate",
            "server": "hexo server",
        },
        "dependencies": {
            "hexo": "^7.0.0",
            "hexo-generator-archive": "^2.0.0",
            "hexo-generator-category": "^2.0.0",
            "hexo-generator-index": "^3.0.0",
            "hexo-generator-tag": "^2.0.0",
            "hexo-generator-search": "^2.4.0",
            "hexo-renderer-marked": "^6.0.0",
            "hexo-server": "^3.0.0",
            "hexo-theme-next": "^8.19.1",
        },
    }
    (OUT_DIR / "package.json").write_text(
        json.dumps(package_json, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    readme = textwrap.dedent(
        """\
        # Recovered Hexo Source

        This directory is reconstructed from generated static files (`search.xml` + `posts/*.html`).

        ## Usage

        ```bash
        cd recovered_source
        npm install
        npm run build
        npm run server
        ```

        ## Notes

        - Post bodies are preserved in HTML form inside Markdown files to avoid losing formatting.
        - Front matter fields (`title`, `date`, `updated`, `tags`, `categories`) are restored from static pages where possible.
        - Local search is configured via `hexo-generator-search`.
        """
    )
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    next_config = textwrap.dedent(
        """\
        # Recovered NexT theme config (minimal)
        local_search:
          enable: true
          trigger: auto
          top_n_per_article: 1
          unescape: false
          preload: false

        menu:
          home: / || fa fa-home
          about: /about/ || fa fa-user
          tags: /tags/ || fa fa-tags
          categories: /categories/ || fa fa-th
          archives: /archives/ || fa fa-archive
          search: /search/ || fa fa-search
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

    write_root_files(main_config)
    print(f"Recovered {len(entries)} posts into {OUT_DIR}")


if __name__ == "__main__":
    main()
