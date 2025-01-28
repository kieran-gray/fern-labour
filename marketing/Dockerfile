# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG BACKEND_API_URL
ARG INSTAGRAM_URL

ENV NEXT_PUBLIC_BACKEND_API_URL=${BACKEND_API_URL}
ENV NEXT_PUBLIC_INSTAGRAM_URL=${INSTAGRAM_URL}

RUN npm run build

# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM alpine

RUN apk add brotli nginx nginx-mod-http-brotli

COPY --from=build-stage /app/out/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/http.d/default.conf

EXPOSE 81
CMD ["nginx", "-g", "daemon off;"]
