# Blog management rules

- This repository contains the Hexo source for <https://superyzs.github.io/>.
- Edit source files only. Never manually edit or commit generated files under `public/`.
- Posts belong in `source/_posts/` and must include title, date, categories, tags, and an explicit stable `permalink`.
- Preserve existing post URLs. Do not rename or remove a permalink unless the user explicitly requests a redirect or deletion.
- Before proposing changes, run `npm ci` and `npm run check`.
- Verify the homepage, the changed post, category/tag indexes, `search.xml`, `sitemap.xml`, and `sitemap.txt`.
- Preserve the site identity, analytics, comment configuration, publication dates, categories, and tags unless explicitly asked to change them.
- Keep credentials out of new files and logs. Use GitHub repository secrets for any new private values.
- Work on a separate branch and create a draft pull request. Never push directly to `main` or merge without explicit user approval.
- Keep dependency updates narrow and include the resulting `package-lock.json` changes.
