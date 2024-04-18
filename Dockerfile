FROM python:3.12

WORKDIR /app

ADD requirements.txt .
RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "run.py"]