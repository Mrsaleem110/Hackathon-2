FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM node:18-alpine

WORKDIR /app

COPY --from=build /app/dist ./dist
COPY package*.json ./
# Only copy necessary files for running, not development dependencies
COPY --from=build /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "run", "preview"]