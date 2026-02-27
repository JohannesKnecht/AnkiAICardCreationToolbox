import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    define: {
      // Use the production Cloud Run URL during tests unless VITE_USE_DEV_BACKEND is set.
      // This ensures real HTTP requests hit the deployed backend rather than localhost.
      'import.meta.env.DEV': JSON.stringify(process.env.VITE_USE_DEV_BACKEND === 'true'),
    },
    test: {
      environment: 'jsdom',
      exclude: [...configDefaults.exclude, 'e2e/**'],
      root: fileURLToPath(new URL('./', import.meta.url)),
    },
  }),
)
