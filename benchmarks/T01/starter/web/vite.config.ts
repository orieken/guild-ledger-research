import { defineConfig } from 'vitest/config'
import vue from '@vitejs/plugin-vue'
export default defineConfig({ plugins: [vue()], server: {host:'0.0.0.0',port:5173,strictPort:true,proxy:{'/api':process.env.GUILD_PROXY_TARGET || 'http://localhost:18000'}}, test:{environment:'jsdom',setupFiles:['./tests/setup.ts']} })
