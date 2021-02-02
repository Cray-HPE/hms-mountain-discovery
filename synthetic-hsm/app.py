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

redfish_endpoints = {}
component_endpoints = {}
state_components = {}

@app.route('/Inventory/ComponentEndpoints', methods=['GET'])
def component_endpoints():

    if request.method == 'GET':
        tmp = get_component_endpoints(request)
        return tmp


def get_component_endpoints(request):
    typeOfEndpoint = request.args.getlist('type')

    payload = {}
    RfEp = []

    if typeOfEndpoint == None:
        return jsonify(component_endpoints)

    for ep in component_endpoints['ComponentEndpoints']:
        if ep['Type'] in typeOfEndpoint:
            RfEp.append(ep)

    payload['ComponentEndpoints'] = RfEp

    response = app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype='application/json'
    )

    return response


@app.route('/State/Components', methods=['POST','GET'])
def state_components():
    typeOfEndpoint = request.args.getlist('type')

    payload = {}
    RfEp = []

    if typeOfEndpoint == None:
        return jsonify(state_components)

    for ep in state_components['Components']:
        if ep['Type'] in typeOfEndpoint:
            RfEp.append(ep)

    payload['Components'] = RfEp

    response = app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype='application/json'
    )

    return response

    # nidList = request.args.getlist('nid')
    # nids = []
    #
    # #convert from string to int
    # for n in nidList :
    #     try:
    #         nid = int(n)
    #         nids.append(nid)
    #     except ValueError:
    #         continue
    #
    # #if there are no nids in the query then return all of them from the file
    # if len(nids) == 0 :
    #     return jsonify(state_components)
    #
    # #else match the nids and return
    # componentsByNid = {}
    # for c in state_components["Components"]:
    #     componentsByNid[c["NID"]] = c
    #
    # nidComponents = []
    # for nid in nids:
    #     if nid in componentsByNid.keys():
    #         nidComponents.append(componentsByNid[nid])
    #
    # finalComponents = {}
    # finalComponents["Components"] = nidComponents
    #
    # return jsonify(finalComponents)


@app.route('/Inventory/RedfishEndpoints/<xname>', methods=['GET'])
def redfish_endpoint(xname):

    if request.method == 'GET':
        tmp = get_redfish_endpoint(xname, request)
        return tmp


def get_redfish_endpoint(xname, request):
    payload = {}
    found = False
    for ep in redfish_endpoints['RedfishEndpoints']:
        if xname == ep['ID']:
            payload=ep
            found = True

    if found == True:
        response = app.response_class(
            response=json.dumps(payload),
            status=200,
            mimetype='application/json'
        )
    else:
        payload['error'] = 'not found'

        response = app.response_class(
            response=json.dumps(payload),
            status=404,
            mimetype='application/json'
        )
    return response


@app.route('/Inventory/RedfishEndpoints', methods=['GET', 'POST'])
def redfish_endpoints():

    if request.method == 'GET':
        tmp = get_redfish_endpoints(request)
        return tmp

    elif request.method == 'POST':
        tmp = post_redfish_endpoints(request)
        return tmp

def get_redfish_endpoints(request):
    typeOfEndpoint = request.args.get('type')
    payload = {}
    RfEp = []

    if typeOfEndpoint == None:
        return jsonify(redfish_endpoints)

    for ep in redfish_endpoints['RedfishEndpoints']:
        if typeOfEndpoint == ep['Type']:
            RfEp.append(ep)

    payload['RedfishEndpoints'] = RfEp

    response = app.response_class(
        response=json.dumps(payload),
        status=200,
        mimetype='application/json'
    )

    return response

def post_redfish_endpoints(request):
    req = request.get_json()
    logging.debug(req)

    xnames = []
    return_payload = []
    eps  = req['RedfishEndpoints']
    for ep in eps:
        xname = ep['ID']
        xnames.append(xname)
        tmp = {}
        tmp['URI'] = '/Inventory/RedfishEndpoints/' + str(xname)
        return_payload.append(tmp)

    #add the new rf endpoints
    for xname in xnames:
        tmp = {}
        tmp['ID'] = xname
        tmp['Type']= "NodeBMC"

        tmpDisc= {}
        tmpDisc['LastDiscoveryAttempt']=datetime.datetime.now().isoformat()
        tmpDisc['LastDiscoveryStatus'] = 'DiscoverOK'

        #check to see if we should override this
        for d in inventory_rf_endpoints_special_test:
            if d['ID'] == xname:
                tmpDisc['LastDiscoveryStatus']=d['LastDiscoveryStatus']

        tmpDisc['RedfishVersion']='1.2.0'
        tmp['DiscoveryInfo']=tmpDisc
        redfish_endpoints['RedfishEndpoints'].append(tmp)

    response = app.response_class(
        response=json.dumps(return_payload),
        status=201,
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
    logging.info('Starting Synthetic-HSM')
    logging.info("LOG_LEVEL: %s; value: %s", log_level, llevel)

    with open('files/redfish_endpoints.json', 'r') as f:
        redfish_endpoints = json.load(f)

    with open('files/component_endpoints.json', 'r') as f:
        component_endpoints = json.load(f)

    with open('files/state_components.json', 'r') as f:
        state_components = json.load(f)

    with open('files/redfish_endpoints_discovery_status_testing.json', 'r') as f:
        inventory_rf_endpoints_special_test = json.load(f)

    app.run(debug=False, host='0.0.0.0', port=27779)
