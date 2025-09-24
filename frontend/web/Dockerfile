# syntax=docker/dockerfile:1
FROM node:20-alpine
WORKDIR /app
COPY package*.json /app/
RUN npm ci
COPY . /app
ENV VITE_API_BASE=${VITE_API_BASE}
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host"]
