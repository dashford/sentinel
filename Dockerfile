FROM python:3.6-alpine

RUN apk --update add \
    curl \
    make \
    gcc \
    glib-dev \
    musl-dev \
    bluez \
    git

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# TODO Remove once https://github.com/IanHarvey/bluepy/issues/158 is solved
WORKDIR /usr/local/lib/python3.6/site-packages/bluepy
RUN make bluepy-helper

WORKDIR /home/sentinel

CMD ["python", "sentinel.py"]
