FROM python:3.8
WORKDIR /usr/src/bot
COPY . .
COPY requirements.txt requiremenets.txt
RUN pip3 install -r requirements.txt