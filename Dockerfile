FROM python:3.12

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install -y nano

COPY . /app

CMD ["python", "run.py"]