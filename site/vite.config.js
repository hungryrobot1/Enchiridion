import { defineConfig } from 'vite';
import { execSync } from 'child_process';

export default defineConfig({
  root: '.',
  base: '/Enchiridion/',
  publicDir: 'public',
  build: {
    outDir: '../docs',
    emptyOutDir: true,
  },
  plugins: [
    {
      name: 'build-text-index',
      buildStart() {
        execSync('node scripts/build-index.js', { stdio: 'inherit' });
      },
    },
  ],
});
