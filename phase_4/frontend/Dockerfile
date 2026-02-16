FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Accept build arguments for environment variables
ARG VITE_API_BASE_URL
ARG VITE_AUTH_BASE_URL

# Set environment variables during build
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL
ENV VITE_AUTH_BASE_URL=$VITE_AUTH_BASE_URL

RUN npm run build

EXPOSE 3000

CMD ["npm", "run", "preview", "--", "--port", "3000", "--host", "0.0.0.0"]
