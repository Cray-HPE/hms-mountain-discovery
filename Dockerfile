# MIT License

# (C) Copyright [2021] Hewlett Packard Enterprise Development LP

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

FROM arti.dev.cray.com/baseos-docker-master-local/alpine:3.13 AS build-base

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
