# Stage 0, "build-stage", based on Node.js, to build and compile the frontend
FROM node:20 AS build-stage

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG NEXT_PUBLIC_FRONTEND_URL
ARG NEXT_PUBLIC_CONTACT_SERVICE_URL
ARG NEXT_PUBLIC_INSTAGRAM_URL
ARG NEXT_PUBLIC_CLOUDFLARE_SITEKEY

ENV NEXT_PUBLIC_FRONTEND_URL=${NEXT_PUBLIC_FRONTEND_URL}
ENV NEXT_PUBLIC_CONTACT_SERVICE_URL=${NEXT_PUBLIC_CONTACT_SERVICE_URL}
ENV NEXT_PUBLIC_INSTAGRAM_URL=${NEXT_PUBLIC_INSTAGRAM_URL}
ENV NEXT_PUBLIC_CLOUDFLARE_SITEKEY=${NEXT_PUBLIC_CLOUDFLARE_SITEKEY}

RUN npm run build

# Stage 1, based on alpine, to have only the compiled app, ready for production with Nginx
FROM alpine

RUN apk add brotli nginx nginx-mod-http-brotli

COPY --from=build-stage /app/out/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/http.d/default.conf

EXPOSE 81
CMD ["nginx", "-g", "daemon off;"]
