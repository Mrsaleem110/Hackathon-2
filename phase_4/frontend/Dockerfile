FROM node:18-alpine AS builder

WORKDIR /app

# Accept build arguments
ARG VITE_API_BASE_URL=http://localhost:8000
ARG VITE_AUTH_URL=http://localhost:3001
ARG VITE_MCP_SERVER_URL=http://localhost:8001

# Set as environment variables for the build
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_AUTH_URL=$VITE_AUTH_URL
ENV VITE_MCP_SERVER_URL=$VITE_MCP_SERVER_URL

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
