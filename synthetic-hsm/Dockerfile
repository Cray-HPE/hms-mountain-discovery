# Copyright 2020 Hewlett Packard Enterprise Development LP

FROM dtr.dev.cray.com/baseos/alpine:3.12 AS build-base

# Configure pip to use the DST PIP Mirror
ENV PIP_TRUSTED_HOST dst.us.cray.com
ENV PIP_INDEX_URL http://$PIP_TRUSTED_HOST/dstpiprepo/simple/

COPY requirements.txt /

RUN set -ex \
    && apk update \
    && apk add --no-cache \
        python3 \
        py3-pip \
    && pip3 install --upgrade \
        pip \
        setuptools \
    && pip3 install -r /requirements.txt

FROM build-base

COPY . /app
WORKDIR /app
EXPOSE 27779
ENTRYPOINT ["python3"]
CMD ["app.py"]
