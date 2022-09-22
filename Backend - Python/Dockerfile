FROM python:3.10
ENV TZ="Asia/Ho_Chi_Minh"

RUN mkdir /code
WORKDIR /code

COPY requirements.txt setup.py tox.ini ./
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN pip install -e .

ADD  application application/
COPY application application/
COPY migrations migrations/

EXPOSE 7777
