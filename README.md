# HMS-mountain-discovery

## Overview
The purpose of this tool is to facilitate the mountain discovery process by powering on Chassis, ComputeModules, and RouterModules below a CMM (ChassisBMC).
This process will be executed via ansible that will execute the kubernetes job that conatains this process.
If the `FEATURE_FLAG_SLS` is enabled then the process will attempt to verify that HSM has all CMMs identified in SLS.

The general flow of the process is as follows:

 1. retrieve list of Chassis, ComputeModules, RouterBMCs HSM that are not empty
 1. For each xname, retrieve the power status from CAPMC.
 1. For each device that is OFF, tell CAPMC to power it on.
     1. Wait for CAPMC to return
 1. Verify power status from CAPMC
 1. *Optional compare CMMs in SLS to HSM
 1. Report on operation status.  
    1. if all powered off nodes are NOW powered on, then it is a success!
 
## Development Approach
The development approach for this project is the create a python application (that will be deployed as a kubernetes job), that will execute the above process. 

Because elements like HSM and SLS are LARGE and have extensive overhead I have created some very minimal synthetic versions of each service that facilitate the bare minimum of interactions to correcly emulate their respective services.

Each 'Synthetic' service uses the correct pathing, verbs and response payloads as described by their API documentation. 


## Test Approach
The automated testing approach for this project is to use docker-compose to stand up a synthetic SLS and a synthetic HSM as well as run the script in a container.  

The Synthsm (synthetic hsm) utilizes two special files:

 1. `redfish_endpoints.json` - contains the 'population' for HSM to use.
 1. `resfish_endpoints_discovery_status_testing.json` - contains a list of BMCs and default LastDiscoveryStatus they should be set to, this allows for test case injection of a BMC failing discovery from the perspective of HSM

The Synthetic-SLS utilized one special file:

 1. `search_hardware.json` - contains the SLS population to use.
 
The Synthetic-CAPMC utilized one special file:

 1. `get_xname_status.json` - contains the capmc xname power status population to use.
 
 
The `docker-compose.yml` is used by `runUnitTest.sh` to standup the correct testing environment and run the process.  Of important note is the `extra hosts` key. This allows us to create 'PING'able 'endpoints' that we can use for testing. 
 
### Test Cases 

The main test boundary cases are:

 1. xname in SLS that is in HSM
 1. xname in  SLS that is NOT in HSM
    1. xname cannot be pinged
    1. xname can be pinged -> Tell HSM
        1. HSM unexpectidly cannot find xname
        1. HSM fails the discovery xname
        1. HSM times out waiting for xname
        1. HSM successfully discovers xname
        
### runUnitTest.sh
The `runUnitTest.sh` script will:
 
 1. install docker-compose if it doesnt not exist
 1. use docker-compose to stand-up the 4 containers: 
     1. synthetic-SLS
     1. synthsm
     1. synthetic-capmc
     1. mountain-discovery
 1. the conatiners will run until the discovery container exits.  
 1. the exit code will be reported to the user as the OVERALL exit code.
 1. the docker-compose environment will be torn down.
 
### ansible test procedure
This code is only part of equation. The remaining piece is ansible and k8s job yaml that instantiates the job.  

That code will be checked into crayctl/ansible_famework/roles/mountain-discovery

Here is that test procedure.

 1. `./build_tag_push -l slice-sms.us.cray.com:5000`, make sure that slice is in your list of trusted `insecure registries`
 1. scp the ansbile to `/opt/cray/crayctl/ansible_framework/main + /opt/cray/crayctl/ansible_framework/roles/mountain-discovery/* the respective files`
 1. use ansible to start the play: `ansible-playbook mountain-discovery`  probably need to be in `/opt/cray/crayctl/ansible_framework/main` to run that
 
## <a name="vars">Environment Variables</a>
The HMS-mountain-discovery accepts the following env variables:

  1. FEATURE_FLAG_SLS (default False)
     1. whether or not to do CMM comparison
  2. SLEEP_LENGTH (default 30 seconds)
     1. The length of time between CAPMC xname_on, and verifying the power status from CAPMC
  2. LOG_LEVEL  
     options:  
     1. DEBUG  (default)
     1. INFO  
     1. ERROR   
     1. WARNING  
     1. PANIC  
  2. HSM_PROTOCOL  (default: `http://`)
     1. used for the path builder
  2. HSM_HOST_WITH_PORT  (default: `cray-smd`)
     1. used for the path builder
  2. HSM_BASE_PATH  (default: empty)
     1. used for the path builder
  2. SLS_PROTOCOL  (default: `http://`)
     1. used for the path builder
  2. SLS_HOST_WITH_PORT  (default: `cray-sls`)
     1. used for the path builder
  2. SLS_BASE_PATH  (default: empty)
     1. used for the path builder
  2. CAPMC_PROTOCOL  (default: `http://`)
     1. used for the path builder
  2. CAPMC_HOST_WITH_PORT  (default: `cray-capmc`)
     1. used for the path builder
  2. CAPMC_BASE_PATH  (default: empty)
     1. used for the path builder
     
[back to top](#top)

