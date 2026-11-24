// A working news-image-daily entry (Node 22, standard library only): its image is the entry.png beside this file, and
// the program copies it to /output/entry.png. A starting point, not a winner: replace the image. The gate takes a
// whole PNG or JPEG of at most 1 MiB and 1024 by 1024 pixels, and the judge sees exactly the bytes copied.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

// --- validation added for this entry -------------------------------------
// Before anything is copied, confirm the image beside this file really is
// the artefact the gate expects: a PNG of exactly 1024x1024 pixels and no
// larger than 1 MiB. Failing loudly here beats shipping a broken entry.
const MAX_BYTES = 1_048_576; // 1 MiB gate limit
const EXPECTED = 1024; // gate requires a 1024x1024 image
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

const sourcePath = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(sourcePath);

for (let i = 0; i < PNG_MAGIC.length; i += 1) {
  if (bytes[i] !== PNG_MAGIC[i]) {
    throw new Error('entry.png is not a PNG file (bad signature)');
  }
}

// A PNG stores its pixel dimensions as big-endian uint32s in the IHDR
// chunk, at byte offsets 16 (width) and 20 (height).
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== EXPECTED || height !== EXPECTED) {
  throw new Error(`entry.png is ${width}x${height}, expected ${EXPECTED}x${EXPECTED}`);
}

const size = statSync(sourcePath).size;
if (size > MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the ${MAX_BYTES}-byte limit`);
}

const destination = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');
copyFileSync(sourcePath, destination);
console.log(`copied entry.png (${width}x${height}, ${size} bytes) to ${destination}`);
