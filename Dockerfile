FROM flipperdevices/nginx-headers-more-alpine:1.25.1

WORKDIR /app

RUN apk update && apk add python3 py3-pip bash nginx

COPY requirements.txt ./
COPY app.py ./
COPY startup.sh ./
COPY nginx.conf /etc/nginx/nginx.conf

RUN python3 -m pip install -r requirements.txt

EXPOSE 80

CMD ["/bin/bash", "/app/startup.sh"]
