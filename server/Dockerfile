FROM python
COPY . /var/app
RUN apt-get update
RUN apt-get install -y locales
RUN rm -rf /var/lib/apt/lists/*
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
RUN pip3 install -r /var/app/requirements.txt
WORKDIR /var/app
CMD ["python3" ,"main.py"]
