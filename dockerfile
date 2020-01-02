FROM nikolaik/python-nodejs:latest

COPY server /var/app/server/
COPY cli/ /var/app/cli/

WORKDIR /var/app/cli
RUN yarn install
RUN yarn build

WORKDIR /var/app/server
RUN python3 -m pip install -r requirements.txt

CMD ["python3", "main.py"]