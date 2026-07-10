import { access, readFile, readdir } from 'node:fs/promises';
import path from 'node:path';

const root = path.resolve('public');
const requiredPaths = [
  'index.html',
  '404/index.html',
  'about/index.html',
  'categories/index.html',
  'tags/index.html',
  'archives/index.html',
  'search.xml',
  'sitemap.xml',
  'sitemap.txt',
  'BingSiteAuth.xml',
  'googleb76ba8f1d755a8d4.html'
];

const expectedPostIds = [
  '179be3c4', '1e2dafef', '2947dde5', '362c9816', '3ed4a3d8',
  '4a597bff', '54097cbd', '5d65ccb7', '5dcef6ef', '609cd352',
  '661cdd66', '692a9f79', '8e92b27e', 'a127f116', 'b73b57f4',
  'c46c9d0d', 'cd002d07', 'e6e6ac69', 'f99582e8'
];

for (const relativePath of requiredPaths) {
  await access(path.join(root, relativePath));
}

for (const id of expectedPostIds) {
  await access(path.join(root, 'posts', `${id}.html`));
}

const generatedPosts = (await readdir(path.join(root, 'posts')))
  .filter((name) => name.endsWith('.html'));
if (generatedPosts.length !== expectedPostIds.length) {
  throw new Error(`Expected ${expectedPostIds.length} posts, found ${generatedPosts.length}.`);
}

const homepage = await readFile(path.join(root, 'index.html'), 'utf8');
const searchIndex = await readFile(path.join(root, 'search.xml'), 'utf8');
const sitemap = await readFile(path.join(root, 'sitemap.xml'), 'utf8');

for (const marker of ["SuperYzs'Blog", '/archives/', '/categories/', '/tags/']) {
  if (!homepage.includes(marker)) throw new Error(`Homepage is missing ${marker}`);
}

for (const id of expectedPostIds) {
  if (!searchIndex.includes(`/posts/${id}.html`)) {
    throw new Error(`search.xml is missing post ${id}`);
  }
  if (!sitemap.includes(`/posts/${id}.html`)) {
    throw new Error(`sitemap.xml is missing post ${id}`);
  }
}

console.log(`Verified ${generatedPosts.length} posts and ${requiredPaths.length} required site files.`);
