// News-image entry for 24 November 2026 (Node 22, standard library only).
// The image is drawn by draw.py and shipped beside this file; the program
// simply places a copy of it where the grader expects it.
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

if (!existsSync(source)) {
  throw new Error('entry.png is missing next to main.ts');
}
mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
console.log('wrote entry.png to ' + outDir);
