# Stage 1: Build the app
FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

# Inject build-time environment variables
ARG VUE_APP_API
ARG VUE_APP_WSGLOBALCHAT
ARG VUE_APP_WSROOMCHAT
ARG VUE_APP_WSROOM
ARG VUE_APP_SSOLINK

ENV VUE_APP_API=$VUE_APP_API
ENV VUE_APP_WSGLOBALCHAT=$VUE_APP_WSGLOBALCHAT
ENV VUE_APP_WSROOMCHAT=$VUE_APP_WSROOMCHAT
ENV VUE_APP_WSROOM=$VUE_APP_WSROOM
ENV VUE_APP_SSOLINK=$VUE_APP_SSOLINK

COPY . .
RUN rm -f .env
RUN npm run build

# ────────────────────────────────────────────────
# Stage 2: Serve with Nginx
FROM nginx:alpine

# Copy built Vue app to Nginx's web root
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 and run Nginx in the foreground
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]