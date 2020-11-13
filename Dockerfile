# Copyright 2020 Hewlett Packard Enterprise Development LP

FROM dtr.dev.cray.com/baseos/alpine:3.12 AS build-base

# Configure pip to use the DST PIP Mirror
ENV PIP_TRUSTED_HOST dst.us.cray.com
ENV PIP_INDEX_URL http://$PIP_TRUSTED_HOST/dstpiprepo/simple/

COPY src/requirements.txt /

RUN set -ex \
    && apk update \
    && apk add --no-cache \
        python3 \
        py3-pip \
        curl \
    && pip3 install --upgrade \
        pip \
        setuptools \
    && pip3 install -r /requirements.txt

FROM build-base

COPY src /app
WORKDIR /app

ENV LOG_LEVEL DEBUG
ENV HSM_PROTOCOL http://
ENV HSM_HOST_WITH_PORT cray-smd
#ENV HSM_BASE_PATH /v1

ENV SLS_PROTOCOL http://
ENV SLS_HOST_WITH_PATH sls
#ENV SLS_BASE_PATH = ""

ENV SLEEP_LENGTH 30
ENV FEATURE_FLAG_SLS True

ENTRYPOINT ["python3"]
CMD ["mountain_discovery.py"]
