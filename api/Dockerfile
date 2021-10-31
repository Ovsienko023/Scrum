FROM python:3.8

RUN mkdir -p /usr/src/api/
WORKDIR /usr/src/api/

COPY . /usr/src/api/

RUN pip install -r requirements.txt

EXPOSE 8888

CMD ["python", "__main__.py"]
