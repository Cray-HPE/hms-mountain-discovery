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

import config
import requests
import logging
import json
from dateutil.parser import parse
import re


def hsm_get_state_components(types):
    if types == None or len(types) == 0:
        url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/State/Components"
    else:
        type_string = "?"
        for ty in types:
            type_string +='type='+ty + '&'
        type_string = type_string[:-1]
        url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/State/Components" + type_string

    logging.debug("preparing request url: %s", url)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    try:
        res = requests.request("GET", url, data=payload, headers=headers, verify=config.VERIFY_SSL)
        return res, None
    except requests.exceptions.ConnectionError as err:
        return None, err

def hsm_get_component_endpoints(types):
    if types == None or len(types) == 0:
        url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/Inventory/ComponentEndpoints"
    else:
        type_string = "?"
        for ty in types:
            type_string +='type='+ty + '&'
        type_string = type_string[:-1]
        url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/Inventory/ComponentEndpoints" + type_string


    logging.debug("preparing request url: %s", url)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    try:
        res = requests.request("GET", url, data=payload, headers=headers, verify=config.VERIFY_SSL)
        return res, None
    except requests.exceptions.ConnectionError as err:
        return None, err


def hsm_get_redfish_endpoints(type):

    if type != None:
        url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/Inventory/RedfishEndpoints?type=" + type
    else:
        url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/Inventory/RedfishEndpoints"

    logging.debug("preparing request url: %s", url)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    try:
        res = requests.request("GET", url, data=payload, headers=headers, verify=config.VERIFY_SSL)

    except requests.exceptions.ConnectionError as err:
        return None, err
    return res, None

def hsm_get_redfish_endpoint(xname):

    url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/Inventory/RedfishEndpoints/" + xname
    logging.debug("preparing request url: %s", url)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    try:
        res = requests.request("GET", url, data=payload, headers=headers, verify=config.VERIFY_SSL)

    except requests.exceptions.ConnectionError as err:
        return None, err
    return res, None


def capmc_get_xname_status(xnames):

    url = config.CAPMC_PROTOCOL + config.CAPMC_HOST_WITH_PORT + config.CAPMC_BASE_PATH + "/get_xname_status"

    logging.debug("preparing request url: %s", url)
    payload = {}
    payload['xnames'] = xnames
    headers = {
        'cache-control': "no-cache",
    }
    logging.debug("payload: %s",json.dumps(payload))
    try:
        res = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=config.VERIFY_SSL)

    except requests.exceptions.ConnectionError as err:
        return None, err
    return res, None


def capmc_xname_on(xnames, reason):
    url = config.CAPMC_PROTOCOL + config.CAPMC_HOST_WITH_PORT + config.CAPMC_BASE_PATH + "/xname_on"

    logging.debug("preparing request url: %s", url)
    payload = {}
    payload['xnames'] = xnames
    payload['reason'] = reason
    payload['continue'] = True
    headers = {
        'cache-control': "no-cache",
    }
    logging.debug("payload: %s", json.dumps(payload))
    try:
        res = requests.request("POST", url, data=json.dumps(payload), headers=headers, verify=config.VERIFY_SSL)

    except requests.exceptions.ConnectionError as err:
        return None, err
    return res, None


def sls_search_hardware(type_name, class_name):
    url = config.SLS_PROTOCOL + config.SLS_HOST_WITH_PORT + config.SLS_BASE_PATH + "/search/hardware?type="+type_name+"&class="+class_name
    logging.debug("preparing request url: %s", url)
    payload = ""
    headers = {
        'cache-control': "no-cache",
    }
    try:
        res = requests.request("GET", url, data=payload, headers=headers, verify=config.VERIFY_SSL)

    except requests.exceptions.ConnectionError as err:
        return None, err
    return res, None
#
#
#
#     ## post_hsm_add_redfishendpoints: expects format:
#     # {
#     #     "RedfishEndpoints": [
#     #         {
#     #             "ID": "x0c0s28b0",
#     #             "RediscoverOnUpdate": true
#     #         }
#     #     ]
#     # }
# def post_hsm_add_redfishendpoints(nodes, rediscover):
#     url = config.HSM_PROTOCOL + config.HSM_HOST_WITH_PORT + config.HSM_BASE_PATH + "/Inventory/RedfishEndpoints"
#     logging.debug("preparing request url: %s", url)
#     payload = ""
#     payload_struct = {}
#     payload_list = []
#     for node in nodes:
#         tmp = {}
#         tmp['ID'] = node
#         tmp['RediscoverOnUpdate'] = rediscover
#         payload_list.append(tmp)
#
#     payload_struct['RedfishEndpoints'] = payload_list
#
#     payload = json.dumps(payload_struct)
#     headers = {
#         'cache-control': "no-cache",
#         'content-type':"application/json"
#     }
#     try:
#         res = requests.request("POST", url, data=payload, headers=headers, verify=config.VERIFY_SSL)
#     except requests.exceptions.ConnectionError as err:
#         return None, err
#     return res, None



def is_valid_timestamp(date_text):
    try:
        date = parse(date_text)
        return True
    except ValueError:
        return False


def is_empty(any_structure):
    if any_structure:
        return False
    else:
        return True

def validate_string_format(string):
    charRe = re.compile(r'[^a-zA-Z0-9\_\-.]')
    string = charRe.search(string)
    return not bool(string)