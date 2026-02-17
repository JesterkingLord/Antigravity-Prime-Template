
# 🎨 Antigravity Frontend Dockerfile

# Build Stage
FROM node:18-alpine AS builder

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production Stage (Lightweight Serve)
FROM node:18-alpine

WORKDIR /app
# Copy built assets from builder
COPY --from=builder /app/build ./build
COPY --from=builder /app/package.json ./package.json

# Install minimal prod dependencies
RUN npm install --production

# Expose Port for SvelteKit (usually 3000 in prod, but let's stick to 5173 for consistency or change to 3000)
ENV PORT=3000
EXPOSE 3000

# Start Node Server
CMD ["node", "build"]
