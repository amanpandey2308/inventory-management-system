# ===================================
# Dockerfile for Inventory Management Frontend
# ===================================
# This is a multi-stage Docker build:
#   Stage 1 (build): Install dependencies and build the React app
#   Stage 2 (production): Serve the built files with Nginx
#
# Multi-stage builds keep the final image small because
# Node.js and node_modules are NOT included in the production image.
#
# How to build and run:
#   docker build -t inventory-frontend .
#   docker run -p 3000:80 inventory-frontend

# ---- Stage 1: Build the React app ----
FROM node:20-alpine AS build
WORKDIR /app

# Accept VITE_API_URL as a build argument
# This is passed from docker-compose.yml so the frontend
# knows where the backend API is located
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL

# Copy package files first (Docker layer caching)
# Dependencies are only re-installed when package.json changes
COPY package*.json ./
RUN npm ci

# Copy source code and build
COPY . .
RUN npm run build

# ---- Stage 2: Serve with Nginx ----
FROM nginx:alpine

# Copy built files from the build stage
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom nginx config for SPA routing
# Without this, refreshing on /products would return 404
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 (Nginx default)
EXPOSE 80

# Start Nginx in foreground mode
CMD ["nginx", "-g", "daemon off;"]
