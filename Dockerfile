# Dockerfile
FROM python:3.7-stretch

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential

ENV PORT 8080
ENV HOST 0.0.0.0

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app.py"]