# Flipper Tilda Exporter

## General
This application forked from [tilda-static-page-exporter](https://github.com/FallenChromium/tilda-static-page-exporter) repository and contains some changes:
1. Added Nginx to serve static files
2. Added custom js, css and images paths reading from Tilda

## This application does
1. Handles Tilda's site export webhook via [Tilda's API](https://help.tilda.cc/api)
2. Exports all site files to specified directory
3. Serves this files via Nginx

## How to use
1. Generate API credentials (Tilda's Dashboard->Site Settings->API Integration->Generate new API keys)
2. Add webhook URL on same page ([YOUR SERVER IP OR HOSTNAME]/webhook)
3. Start applicaton in docker
    ```bash
    docker run --rm -d -p 80:80 \
        -e "TILDA_PUBLIC_KEY=[YOUR PUBLIC KEY]" \
        -e "TILDA_SECRET_KEY=[YOUR SECRET KEY]" \
        -e 'TILDA_STATIC_PATH_PREFIX=/static' \
        -v [YOUR STATIC FILES DIRECTORY]:/static \
        flipperdevices/flipper-tilda-webserver:latest
    ```
4. Make some chages on your site and type 'Publish'. Your site will be avaliabe on your server in a few minnutes
