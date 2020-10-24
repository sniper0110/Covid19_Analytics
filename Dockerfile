FROM python:3.8-slim

WORKDIR /usr/src/app

COPY . .

RUN pip install -r /usr/src/app/requirements.txt
RUN pip install --upgrade pip && pip install gunicorn

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 my_dashboard:flask_app