FROM python:3.8
WORKDIR /code
COPY ./app /code
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt