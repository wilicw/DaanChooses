FROM node:13-alpine AS build
WORKDIR /app
ADD cli/package.json .
RUN npm install
ADD cli .
RUN npm run build

FROM python:alpine
COPY --from=build /tmp/dist /app/cli/dist
WORKDIR /app/server
ADD server/requirements.txt .
RUN python3 -m pip install -r requirements.txt
ADD server .
CMD ["python3", "main.py"]
