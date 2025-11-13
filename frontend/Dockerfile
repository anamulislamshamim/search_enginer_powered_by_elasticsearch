# Step 1: Build stage
FROM node:18-alpine AS build-stage

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the source code
COPY . .

# Build the Vue app for production
RUN npm run build


# Step 2: Production stage
FROM nginx:alpine AS production-stage

# Copy built files from the previous stage to Nginx's web directory
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Expose port 80 for the container
EXPOSE 80

# Start Nginx server
CMD ["nginx", "-g", "daemon off;"]