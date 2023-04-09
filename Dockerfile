FROM python:3.11-alpine3.17

WORKDIR /app

RUN apk update && apk add python3 py3-pip bash nginx

COPY requirements.txt ./
COPY app.py ./
COPY startup.sh ./
COPY nginx.conf /etc/nginx/nginx.conf

RUN python3 -m pip install -r requirements.txt

EXPOSE 80

CMD ["/bin/bash", "/app/startup.sh"]
