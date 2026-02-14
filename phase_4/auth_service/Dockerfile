# Use an official Node.js runtime as a parent image
FROM node:20-alpine

# Set the working directory in the container
WORKDIR /app

# Install app dependencies
# A wildcard is used to ensure both package.json and package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install

# Bundle app source
COPY . .

# Expose port (if your Node.js app listens on a specific port, e.g., 3000 or 8080)
# You might need to adjust this based on your actual application's port.
EXPOSE 3001

# Define the command to run your app
CMD [ "node", "better_auth_server.js" ]