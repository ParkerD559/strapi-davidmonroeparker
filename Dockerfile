FROM strapi/strapi

COPY strapi-app/ /usr/src/api/strapi-app

WORKDIR /usr/src/api/strapi-app

RUN npm install