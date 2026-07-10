import { readFile, writeFile } from 'node:fs/promises';

const sitemapPath = new URL('../public/sitemap.xml', import.meta.url);
const outputPath = new URL('../public/sitemap.txt', import.meta.url);
const sitemap = await readFile(sitemapPath, 'utf8');
const urls = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map((match) => match[1]);

if (urls.length === 0) {
  throw new Error('No URLs were found in public/sitemap.xml');
}

await writeFile(outputPath, `${urls.join('\n')}\n`, 'utf8');
console.log(`Generated sitemap.txt with ${urls.length} URLs.`);
