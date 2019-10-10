FROM node
RUN npm install -g http-server
# make the 'app' folder the current working directory
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
CMD [ "http-server", "dist" ]
