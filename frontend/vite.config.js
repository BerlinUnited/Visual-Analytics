import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';

// Determine if we are building for Electron or Web based on an environment variable
// This is crucial for Vite to know which entry point to use.
const isElectron = process.env.VITE_APP_TARGET === 'electron';

export default defineConfig({
    plugins: [react()],
    // Set the root directory for Vite based on the target.
    // This tells Vite where to find the index.html for the dev server
    // and how to resolve paths starting with '/' in your HTML/JS files.
    root: isElectron ? 'electron/renderer' : 'web', // NEW: Dynamically sets the root for the dev server

    // Define base path for assets. For Electron, it's relative. For web, it's absolute.
    base: isElectron ? './' : '/',

    resolve: {
        alias: {
            // Alias for shared components to simplify imports
            '@shared': resolve(__dirname, 'shared'),
            // Alias for web-specific code
            '@web': resolve(__dirname, 'web'),
            // Alias for electron-specific code
            '@electron': resolve(__dirname, 'electron'),
        },
    },

    build: {
        // Output directory for the built files
        outDir: isElectron ? '../dist/electron' : '../dist/web',

        rollupOptions: {
            input: {
                // Define entry points based on the target
                main: resolve(__dirname, isElectron ? 'electron/renderer/index.html' : 'web/index.html'),
            },
            output: {
                // Ensure consistent naming for built assets
                assetFileNames: 'assets/[name].[ext]',
                chunkFileNames: 'assets/[name].[hash].js',
                entryFileNames: 'assets/[name].[hash].js',
            },
        },
        // For production builds, enable minification
        minify: 'esbuild',
        // Generate sourcemaps for easier debugging
        sourcemap: true,
    },

    server: {
        // Port for the development server
        port: 3000,
        // Open browser automatically for web development
        open: !isElectron,
        // Proxy API requests if you have a separate backend API
        proxy: {
            '/api': 'http://localhost:8000', // Example for Django backend
        },
    },
});
