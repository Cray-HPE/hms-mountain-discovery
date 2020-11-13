#! /usr/bin/env python3
# Copyright [2019] Cray Inc. All Rights Reserved.
# Except as permitted by contract or express written permission of Cray Inc.,
# no part of this work or its content may be modified, used, reproduced or
# disclosed in any form. Modifications made without express permission of
# Cray Inc. may damage the system the software is installed within, may
# disqualify the user from receiving support from Cray Inc. under support or
# maintenance contracts, or require additional support services outside the
# scope of those contracts to repair the software or system.


import functions

import config
import logging
import time
import os
import urllib3
import json
import ping3
import copy


##################
## TODOS
# allow synthetic-capmc to NOT update node power states -> not worth it
# put a delay in CAPMC of 120 seconds and see if the connection times out. -> it doesnt
# find out what happens if a connection severs -> get a 500
# check HSM for xname status? -> not worth it
# wire up HSM to get a new power state from CAPMC stuff? -> not worth it
##################

SLEEP_LENGTH = 3
FEATURE_FLAG_SLS = False

def configure_logging():
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
    logging.info('Starting Mountain Discovery Helper')
    logging.info("LOG_LEVEL: %s; value: %s", log_level, llevel)

def configure_HSM():
    if "HSM_PROTOCOL" in os.environ:
        hsm_protocol = os.environ['HSM_PROTOCOL']
    else:
        hsm_protocol = "http://"

    if "HSM_HOST_WITH_PORT" in os.environ:
        hsm_server_port = os.environ['HSM_HOST_WITH_PORT']
    else:
        hsm_server_port = "cray-smd"

    if "HSM_BASE_PATH" in os.environ:
        hsm_base_path = os.environ['HSM_BASE_PATH']
    else:
        hsm_base_path = ""

    config.connections_init_hsm(hsm_protocol, hsm_server_port, hsm_base_path)

def conigure_SLS():
    if "SLS_PROTOCOL" in os.environ:
        sls_protocol = os.environ['SLS_PROTOCOL']
    else:
        sls_protocol = "http://"

    if "SLS_HOST_WITH_PORT" in os.environ:
        sls_host_with_port = os.environ['SLS_HOST_WITH_PORT']
    else:
        sls_host_with_port = "cray-sls"

    if "SLS_BASE_PATH" in os.environ:
        sls_base_path = os.environ['SLS_BASE_PATH']
    else:
        sls_base_path = ""

    config.connections_init_sls(sls_protocol, sls_host_with_port, sls_base_path)

def configure_CAPMC():
    if "CAPMC_PROTOCOL" in os.environ:
        capmc_protocol = os.environ['CAPMC_PROTOCOL']
    else:
        capmc_protocol = "http://"

    if "CAPMC_HOST_WITH_PORT" in os.environ:
        capmc_host_with_port = os.environ['CAPMC_HOST_WITH_PORT']
    else:
        capmc_host_with_port = "cray-capmc"

    if "CAPMC_BASE_PATH" in os.environ:
        capmc_base_path = os.environ['CAPMC_BASE_PATH']
    else:
        capmc_base_path = ""

    config.connections_init_capmc(capmc_protocol, capmc_host_with_port, capmc_base_path)

def configure_SSL():
    verify_ssl = False
    if "VERIFY_SSL" in os.environ:
        if os.environ['VERIFY_SSL'].upper() == 'FALSE':
            verify_ssl = False
            # have to disable warnings because this is all self-signed!
            urllib3.disable_warnings()

    config.requests_verify_ssl_init(verify_ssl)

