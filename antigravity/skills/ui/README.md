
# ⚡ Stitch Integration for Antigravity

This directory contains skills powered by [Google Stitch](https://stitch.withgoogle.com/).

## Configuration

To use these skills, you must configure your MCP client with the settings found in `antigravity/configs/mcp_config.json`.
The API Key has been secured in your `.env` file.

## Available Skills

### 📋 `design-md`
**Design System Extraction & Documentation**
- Analyzes existing Stitch projects.
- Extracts colors, typography, spacing, and layouts.
- Creates a semantic `DESIGN.md`.

### ⚛️ `react-components`
**Stitch → Production React Conversion**
- Transforms Stitch HTML output into scalable React components.
- Validates functional output.
- Maintains design token consistency.

### 🔄 `stitch-loop`
**Autonomous Multi-Page Website Generator**
- Generates complete multi-page websites.
- Organizes project files.
- Validates functionality.

### ✨ `enhance-prompt`
**Prompt Intelligence Engine**
- Optimizes prompts for Stitch generation.
- Injects UI/UX keywords and context.

### 🎥 `remotion`
**Automated App Walkthrough Videos**
- Generates professional showcase videos.
- Uses Remotion framework for smooth transitions.

### 🎨 `shadcn-ui`
**shadcn/ui Integration Expert**
- Guides integration of shadcn components.
- Optimization and best practices.

---
**Note:** These skills rely on the `stitch` MCP server. Ensure your `STITCH_API_KEY` is valid.
