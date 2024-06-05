FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . /app
RUN mkdir -p /app/static/images

CMD ["python", "run.py"]