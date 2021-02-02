#!/usr/bin/env python3

# MIT License

# (C) Copyright [2019-2021] Hewlett Packard Enterprise Development LP

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


import logging
HSM_PROTOCOL = ""
HSM_HOST_WITH_PORT = ""
HSM_BASE_PATH = ""

SLS_PROTOCOL = ""
SLS_HOST_WITH_PORT = ""
SLS_BASE_PATH = ""

CAPMC_PROTOCOL = ""
CAPMC_HOST_WITH_PORT = ""
CAPMC_BASE_PATH = ""

VERIFY_SSL = True


def connections_init_hsm(init_HSM_PROTOCOL, init_HSM_HOST_WITH_PORT, init_HSM_BASE_PATH):
    global HSM_PROTOCOL
    global HSM_HOST_WITH_PORT
    global HSM_BASE_PATH

    HSM_PROTOCOL = init_HSM_PROTOCOL
    HSM_HOST_WITH_PORT = init_HSM_HOST_WITH_PORT
    HSM_BASE_PATH = init_HSM_BASE_PATH

    con = {}
    con["HSM_PROTOCOL"] = HSM_PROTOCOL
    con["HSM_HOST_WITH_PORT"] = HSM_HOST_WITH_PORT
    con["HSM_BASE_PATH"] = HSM_BASE_PATH
    logging.info("Configuring HSM connection: %s", con)

def connections_init_sls(init_SLS_PROTOCOL, init_SLS_HOST_WITH_PORT, init_SLS_BASE_PATH):
    global SLS_PROTOCOL
    global SLS_HOST_WITH_PORT
    global SLS_BASE_PATH

    SLS_PROTOCOL = init_SLS_PROTOCOL
    SLS_HOST_WITH_PORT = init_SLS_HOST_WITH_PORT
    SLS_BASE_PATH = init_SLS_BASE_PATH

    con = {}
    con["SLS_PROTOCOL"] = SLS_PROTOCOL
    con["SLS_HOST_WITH_PORT"] = SLS_HOST_WITH_PORT
    con["SLS_BASE_PATH"] = SLS_BASE_PATH
    logging.info("Configuring SLS connection: %s", con)

def connections_init_capmc(init_CAPMC_PROTOCOL, init_CAPMC_HOST_WITH_PORT, init_CAPMC_BASE_PATH):
    global CAPMC_PROTOCOL
    global CAPMC_HOST_WITH_PORT
    global CAPMC_BASE_PATH

    CAPMC_PROTOCOL = init_CAPMC_PROTOCOL
    CAPMC_HOST_WITH_PORT = init_CAPMC_HOST_WITH_PORT
    CAPMC_BASE_PATH = init_CAPMC_BASE_PATH

    con = {}
    con["CAPMC_PROTOCOL"] = CAPMC_PROTOCOL
    con["CAPMC_HOST_WITH_PORT"] = CAPMC_HOST_WITH_PORT
    con["CAPMC_BASE_PATH"] = CAPMC_BASE_PATH
    logging.info("Configuring CAPMC connection: %s", con)


def requests_verify_ssl_init(init_VERIFY_SSL):
    global VERIFY_SSL
    VERIFY_SSL = init_VERIFY_SSL
    logging.info("Configuring requests library ssl connection to use trusted connection: %s", VERIFY_SSL)
