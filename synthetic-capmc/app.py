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

from flask import Flask, render_template, request, jsonify
import json
import logging
import os
import time
import datetime

app = Flask(__name__)

xname_status = {}

# DISCLAIMER!!!!!!!!!!
# This was built based on conversations with bginsbach and mjendrysik.
# The CAPMC API doc does NOT conform to the code as of the writing of this doc: 11/11/19

@app.route('/xname_on', methods=['POST'])
def xname_on():
    payload = {}
    error = False
    e = 400
    err_msg = "invalid request, xnames list cannot be empty"

    logging.debug(request)

    the_json = request.get_json(force=True)
    logging.debug("json: %s",the_json)
    xnames = the_json['xnames']

    if len(xnames) == 0:
        payload['e'] = e
        payload['err_msg'] = err_msg
        response = app.response_class(
            response=json.dumps(payload),
            status=400,
            mimetype='application/json'
        )
        return response

    not_found = []
    # if xname in xname_status; then set the state;
    for xname in xnames:
        if xname in xname_status.keys():
            xname_status[xname] = "on"
            e = 0
            err_msg = ""
        else:
            error = True
            not_found.append(xname)


    payload = {}

    if error == False:
        e = 0
        err_msg = ""
        payload['e'] = e
        payload['err_msg'] = err_msg

        response = app.response_class(
            response=json.dumps(payload),
            status=200,
            mimetype='application/json'
        )
    else:
        payload['err_msg'] = 'xnames not found: ' + str(not_found)
        payload['e'] = 400

        response = app.response_class(
            response=json.dumps(payload),
            status=400,
            mimetype='application/json'
        )
    return response



@app.route('/get_xname_status', methods=['POST'])
def get_xname_status():
    payload = {}
    error = False
    e = 400
    err_msg = "invalid request, xnames list cannot be empty"

    logging.debug(request)

    the_json = request.get_json(force=True)
    logging.debug("json: %s",the_json)
    xnames = the_json['xnames']

    if len(xnames) == 0:
        payload['e'] = e
        payload['err_msg'] = err_msg
        response = app.response_class(
            response=json.dumps(payload),
            status=400,
            mimetype='application/json'
        )
        return response


    status_dict = {}
    not_found = []

    # look for xnames
    for xname in xnames:
        if xname in xname_status.keys():
            status = xname_status[xname]
            logging.debug("status %s, xname %s",status, xname)
            if status in status_dict.keys():
                status_dict[status].append(xname)
            else:
                list = []
                list.append(xname)
                status_dict[status] = list
        else:
            not_found.append(xname)
            error = True


    total_count = 0

    for key_type in status_dict.keys():
        total_count += len(status_dict[key_type])

    logging.debug("total_count: %d", total_count)



    payload = {}

    if error == False:
        e = 0
        err_msg = ""
        # count undefined keys
        if 'undefined' in status_dict.keys():
            undefined_len = len(status_dict['undefined'])
            err_msg = 'Errors encountered with ' + str(undefined_len) + '/' + str(total_count) + ' Xnames'
            e = 0
        payload['e'] = e
        payload['err_msg'] = err_msg
        for key in status_dict.keys():
            payload[key] = status_dict[key]
        response = app.response_class(
            response=json.dumps(payload),
            status=200,
            mimetype='application/json'
        )
    else:
        payload['err_msg'] = 'xnames not found: ' + str(not_found)
        payload['e'] = 400

        response = app.response_class(
            response=json.dumps(payload),
            status=400,
            mimetype='application/json'
        )
    return response



if __name__ == '__main__':

    ############
    # Configurations
    ############

    # 1 - CONFIGURE LOGGING
    llevel = logging.DEBUG
    log_level = "DEBUG"
    if "LOG_LEVEL" in os.environ:
        log_level = os.environ['LOG_LEVEL'].upper()
        if log_level == "DEBUG":
            llevel = logging.DEBUG
        elif log_level == "INFO":
            llevel = logging.INFO
        elif log_level == "WARNING":
            llevel = logging.WARNING
        elif log_level == "ERROR":
            llevel = logging.ERROR
        elif log_level == "NOTSET":
            llevel = logging.NOTSET

    logging.Formatter.converter = time.gmtime
    FORMAT = '%(asctime)-15s-%(levelname)s-%(message)s'
    logging.basicConfig(format=FORMAT, level=llevel, datefmt='%Y-%m-%dT%H:%M:%SZ')
    logging.info('Starting Synthetic-CAPMC')
    logging.info("LOG_LEVEL: %s; value: %s", log_level, llevel)


    #load xname status file
    with open('files/get_xname_status.json', 'r') as f:
        xname_status_dict = json.load(f)

    xname_status = {}

    for xname in xname_status_dict['on']:
        xname_status[xname] = 'on'
    for xname in xname_status_dict['off']:
        xname_status[xname] = 'off'
    for xname in xname_status_dict['undefined']:
        xname_status[xname] = 'undefined'


    app.run(debug=False, host='0.0.0.0', port=37777)
