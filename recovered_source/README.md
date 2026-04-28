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
