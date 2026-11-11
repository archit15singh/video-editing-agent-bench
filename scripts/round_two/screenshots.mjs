// Render the code-native fictitious product screens; no live service data.
import sharp from 'sharp';import fs from 'node:fs';
const directory='results/round-two/media';
for(const f of fs.readdirSync(directory).filter(x=>x.endsWith('.svg')))await sharp(`${directory}/${f}`).png().toFile(`${directory}/${f.replace('.svg','.png')}`);
