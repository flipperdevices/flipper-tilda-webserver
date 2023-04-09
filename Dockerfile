FROM nginx:1.23.4-alpine

WORKDIR /app

COPY requirements.txt ./
COPY app.py ./
COPY startup.sh ./
COPY nginx.conf /etc/nginx/nginx.conf

RUN apk update && apk add python3 py3-pip
RUN python3 -m pip install -r requirements.txt

EXPOSE 80

CMD ["/bin/sh", "/app/startup.sh"]
