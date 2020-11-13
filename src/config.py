#!/usr/bin/env python3
# Copyright [2019] Cray Inc. All Rights Reserved.
# Except as permitted by contract or express written permission of Cray Inc.,
# no part of this work or its content may be modified, used, reproduced or
# disclosed in any form. Modifications made without express permission of
# Cray Inc. may damage the system the software is installed within, may
# disqualify the user from receiving support from Cray Inc. under support or
# maintenance contracts, or require additional support services outside the
# scope of those contracts to repair the software or system.

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
