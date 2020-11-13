from flask import Flask, render_template, request, jsonify
import json
import os
import logging
import time

app = Flask(__name__)


@app.route('/search/hardware', methods=['GET'])
def search_hardware():
    with open('files/search_hardware.json', 'r') as f:
        components = json.load(f)

    typeOfComponent = request.args.get('type')
    typeOfClass = request.args.get('class')

    HaCo = []

    if typeOfComponent == None and typeOfClass == None:
        return jsonify(components)
    elif typeOfComponent != None and typeOfClass== None:
        for co in components:
            if typeOfComponent == co['Type']:
                HaCo.append(co)
    elif typeOfComponent == None and typeOfClass != None:
        for co in components:
            if typeOfClass == co['Class']:
                HaCo.append(co)
    else:
        for co in components:
            if typeOfClass == co['Class'] and typeOfComponent == co['Type']:
                HaCo.append(co)
    logging.debug(HaCo)
    return jsonify(HaCo)

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

    app.run(debug=False, host='0.0.0.0', port=8376)
