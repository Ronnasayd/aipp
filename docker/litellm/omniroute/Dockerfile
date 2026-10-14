FROM node:24-slim

RUN npm install -g omniroute

EXPOSE 20128 20129 20132

CMD ["omniroute", "serve", "--no-open", "--log", "--port", "20128"]
