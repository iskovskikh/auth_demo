

    # Use Node.js as the base image
    FROM node:25.9.0-alpine

    # Set working directory
    WORKDIR /app

    # Copy package files and install dependencies with Yarn
    COPY package.json yarn.lock ./
    RUN yarn install

    # Copy the rest of the application code
    COPY . .

    # Start the application
    CMD ["yarn", "run", "dev", "--host", "0.0.0.0"]