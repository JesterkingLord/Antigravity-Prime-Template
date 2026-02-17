# ⚠️ This file is deprecated. Please check package.json for the latest version.

# SvelteKit project (JavaScript)

This template should help you get started developing with SvelteKit in Vite.

## Recommended IDE Setup

[VS Code](https://code.visualstudio.com/) + [Svelte](https://marketplace.visualstudio.com/items?itemName=svelte.svelte-vscode).

## Antigravity Template Features

This frontend is configured to work with the Antigravity Master Template backend.

- **API Connection**: Pre-configured to talk to `http://localhost:8000/api`
- **Skill Manager**: UI components to view and manage skills.
- **Chat Interface**: Interact with your agent via `Chat.svelte`.

## Developing

Once you've installed dependencies with `npm install` (or `pnpm install` or `yarn`), start a development server:

```bash
npm run dev
# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of your app:

```bash
npm run build
```

## Docker Deployment

To build and run in production mode with Docker:

```bash
docker build -t antigravity-frontend .
docker run -p 3000:3000 antigravity-frontend
```
