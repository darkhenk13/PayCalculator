FROM python:3.10-alpine as build
COPY . .
RUN apk update
RUN apk --no-cache add build-base linux-headers && rm -rf /var/cache/apk/* && rm -rf /tmp/*
RUN pip install --no-cache-dir -r requirements.txt && rm -rf /var/cache/apk/*

#FROM python:3.10-alpine
#COPY --from=build . .
FROM python:3.10-alpine
RUN apk add --update --no-cache python3 %% apk add --update py-pip %% ln -sf python3 /usr/bin/python && rm -rf /var/cache/apk/* && rm -rf /tmp/*
#RUN pip install --no-cache --upgrade pip setuptools
COPY --from=build . .
CMD ["python", "main.py"]