def main():
    targeted_hardware_type = []
    targeted_hardware_type.append("Chassis")
    targeted_hardware_type.append("ComputeModule")
    targeted_hardware_type.append("RouterModule")

    targeted_hardware = []
    targeted_hardware_for_power_on = []
    successful_power_on = []


    ############
    # Configurations
    ############

    # 1 - CONFIGURE LOGGING
    configure_logging()

    # 2 - CONFIGURE CONNECTION To HSM
    configure_HSM()

    # 3 - CONFIGURE CONNECTION To SLS
    conigure_SLS()

    # 4 - CONFIGURE CONNECTION To CAPMC
    configure_CAPMC()

    # 5 - have to setup ssl policy before trying to use the api
    configure_SSL()

    # #5 - configure time
    if "SLEEP_LENGTH" in os.environ:
        SLEEP_LENGTH = int(os.environ['SLEEP_LENGTH'])

    FEATURE_FLAG_SLS = False
    if "FEATURE_FLAG_SLS" in os.environ:
        FFS = os.environ['FEATURE_FLAG_SLS']
        if FFS in ['TRUE','True','true']:
            FEATURE_FLAG_SLS = True

    #################
    # GET list of targeted_hardware_type endpoints from HSM
    #################
    logging.info("Retrieving list of StateComponents %s from HSM", str(targeted_hardware_type))
    result, err = functions.hsm_get_state_components(targeted_hardware_type)
    if err != None:
        logging.error(err)
        logging.critical("cannot connect to hsm, terminating...")
        exit(1)
    else:
        logging.debug("Retrieved StateComponents from HSM")

    component_endpoints = json.loads(result.text)
    for component_endpoint in component_endpoints['Components']:
        if component_endpoint['State'] != 'Empty':
            targeted_hardware.append(component_endpoint['ID'])

    logging.info("targeted hardware: %s", str(targeted_hardware))

    if len(targeted_hardware) == 0:
        logging.info("No valid targets, exiting")
        exit(0)

    #################
    # GET power status for targeted_hardware;
    #################
    logging.info("Retrieving xname power state from CAPMC: %s", str(targeted_hardware))
    result, err = functions.capmc_get_xname_status(targeted_hardware)
    if err != None:
        logging.error(err)
        logging.critical("cannot connect to CAPMC, terminating...")
        exit(1)

    result_payload = json.loads(result.text)
    logging.debug("Retrieved xname power state from CAPMC: %s", json.dumps(json.loads(result.text)))

    if int(result_payload['e']) == 400:
        logging.error("received error from CAPMC: %s", result_payload['err_msg'])


    ###############
    # POWER on targeted xnames that are 'off'
    ###############
    # ONLY attempt to power on a node that isnt already on, else you will get a CAPMC error! (yes, thats dumb... but thats redfish forya)
    VERIFY_POWER = False
    if 'off' not in result_payload.keys():
        logging.info("No xnames are in 'off' state; skipping power on attempt!")
    else:
        targeted_hardware_for_power_on = result_payload['off']
        logging.info("targeted xname for power on: %s", str(targeted_hardware_for_power_on))
        result, err = functions.capmc_xname_on(targeted_hardware_for_power_on, "power on to facilitate mountain discovery")
        if err != None:
            logging.error(err)
        else:
            if result.status_code != 500:
                VERIFY_POWER = True
                result_payload = json.loads(result.text)

                # print a warning if the e code is un-expected
                if int(result_payload['e']) != 0:
                    logging.warning("e: %s, err_msg: %s", result_payload['e'], result_payload['err_msg'])

    ###############
    # Verify POWER state
    ###############
    #check power status for all targetd_xname that we attempted to power on
    if VERIFY_POWER:
        logging.info("Sleeping for %d seconds before attempting to verify power state", SLEEP_LENGTH)
        time.sleep(SLEEP_LENGTH)
        result, err = functions.capmc_get_xname_status(targeted_hardware_for_power_on)
        if err != None:
            logging.error(err)
        result_payload = json.loads(result.text)

        if int(result_payload['e']) != 0:
            logging.error("e: %s, err_msg: %s", result_payload['e'], result_payload['err_msg'])
        else:
            if 'on' in result_payload.keys():
                if len(result_payload['on']) != len(targeted_hardware_for_power_on):
                    logging.error("Not all xnames could be powered on: %s", json.dumps(result_payload))
                else:
                    logging.info("Power on successfully applied to: %s", str(result_payload['on']))
                    successful_power_on = result_payload['on']
            else:
                logging.warning("power on of targeted xnames has not worked as expected")

    #############
    # COMPARE SLS cmms to HSM
    #############
    if FEATURE_FLAG_SLS:

        #################
        ## GET list of ChassisBMC from SLS
        #################
        sls_chassis_bmc = []
        logging.info("Retrieving list of hardware %s from SLS", str(['comptype_chassis_bmc']))
        result, err = functions.sls_search_hardware('comptype_chassis_bmc', 'Mountain')
        if err != None:
            logging.error(err)
            FEATURE_FLAG_SLS = False
            logging.info("Skipping SLS comparison")

        else:
            logging.debug("Retrieved ComponentEndpoints from HSM")
            sls_hardware = json.loads(result.text)
            for hw in sls_hardware:
                if 'XName' in hw.keys():
                    sls_chassis_bmc.append(hw['XName'])

        if FEATURE_FLAG_SLS:
            #################
            ## GET list of ChassisBMC from HSM
            #################
            hsm_chassis_bmc = []
            logging.info("Retrieving list of StateComponents %s from HSM", str(['ChassisBMC']))
            result, err = functions.hsm_get_state_components(['ChassisBMC'])
            if err != None:
                logging.error(err)

            else:
                logging.debug("Retrieved StateComponents from HSM")

                component_endpoints = json.loads(result.text)
                for component_endpoint in component_endpoints['Components']:
                    if component_endpoint['State'] != 'Empty':
                        hsm_chassis_bmc.append(component_endpoint['ID'])


            ##############
            # COMPARE
            ##############

            logging.debug("HSM ChassisBMC(CMM) population: %s",str(hsm_chassis_bmc))
            logging.debug("SLS ChassisBMC(CMM) population: %s",str(sls_chassis_bmc))


            sls_intersect_hsm = []
            for x in hsm_chassis_bmc:
                for y in sls_chassis_bmc:
                    if y == x:
                        sls_intersect_hsm.append(y)
            logging.debug("SLS/HSM intersection: %s", str(sls_intersect_hsm))

            hsm_minus_sls = []
            for x in hsm_chassis_bmc:
                if x not in sls_chassis_bmc:
                    hsm_minus_sls.append(x)
            logging.warning("HSM minus SLS: %s", str(hsm_minus_sls))

            sls_minus_hsm = []
            for x in sls_chassis_bmc:
                if x not in hsm_chassis_bmc:
                    sls_minus_hsm.append(x)
            logging.warning("SLS minus HSM: %s", str(sls_minus_hsm))

    # #########
    # # Report & Exit
    # #########
    logging.info("Operation Summary:")
    logging.info("Targeted hardware types: \t %s", str(targeted_hardware_type))
    logging.info("HSM identified count of targeted hardware: \t %d", len(targeted_hardware))
    logging.debug("HSM identified population of targeted hardware: \t %s", str(targeted_hardware))

    logging.info("Count of xnames for power on: \t %d", len(targeted_hardware_for_power_on))
    logging.debug("Targeted population of xnames for power on: \t %s", str(targeted_hardware_for_power_on))
    logging.info("Count of xnames successfully powered on: \t %d", len(successful_power_on))
    logging.debug("Targeted population of xnames successfully powered on: \t %s", str(successful_power_on))

    # short circuit evaluation
    if FEATURE_FLAG_SLS and len(sls_minus_hsm) > 0:
        logging.error("HSM is missing %d CMM's as identified in SLS, it is possible not all CMMs have been powered on!", len(sls_minus_hsm))
        logging.error("SLS minus HSM: %s", str(sls_minus_hsm))

    if len(targeted_hardware_for_power_on) != len(successful_power_on):
        failed_power_on = []
        for x in targeted_hardware_for_power_on:
            if x not in successful_power_on:
                failed_power_on.append(x)
        logging.critical("FAILURE: Could not power on xnames: %s", str(failed_power_on))
        exit(1)

if __name__ == '__main__':
    main()

# vim: set expandtab tabstop=4 shiftwidth=4: