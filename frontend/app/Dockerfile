# Build stage
FROM node:20-alpine as build-stage

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy project files
COPY . .

# Build the app
RUN npm run build

# Production stage
FROM nginx:stable-alpine as production-stage

# Install envsubst
RUN apk add --no-cache gettext

# Copy built files from build stage
COPY --from=build-stage /app/dist /usr/share/nginx/html

# Copy nginx configuration if you have any custom config
COPY nginx/nginx.conf /etc/nginx/templates/default.conf.template

# Use envsubst to process the template
CMD ["/bin/sh", "-c", "envsubst '${BACKEND_URL}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'"]
