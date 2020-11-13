# I have pushed the image to jolt1

```
./build_tag_push.sh -l jolt1-sms1.us.cray.com:5000
```

# I have SCP'd my ansible to /opt/cray/crayctl on Jolt1

# get a list of  components from HSM

```
jolt1-sms01-nmn:~ # cray hsm State Components list --format json | jq '.Components[].ID'
```

# dump sys info

```
jolt1-sms01-nmn:/opt/cray/crayctl/ansible_framework/main # cray capmc get_nid_map create --nids 100[0-7] --format json  | jq
{
  "nids": [
    {
      "role": "Compute",
      "xname": "x5000c1s1b1n0",
      "nid": 1006
    },
    {
      "role": "Compute",
      "xname": "x5000c1s1b0n0",
      "nid": 1004
    },
    {
      "role": "Compute",
      "xname": "x5000c1s0b0n0",
      "nid": 1000
    },
    {
      "role": "Compute",
      "xname": "x5000c1s0b1n0",
      "nid": 1002
    },
    {
      "role": "Compute",
      "xname": "x5000c1s0b1n1",
      "nid": 1003
    },
    {
      "role": "Compute",
      "xname": "x5000c1s0b0n1",
      "nid": 1001
    },
    {
      "role": "Compute",
      "xname": "x5000c1s1b1n1",
      "nid": 1007
    },
    {
      "role": "Compute",
      "xname": "x5000c1s1b0n1",
      "nid": 1005
    }
  ],
  "e": 0,
  "err_msg": ""
}
```

# motd

```
jolt1-sms01-nmn:/opt/cray/crayctl/ansible_framework/main # cat /etc/motd
                     oooo           oooo      .     .o
                     `888           `888    .o8   o888
                      888  .ooooo.   888  .o888oo  888
                      888 d88' `88b  888    888    888
                      888 888   888  888    888    888
                      888 888   888  888    888 .  888
                  .o. 88P `Y8bod8P' o888o   "888" o888o
                  `Y888P

             https://cje2.dev.cray.com/teams-dst-cd-pipeline/
                 job/dst-cd-pipeline/job/Shasta/job/Jolt1

--------------------------------------------------------------------------
Slack Channel: #jolt1

Last Known State: CrayCtl Install Completed Sep 17 2019
Time/Date: Wed Sep 11 04:15:04 UTC 2019

Blob: 172.30.50.19:/var/www/html/dstrepo/shasta-cd-premium-prod/
Snapshot: shasta-cd-snapshots/shasta-premium-prod/2019-09-09_15-30-00
--------------------------------------------------------------------------


Notes
-----
- jolt1 does not have a UAN

- compute nodes
   Intel Skylake        :  nid00000[1-4]
   Gigabyte AMD Rome    :  nid00000[5-8]  ##  nid000007 is down
   Cray Windom AMD Rome :  nid00100[0-7]  ##  nid001001 is down

News
----
11/06/19 - Problems with ARS may be fixed ('cray ars artifacts list' now works).
11/11/19 - A PE update was done at 0700.
11/12/19 - The HSN is down to nid001005.
```

# ansible logs 

```
jolt1-sms01-nmn:/opt/cray/crayctl/ansible_framework/main # ansible-playbook mountain-discovery.yml

PLAY [bis[0]] ********************************************************************************************************

TASK [docker : Set fact for cray_stack_registry_source cray_stack_registry_source={{ registries[cray_docker_registry_image_source]['fqdn'] }}:{{ registries[cray_docker_registry_image_source]['port'] }}] ***
Wednesday 13 November 2019  10:06:48 -0600 (0:00:00.116)       0:00:00.116 ****
ok: [sms01-nmn]

TASK [mountain-discovery : Look for hms-mountain-discovery yaml path={{ cray_hms_mountain_discovery_job_yaml }}] *****
Wednesday 13 November 2019  10:06:48 -0600 (0:00:00.084)       0:00:00.201 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Delete previous job if exists _raw_params=kubectl -n services delete -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:06:49 -0600 (0:00:00.590)       0:00:00.791 ****
skipping: [sms01-nmn]

TASK [mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file src=hms-mountain-discovery-job.yaml.j2, dest={{ cray_hms_mountain_discovery_job_yaml }}] ***
Wednesday 13 November 2019  10:06:49 -0600 (0:00:00.039)       0:00:00.831 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Start HMS mountain discovery job _raw_params=kubectl -n services apply -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:06:50 -0600 (0:00:01.220)       0:00:02.052 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Wait for discovery verify to complete _raw_params=kubectl -n services get jobs cray-hms-mountain-discovery -o jsonpath="{.status.conditions[0].type}"] ***
Wednesday 13 November 2019  10:06:51 -0600 (0:00:00.854)       0:00:02.906 ****
FAILED - RETRYING: Wait for discovery verify to complete (120 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (119 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (118 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (117 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (116 retries left).
changed: [sms01-nmn -> sms01-nmn]

PLAY RECAP ***********************************************************************************************************
sms01-nmn                  : ok=5    changed=3    unreachable=0    failed=0

Wednesday 13 November 2019  10:09:25 -0600 (0:02:33.842)       0:02:36.749 ****
===============================================================================
mountain-discovery : Wait for discovery verify to complete -------------------------------------------------- 153.84s
mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file ----------------------------------- 1.22s
mountain-discovery : Start HMS mountain discovery job --------------------------------------------------------- 0.85s
mountain-discovery : Look for hms-mountain-discovery yaml ----------------------------------------------------- 0.59s
docker : Set fact for cray_stack_registry_source -------------------------------------------------------------- 0.08s
mountain-discovery : Delete previous job if exists ------------------------------------------------------------ 0.04s
Playbook run took 0 days, 0 hours, 2 minutes, 36 seconds
```

# dump the logs for the thing

```
jolt1-sms01-nmn:~ # kubectl -n services logs cray-hms-mountain-discovery-j45t5 cray-hms-mountain-discovery
2019-11-13T16:07:01Z-INFO-Starting Mountain Discovery Helper
2019-11-13T16:07:01Z-INFO-LOG_LEVEL: DEBUG; value: 10
2019-11-13T16:07:01Z-INFO-Configuring HSM connection: {'HSM_PROTOCOL': 'http://', 'HSM_HOST_WITH_PORT': 'cray-smd', 'HSM_BASE_PATH': '/hsm/v1'}
2019-11-13T16:07:01Z-INFO-Configuring SLS connection: {'SLS_PROTOCOL': 'http://', 'SLS_HOST_WITH_PORT': 'cray-sls', 'SLS_BASE_PATH': ''}
2019-11-13T16:07:01Z-INFO-Configuring CAPMC connection: {'CAPMC_PROTOCOL': 'http://', 'CAPMC_HOST_WITH_PORT': 'cray-capmc', 'CAPMC_BASE_PATH': '/capmc/v1'}
2019-11-13T16:07:01Z-INFO-Configuring requests library ssl connection to use trusted connection: False
2019-11-13T16:07:01Z-INFO-Retrieving list of StateComponents ['Chassis', 'ComputeModule', 'RouterModule'] from HSM
2019-11-13T16:07:01Z-DEBUG-preparing request url: http://cray-smd/hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule
2019-11-13T16:07:01Z-DEBUG-Starting new HTTP connection (1): cray-smd:80
2019-11-13T16:07:01Z-DEBUG-http://cray-smd:80 "GET /hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule HTTP/1.1" 200 None
2019-11-13T16:07:01Z-DEBUG-Retrieved StateComponents from HMS
2019-11-13T16:07:01Z-INFO-targeted hardware: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:07:01Z-INFO-Retrieving xname power state from CAPMC: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:07:01Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:07:01Z-DEBUG-payload: {"xnames": ["x5000c3", "x5000c1r5", "x5000c1r1", "x5000c1", "x5000c1s1", "x5000c1r3", "x5000c1s0", "x5000c1r7"]}
2019-11-13T16:07:01Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:07:03Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 128
2019-11-13T16:07:03Z-DEBUG-Retrieved xname power state from CAPMC: {"e": 0, "err_msg": "", "on": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s0", "x5000c1s1"], "off": ["x5000c3"]}
2019-11-13T16:07:03Z-INFO-targeted xname for power on: ['x5000c3']
2019-11-13T16:07:03Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/xname_on
2019-11-13T16:07:03Z-DEBUG-payload: {"xnames": ["x5000c3"], "reason": "power on to facilitate mountain discovery"}
2019-11-13T16:07:03Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:08:33Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/xname_on HTTP/1.1" 200 21
2019-11-13T16:08:33Z-INFO-Sleeping for 30 seconds before attempting to verify power state
2019-11-13T16:09:03Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:09:03Z-DEBUG-payload: {"xnames": ["x5000c3"]}
2019-11-13T16:09:03Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:09:03Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 38
2019-11-13T16:09:03Z-INFO-Power on successfully applied to: ['x5000c3']
2019-11-13T16:09:03Z-INFO-Operation Summary:
2019-11-13T16:09:03Z-INFO-Targeted hardware types: 	 ['Chassis', 'ComputeModule', 'RouterModule']
2019-11-13T16:09:03Z-INFO-HSM identified count of targeted hardware: 	 8
2019-11-13T16:09:03Z-DEBUG-HSM identified population of targeted hardware: 	 ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:09:03Z-INFO-Count of xnames for power on: 	 1
2019-11-13T16:09:03Z-DEBUG-Targeted population of xnames for power on: 	 ['x5000c3']
2019-11-13T16:09:03Z-INFO-Count of xnames successfully powered on: 	 1
2019-11-13T16:09:03Z-DEBUG-Targeted population of xnames successfully powered on: 	 ['x5000c3']
```

```
jolt1-sms01-nmn:~ # cray capmc get_xname_status create --xnames x5000c3
e = 0
err_msg = ""
on = [ "x5000c3",]
```


```
jolt1-sms01-nmn:~ # cray hsm State Components list --type Chassis --format json
{
  "Components": [
    {
      "Arch": "X86",
      "Enabled": true,
      "Flag": "OK",
      "State": "Off",
      "NetType": "Sling",
      "Type": "Chassis",
      "ID": "x5000c3"
    },
    {
      "Arch": "X86",
      "Enabled": true,
      "Flag": "OK",
      "State": "On",
      "NetType": "Sling",
      "Type": "Chassis",
      "ID": "x5000c1"
    }
  ]
}
```
# ^^^ it looks like HSM didnt get the state change event

# since we have verified that x5000c3 is on, re-running the ansible should be a no-op

# ansible logs

```
jolt1-sms01-nmn:/opt/cray/crayctl/ansible_framework/main # ansible-playbook mountain-discovery.yml

PLAY [bis[0]] ********************************************************************************************************

TASK [docker : Set fact for cray_stack_registry_source cray_stack_registry_source={{ registries[cray_docker_registry_image_source]['fqdn'] }}:{{ registries[cray_docker_registry_image_source]['port'] }}] ***
Wednesday 13 November 2019  10:17:24 -0600 (0:00:00.101)       0:00:00.101 ****
ok: [sms01-nmn]

TASK [mountain-discovery : Look for hms-mountain-discovery yaml path={{ cray_hms_mountain_discovery_job_yaml }}] *****
Wednesday 13 November 2019  10:17:24 -0600 (0:00:00.080)       0:00:00.182 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Delete previous job if exists _raw_params=kubectl -n services delete -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:17:25 -0600 (0:00:00.885)       0:00:01.067 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file src=hms-mountain-discovery-job.yaml.j2, dest={{ cray_hms_mountain_discovery_job_yaml }}] ***
Wednesday 13 November 2019  10:17:25 -0600 (0:00:00.818)       0:00:01.885 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Start HMS mountain discovery job _raw_params=kubectl -n services apply -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:17:27 -0600 (0:00:01.515)       0:00:03.401 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Wait for discovery verify to complete _raw_params=kubectl -n services get jobs cray-hms-mountain-discovery -o jsonpath="{.status.conditions[0].type}"] ***
Wednesday 13 November 2019  10:17:28 -0600 (0:00:00.774)       0:00:04.175 ****
FAILED - RETRYING: Wait for discovery verify to complete (120 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (119 retries left).
changed: [sms01-nmn -> sms01-nmn]

PLAY RECAP ***********************************************************************************************************
sms01-nmn                  : ok=6    changed=3    unreachable=0    failed=0

Wednesday 13 November 2019  10:18:30 -0600 (0:01:01.974)       0:01:06.149 ****
===============================================================================
mountain-discovery : Wait for discovery verify to complete --------------------------------------------------- 61.97s
mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file ----------------------------------- 1.52s
mountain-discovery : Look for hms-mountain-discovery yaml ----------------------------------------------------- 0.89s
mountain-discovery : Delete previous job if exists ------------------------------------------------------------ 0.82s
mountain-discovery : Start HMS mountain discovery job --------------------------------------------------------- 0.77s
docker : Set fact for cray_stack_registry_source -------------------------------------------------------------- 0.08s
```

# dump the k8s logs

```
jolt1-sms01-nmn:~ # kubectl -n services logs cray-hms-mountain-discovery-95vr9 cray-hms-mountain-discovery
2019-11-13T16:17:37Z-INFO-Starting Mountain Discovery Helper
2019-11-13T16:17:37Z-INFO-LOG_LEVEL: DEBUG; value: 10
2019-11-13T16:17:37Z-INFO-Configuring HSM connection: {'HSM_PROTOCOL': 'http://', 'HSM_HOST_WITH_PORT': 'cray-smd', 'HSM_BASE_PATH': '/hsm/v1'}
2019-11-13T16:17:37Z-INFO-Configuring SLS connection: {'SLS_PROTOCOL': 'http://', 'SLS_HOST_WITH_PORT': 'cray-sls', 'SLS_BASE_PATH': ''}
2019-11-13T16:17:37Z-INFO-Configuring CAPMC connection: {'CAPMC_PROTOCOL': 'http://', 'CAPMC_HOST_WITH_PORT': 'cray-capmc', 'CAPMC_BASE_PATH': '/capmc/v1'}
2019-11-13T16:17:37Z-INFO-Configuring requests library ssl connection to use trusted connection: False
2019-11-13T16:17:37Z-INFO-Retrieving list of StateComponents ['Chassis', 'ComputeModule', 'RouterModule'] from HSM
2019-11-13T16:17:37Z-DEBUG-preparing request url: http://cray-smd/hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule
2019-11-13T16:17:37Z-DEBUG-Starting new HTTP connection (1): cray-smd:80
2019-11-13T16:17:37Z-DEBUG-http://cray-smd:80 "GET /hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule HTTP/1.1" 200 None
2019-11-13T16:17:37Z-DEBUG-Retrieved StateComponents from HMS
2019-11-13T16:17:37Z-INFO-targeted hardware: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:17:37Z-INFO-Retrieving xname power state from CAPMC: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:17:37Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:17:37Z-DEBUG-payload: {"xnames": ["x5000c3", "x5000c1r5", "x5000c1r1", "x5000c1", "x5000c1s1", "x5000c1r3", "x5000c1s0", "x5000c1r7"]}
2019-11-13T16:17:37Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:17:37Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 120
2019-11-13T16:17:37Z-DEBUG-Retrieved xname power state from CAPMC: {"e": 0, "err_msg": "", "on": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s0", "x5000c1s1", "x5000c3"]}
2019-11-13T16:17:37Z-INFO-No xnames are in 'off' state; skipping power on attempt!
2019-11-13T16:17:37Z-INFO-Operation Summary:
2019-11-13T16:17:37Z-INFO-Targeted hardware types: 	 ['Chassis', 'ComputeModule', 'RouterModule']
2019-11-13T16:17:37Z-INFO-HSM identified count of targeted hardware: 	 8
2019-11-13T16:17:37Z-DEBUG-HSM identified population of targeted hardware: 	 ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:17:37Z-INFO-Count of xnames for power on: 	 0
2019-11-13T16:17:37Z-DEBUG-Targeted population of xnames for power on: 	 []
2019-11-13T16:17:37Z-INFO-Count of xnames successfully powered on: 	 0
2019-11-13T16:17:37Z-DEBUG-Targeted population of xnames successfully powered on: 	 []
```

# neat trick -> you can use the app label to get the logs (partially)

```
jolt1-sms01-nmn:~ # kubectl -n services logs -l app=cray-hms-mountain-discovery -c cray-hms-mountain-discovery
2019-11-13T16:17:37Z-DEBUG-Retrieved xname power state from CAPMC: {"e": 0, "err_msg": "", "on": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s0", "x5000c1s1", "x5000c3"]}
2019-11-13T16:17:37Z-INFO-No xnames are in 'off' state; skipping power on attempt!
2019-11-13T16:17:37Z-INFO-Operation Summary:
2019-11-13T16:17:37Z-INFO-Targeted hardware types: 	 ['Chassis', 'ComputeModule', 'RouterModule']
2019-11-13T16:17:37Z-INFO-HSM identified count of targeted hardware: 	 8
2019-11-13T16:17:37Z-DEBUG-HSM identified population of targeted hardware: 	 ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:17:37Z-INFO-Count of xnames for power on: 	 0
2019-11-13T16:17:37Z-DEBUG-Targeted population of xnames for power on: 	 []
2019-11-13T16:17:37Z-INFO-Count of xnames successfully powered on: 	 0
2019-11-13T16:17:37Z-DEBUG-Targeted population of xnames successfully powered on: 	 []
```

# now we will power off x5000c1; which will take its children with it.

```
jolt1-sms01-nmn:~ # cray capmc xname_off create --xnames x5000c[1,3] --force=true -vvv  --format json
Loaded token: /root/.config/cray/tokens/api_gw_service_nmn_local.uastest
<cray.auth.AuthUsername object at 0x7f73f22a5090>
REQUEST: POST to https://api-gw-service-nmn.local/apis/capmc/capmc/v1/xname_off
OPTIONS: {'verify': False, 'json': {u'force': True, u'xnames': [u'x5000c1', u'x5000c3']}}
{
  "e": 0,
  "err_msg": ""
}
```

# capmc reports the chassis are off

```
jolt1-sms01-nmn:~ # cray capmc get_xname_status create --xnames x5000c[1,3]
e = 0
err_msg = ""
off = [ "x5000c1", "x5000c3",]

```

```
jolt1-sms01-nmn:~ # cray capmc get_xname_status create --xnames x5000c[1,3],x5000c1s[0-1],x5000c1r[1,3,5,7] -vvvv --format json
Loaded token: /root/.config/cray/tokens/api_gw_service_nmn_local.uastest
<cray.auth.AuthUsername object at 0x7f8e2089f350>
REQUEST: POST to https://api-gw-service-nmn.local/apis/capmc/capmc/v1/get_xname_status
OPTIONS: {'verify': False, 'json': {u'xnames': [u'x5000c1', u'x5000c3', u'x5000c1s0', u'x5000c1s1', u'x5000c1r1', u'x5000c1r3', u'x5000c1r5', u'x5000c1r7']}}
{
  "e": 0,
  "err_msg": "",
  "off": [
    "x5000c1",
    "x5000c1r1",
    "x5000c1r3",
    "x5000c1r5",
    "x5000c1r7",
    "x5000c1s0",
    "x5000c1s1",
    "x5000c3"
  ]
}
```

# now lets use the ansible to turn it back on!

```
jolt1-sms01-nmn:/opt/cray/crayctl/ansible_framework/main # ansible-playbook mountain-discovery.yml

PLAY [bis[0]] ********************************************************************************************************

TASK [docker : Set fact for cray_stack_registry_source cray_stack_registry_source={{ registries[cray_docker_registry_image_source]['fqdn'] }}:{{ registries[cray_docker_registry_image_source]['port'] }}] ***
Wednesday 13 November 2019  10:30:47 -0600 (0:00:00.106)       0:00:00.106 ****
ok: [sms01-nmn]

TASK [mountain-discovery : Look for hms-mountain-discovery yaml path={{ cray_hms_mountain_discovery_job_yaml }}] *****
Wednesday 13 November 2019  10:30:47 -0600 (0:00:00.080)       0:00:00.187 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Delete previous job if exists _raw_params=kubectl -n services delete -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:30:48 -0600 (0:00:00.878)       0:00:01.065 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file src=hms-mountain-discovery-job.yaml.j2, dest={{ cray_hms_mountain_discovery_job_yaml }}] ***
Wednesday 13 November 2019  10:30:49 -0600 (0:00:00.855)       0:00:01.921 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Start HMS mountain discovery job _raw_params=kubectl -n services apply -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:30:50 -0600 (0:00:01.504)       0:00:03.425 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Wait for discovery verify to complete _raw_params=kubectl -n services get jobs cray-hms-mountain-discovery -o jsonpath="{.status.conditions[0].type}"] ***
Wednesday 13 November 2019  10:30:51 -0600 (0:00:00.871)       0:00:04.296 ****
FAILED - RETRYING: Wait for discovery verify to complete (120 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (119 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (118 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (117 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (116 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (115 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (114 retries left).
changed: [sms01-nmn -> sms01-nmn]

PLAY RECAP ***********************************************************************************************************
sms01-nmn                  : ok=6    changed=3    unreachable=0    failed=0

Wednesday 13 November 2019  10:34:26 -0600 (0:03:34.996)       0:03:39.292 ****
===============================================================================
mountain-discovery : Wait for discovery verify to complete -------------------------------------------------- 215.00s
mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file ----------------------------------- 1.50s
mountain-discovery : Look for hms-mountain-discovery yaml ----------------------------------------------------- 0.88s
mountain-discovery : Start HMS mountain discovery job --------------------------------------------------------- 0.87s
mountain-discovery : Delete previous job if exists ------------------------------------------------------------ 0.86s
docker : Set fact for cray_stack_registry_source -------------------------------------------------------------- 0.08s
Playbook run took 0 days, 0 hours, 3 minutes, 39 seconds
```

# and dump the logs:

```
jolt1-sms01-nmn:~ # kubectl -n services logs cray-hms-mountain-discovery-bfrrn cray-hms-mountain-discovery
2019-11-13T16:31:01Z-INFO-Starting Mountain Discovery Helper
2019-11-13T16:31:01Z-INFO-LOG_LEVEL: DEBUG; value: 10
2019-11-13T16:31:01Z-INFO-Configuring HSM connection: {'HSM_PROTOCOL': 'http://', 'HSM_HOST_WITH_PORT': 'cray-smd', 'HSM_BASE_PATH': '/hsm/v1'}
2019-11-13T16:31:01Z-INFO-Configuring SLS connection: {'SLS_PROTOCOL': 'http://', 'SLS_HOST_WITH_PORT': 'cray-sls', 'SLS_BASE_PATH': ''}
2019-11-13T16:31:01Z-INFO-Configuring CAPMC connection: {'CAPMC_PROTOCOL': 'http://', 'CAPMC_HOST_WITH_PORT': 'cray-capmc', 'CAPMC_BASE_PATH': '/capmc/v1'}
2019-11-13T16:31:01Z-INFO-Configuring requests library ssl connection to use trusted connection: False
2019-11-13T16:31:01Z-INFO-Retrieving list of StateComponents ['Chassis', 'ComputeModule', 'RouterModule'] from HSM
2019-11-13T16:31:01Z-DEBUG-preparing request url: http://cray-smd/hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule
2019-11-13T16:31:01Z-DEBUG-Starting new HTTP connection (1): cray-smd:80
2019-11-13T16:31:01Z-DEBUG-http://cray-smd:80 "GET /hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule HTTP/1.1" 200 None
2019-11-13T16:31:01Z-DEBUG-Retrieved StateComponents from HMS
2019-11-13T16:31:01Z-INFO-targeted hardware: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:31:01Z-INFO-Retrieving xname power state from CAPMC: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:31:01Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:31:01Z-DEBUG-payload: {"xnames": ["x5000c3", "x5000c1r5", "x5000c1r1", "x5000c1", "x5000c1s1", "x5000c1r3", "x5000c1s0", "x5000c1r7"]}
2019-11-13T16:31:01Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:31:01Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 121
2019-11-13T16:31:01Z-DEBUG-Retrieved xname power state from CAPMC: {"e": 0, "err_msg": "", "off": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s0", "x5000c1s1", "x5000c3"]}
2019-11-13T16:31:01Z-INFO-targeted xname for power on: ['x5000c1', 'x5000c1r1', 'x5000c1r3', 'x5000c1r5', 'x5000c1r7', 'x5000c1s0', 'x5000c1s1', 'x5000c3']
2019-11-13T16:31:01Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/xname_on
2019-11-13T16:31:01Z-DEBUG-payload: {"xnames": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s0", "x5000c1s1", "x5000c3"], "reason": "power on to facilitate mountain discovery"}
2019-11-13T16:31:01Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:32:46Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/xname_on HTTP/1.1" 200 21
2019-11-13T16:32:46Z-INFO-Sleeping for 30 seconds before attempting to verify power state
2019-11-13T16:33:16Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:33:16Z-DEBUG-payload: {"xnames": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s0", "x5000c1s1", "x5000c3"]}
2019-11-13T16:33:16Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:33:16Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 120
2019-11-13T16:33:16Z-INFO-Power on successfully applied to: ['x5000c1', 'x5000c1r1', 'x5000c1r3', 'x5000c1r5', 'x5000c1r7', 'x5000c1s0', 'x5000c1s1', 'x5000c3']
2019-11-13T16:33:16Z-INFO-Operation Summary:
2019-11-13T16:33:16Z-INFO-Targeted hardware types: 	 ['Chassis', 'ComputeModule', 'RouterModule']
2019-11-13T16:33:16Z-INFO-HSM identified count of targeted hardware: 	 8
2019-11-13T16:33:16Z-DEBUG-HSM identified population of targeted hardware: 	 ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:33:16Z-INFO-Count of xnames for power on: 	 8
2019-11-13T16:33:16Z-DEBUG-Targeted population of xnames for power on: 	 ['x5000c1', 'x5000c1r1', 'x5000c1r3', 'x5000c1r5', 'x5000c1r7', 'x5000c1s0', 'x5000c1s1', 'x5000c3']
2019-11-13T16:33:16Z-INFO-Count of xnames successfully powered on: 	 8
2019-11-13T16:33:16Z-DEBUG-Targeted population of xnames successfully powered on: 	 ['x5000c1', 'x5000c1r1', 'x5000c1r3', 'x5000c1r5', 'x5000c1r7', 'x5000c1s0', 'x5000c1s1', 'x5000c3']
```

# double check with CAPMC

```
jolt1-sms01-nmn:~ # cray capmc get_xname_status create --xnames x5000c[1,3],x5000c1s[0-1],x5000c1r[1,3,5,7] -vvvv --format json
Loaded token: /root/.config/cray/tokens/api_gw_service_nmn_local.uastest
<cray.auth.AuthUsername object at 0x7f271e147350>
REQUEST: POST to https://api-gw-service-nmn.local/apis/capmc/capmc/v1/get_xname_status
OPTIONS: {'verify': False, 'json': {u'xnames': [u'x5000c1', u'x5000c3', u'x5000c1s0', u'x5000c1s1', u'x5000c1r1', u'x5000c1r3', u'x5000c1r5', u'x5000c1r7']}}
{
  "e": 0,
  "err_msg": "",
  "on": [
    "x5000c1",
    "x5000c1r1",
    "x5000c1r3",
    "x5000c1r5",
    "x5000c1r7",
    "x5000c1s0",
    "x5000c1s1",
    "x5000c3"
  ]
}
```

# turn the system over for use

# power on the system

```
jolt1-sms01-nmn:~ # cray capmc xname_on create --xnames x5000c[1,3] --recursive true -vvv --format json
Loaded token: /root/.config/cray/tokens/api_gw_service_nmn_local.uastest
<cray.auth.AuthUsername object at 0x7f56b8ce7090>
REQUEST: POST to https://api-gw-service-nmn.local/apis/capmc/capmc/v1/xname_on
OPTIONS: {'verify': False, 'json': {u'recursive': True, u'xnames': [u'x5000c1', u'x5000c3']}}
{
  "e": 0,
  "err_msg": ""
}
```

# pushed a code change, verify it works

```
jolt1-sms01-nmn:/opt/cray/crayctl/ansible_framework/main # ansible-playbook mountain-discovery.yml

PLAY [bis[0]] ********************************************************************************************************

TASK [docker : Set fact for cray_stack_registry_source cray_stack_registry_source={{ registries[cray_docker_registry_image_source]['fqdn'] }}:{{ registries[cray_docker_registry_image_source]['port'] }}] ***
Wednesday 13 November 2019  10:53:49 -0600 (0:00:00.103)       0:00:00.103 ****
ok: [sms01-nmn]

TASK [mountain-discovery : Look for hms-mountain-discovery yaml path={{ cray_hms_mountain_discovery_job_yaml }}] *****
Wednesday 13 November 2019  10:53:49 -0600 (0:00:00.083)       0:00:00.186 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Delete previous job if exists _raw_params=kubectl -n services delete -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:53:50 -0600 (0:00:00.925)       0:00:01.112 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file src=hms-mountain-discovery-job.yaml.j2, dest={{ cray_hms_mountain_discovery_job_yaml }}] ***
Wednesday 13 November 2019  10:53:51 -0600 (0:00:00.821)       0:00:01.934 ****
ok: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Start HMS mountain discovery job _raw_params=kubectl -n services apply -f "{{ cray_hms_mountain_discovery_job_yaml }}"] ***
Wednesday 13 November 2019  10:53:53 -0600 (0:00:01.493)       0:00:03.428 ****
changed: [sms01-nmn -> sms01-nmn]

TASK [mountain-discovery : Wait for discovery verify to complete _raw_params=kubectl -n services get jobs cray-hms-mountain-discovery -o jsonpath="{.status.conditions[0].type}"] ***
Wednesday 13 November 2019  10:53:54 -0600 (0:00:00.890)       0:00:04.318 ****
FAILED - RETRYING: Wait for discovery verify to complete (120 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (119 retries left).
FAILED - RETRYING: Wait for discovery verify to complete (118 retries left).
changed: [sms01-nmn -> sms01-nmn]

PLAY RECAP ***********************************************************************************************************
sms01-nmn                  : ok=6    changed=3    unreachable=0    failed=0

Wednesday 13 November 2019  10:55:26 -0600 (0:01:32.506)       0:01:36.825 ****
===============================================================================
mountain-discovery : Wait for discovery verify to complete --------------------------------------------------- 92.51s
mountain-discovery : Create cray-hms-mountain-discovery-job Kubernetes file ----------------------------------- 1.49s
mountain-discovery : Look for hms-mountain-discovery yaml ----------------------------------------------------- 0.93s
mountain-discovery : Start HMS mountain discovery job --------------------------------------------------------- 0.89s
mountain-discovery : Delete previous job if exists ------------------------------------------------------------ 0.82s
docker : Set fact for cray_stack_registry_source -------------------------------------------------------------- 0.08s
Playbook run took 0 days, 0 hours, 1 minutes, 36 seconds
```

```
jolt1-sms01-nmn:~ # kubectl -n services logs cray-hms-mountain-discovery-bhcjh cray-hms-mountain-discovery
2019-11-13T16:54:03Z-INFO-Starting Mountain Discovery Helper
2019-11-13T16:54:03Z-INFO-LOG_LEVEL: DEBUG; value: 10
2019-11-13T16:54:03Z-INFO-Configuring HSM connection: {'HSM_PROTOCOL': 'http://', 'HSM_HOST_WITH_PORT': 'cray-smd', 'HSM_BASE_PATH': '/hsm/v1'}
2019-11-13T16:54:03Z-INFO-Configuring SLS connection: {'SLS_PROTOCOL': 'http://', 'SLS_HOST_WITH_PORT': 'cray-sls', 'SLS_BASE_PATH': ''}
2019-11-13T16:54:03Z-INFO-Configuring CAPMC connection: {'CAPMC_PROTOCOL': 'http://', 'CAPMC_HOST_WITH_PORT': 'cray-capmc', 'CAPMC_BASE_PATH': '/capmc/v1'}
2019-11-13T16:54:03Z-INFO-Configuring requests library ssl connection to use trusted connection: False
2019-11-13T16:54:03Z-INFO-Retrieving list of StateComponents ['Chassis', 'ComputeModule', 'RouterModule'] from HSM
2019-11-13T16:54:03Z-DEBUG-preparing request url: http://cray-smd/hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule
2019-11-13T16:54:03Z-DEBUG-Starting new HTTP connection (1): cray-smd:80
2019-11-13T16:54:03Z-DEBUG-http://cray-smd:80 "GET /hsm/v1/State/Components?type=Chassis&type=ComputeModule&type=RouterModule HTTP/1.1" 200 None
2019-11-13T16:54:03Z-DEBUG-Retrieved StateComponents from HSM
2019-11-13T16:54:03Z-INFO-targeted hardware: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:54:03Z-INFO-Retrieving xname power state from CAPMC: ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:54:03Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:54:03Z-DEBUG-payload: {"xnames": ["x5000c3", "x5000c1r5", "x5000c1r1", "x5000c1", "x5000c1s1", "x5000c1r3", "x5000c1s0", "x5000c1r7"]}
2019-11-13T16:54:03Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:54:04Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 128
2019-11-13T16:54:04Z-DEBUG-Retrieved xname power state from CAPMC: {"e": 0, "err_msg": "", "on": ["x5000c1", "x5000c1r1", "x5000c1r3", "x5000c1r5", "x5000c1r7", "x5000c1s1", "x5000c3"], "off": ["x5000c1s0"]}
2019-11-13T16:54:04Z-INFO-targeted xname for power on: ['x5000c1s0']
2019-11-13T16:54:04Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/xname_on
2019-11-13T16:54:04Z-DEBUG-payload: {"xnames": ["x5000c1s0"], "reason": "power on to facilitate mountain discovery"}
2019-11-13T16:54:04Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:54:11Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/xname_on HTTP/1.1" 200 21
2019-11-13T16:54:11Z-INFO-Sleeping for 30 seconds before attempting to verify power state
2019-11-13T16:54:41Z-DEBUG-preparing request url: http://cray-capmc/capmc/v1/get_xname_status
2019-11-13T16:54:41Z-DEBUG-payload: {"xnames": ["x5000c1s0"]}
2019-11-13T16:54:41Z-DEBUG-Starting new HTTP connection (1): cray-capmc:80
2019-11-13T16:54:41Z-DEBUG-http://cray-capmc:80 "POST /capmc/v1/get_xname_status HTTP/1.1" 200 40
2019-11-13T16:54:41Z-INFO-Power on successfully applied to: ['x5000c1s0']
2019-11-13T16:54:41Z-INFO-Operation Summary:
2019-11-13T16:54:41Z-INFO-Targeted hardware types: 	 ['Chassis', 'ComputeModule', 'RouterModule']
2019-11-13T16:54:41Z-INFO-HSM identified count of targeted hardware: 	 8
2019-11-13T16:54:41Z-DEBUG-HSM identified population of targeted hardware: 	 ['x5000c3', 'x5000c1r5', 'x5000c1r1', 'x5000c1', 'x5000c1s1', 'x5000c1r3', 'x5000c1s0', 'x5000c1r7']
2019-11-13T16:54:41Z-INFO-Count of xnames for power on: 	 1
2019-11-13T16:54:41Z-DEBUG-Targeted population of xnames for power on: 	 ['x5000c1s0']
2019-11-13T16:54:41Z-INFO-Count of xnames successfully powered on: 	 1
2019-11-13T16:54:41Z-DEBUG-Targeted population of xnames successfully powered on: 	 ['x5000c1s0']
```

# run unit tests locally, it works

```
9:52:42 anieuwsma@C02YL0TJJGH7 hms-mountain-discovery feature/CASMHMS-2307-fc-mountain-automatic-power-cycling-for-discovery ?docker-compose up --build --abort-on-container-exitt


Building cray-smd
Step 1/8 : FROM python:3.7-alpine
 ---> 828bce60a61c
Step 2/8 : COPY requirements.txt /
 ---> Using cache
 ---> e826ef594cff
Step 3/8 : RUN pip3 install -r /requirements.txt
 ---> Using cache
 ---> fe184fa222a1
Step 4/8 : COPY . /app
 ---> Using cache
 ---> 9a8564d48bd1
Step 5/8 : WORKDIR /app
 ---> Using cache
 ---> 4dac69c9ebe8
Step 6/8 : EXPOSE 27779
 ---> Using cache
 ---> b190245965cc
Step 7/8 : ENTRYPOINT ["python"]
 ---> Using cache
 ---> 9d922537d486
Step 8/8 : CMD ["app.py"]
 ---> Using cache
 ---> f6be64e6358b
Successfully built f6be64e6358b
Successfully tagged hms-mountain-discovery_cray-smd:latest
Building cray-sls
Step 1/8 : FROM python:3.7-alpine
 ---> 828bce60a61c
Step 2/8 : COPY requirements.txt /
 ---> Using cache
 ---> a979dbb0b906
Step 3/8 : RUN pip3 install -r /requirements.txt
 ---> Using cache
 ---> 67e9e78374aa
Step 4/8 : COPY . /app
 ---> Using cache
 ---> 8c73b4e40c3a
Step 5/8 : WORKDIR /app
 ---> Using cache
 ---> 7027107a87b2
Step 6/8 : EXPOSE 8376
 ---> Using cache
 ---> dc45b136a9d2
Step 7/8 : ENTRYPOINT ["python"]
 ---> Using cache
 ---> 3bcddaf3bcf4
Step 8/8 : CMD ["app.py"]
 ---> Using cache
 ---> bbdbb19089d5
Successfully built bbdbb19089d5
Successfully tagged hms-mountain-discovery_cray-sls:latest
Building cray-capmc
Step 1/10 : FROM python:3.7-alpine
 ---> 828bce60a61c
Step 2/10 : COPY requirements.txt /
 ---> Using cache
 ---> e826ef594cff
Step 3/10 : RUN pip3 install -r /requirements.txt
 ---> Using cache
 ---> fe184fa222a1
Step 4/10 : RUN apk add curl
 ---> Using cache
 ---> 6c8dc9285d20
Step 5/10 : COPY . /app
 ---> Using cache
 ---> f275cdadad2c
Step 6/10 : WORKDIR /app
 ---> Using cache
 ---> d0ced7b8b5fb
Step 7/10 : ENV LOG_LEVEL DEBUG
 ---> Using cache
 ---> dcfa3a575e20
Step 8/10 : EXPOSE 37777
 ---> Using cache
 ---> 3eb24c06c5cd
Step 9/10 : ENTRYPOINT ["python"]
 ---> Using cache
 ---> 95db1ae438be
Step 10/10 : CMD ["app.py"]
 ---> Using cache
 ---> 7db6ffe83805
Successfully built 7db6ffe83805
Successfully tagged hms-mountain-discovery_cray-capmc:latest
Building rediscovery
Step 1/16 : FROM python:3.7-alpine
 ---> 828bce60a61c
Step 2/16 : COPY src/requirements.txt /
 ---> Using cache
 ---> fcedcbe552d9
Step 3/16 : RUN pip install --upgrade pip setuptools
 ---> Using cache
 ---> 4b739b3639a7
Step 4/16 : RUN pip3 install -r /requirements.txt
 ---> Using cache
 ---> 9d3ce1bf22af
Step 5/16 : RUN apk add --no-cache curl
 ---> Using cache
 ---> 9cc4f9dd5aff
Step 6/16 : COPY src /app
 ---> b8f5028a6207
Step 7/16 : WORKDIR /app
 ---> Running in ef5f31663b32
Removing intermediate container ef5f31663b32
 ---> 247b6e9545a9
Step 8/16 : ENV LOG_LEVEL DEBUG
 ---> Running in 284dd2ff8bc6
Removing intermediate container 284dd2ff8bc6
 ---> 3ce9a6f6d76a
Step 9/16 : ENV HSM_PROTOCOL http://
 ---> Running in 96c6a0f9a990
Removing intermediate container 96c6a0f9a990
 ---> 3229a393fc0d
Step 10/16 : ENV HSM_HOST_WITH_PORT cray-smd
 ---> Running in 105e6c734484
Removing intermediate container 105e6c734484
 ---> c26d3cda7bd4
Step 11/16 : ENV SLS_PROTOCOL http://
 ---> Running in 23ecf79d5870
Removing intermediate container 23ecf79d5870
 ---> 28ec9b263c86
Step 12/16 : ENV SLS_HOST_WITH_PATH sls
 ---> Running in b7a5b364a3c2
Removing intermediate container b7a5b364a3c2
 ---> 703eed65c794
Step 13/16 : ENV SLEEP_LENGTH 30
 ---> Running in b5bd0443b676
Removing intermediate container b5bd0443b676
 ---> cf0da2b80c0f
Step 14/16 : ENV FEATURE_FLAG_SLS True
 ---> Running in d4edaeec9e74
Removing intermediate container d4edaeec9e74
 ---> 91f39605eaa5
Step 15/16 : ENTRYPOINT ["python"]
 ---> Running in 2bf6d3369e9a
Removing intermediate container 2bf6d3369e9a
 ---> ef8305254d74
Step 16/16 : CMD ["mountain_discovery.py"]
 ---> Running in a22a2bdc3d2b
Removing intermediate container a22a2bdc3d2b
 ---> a1553336ec4d
Successfully built a1553336ec4d
Successfully tagged hms-mountain-discovery_rediscovery:latest
Starting hms-mountain-discovery_cray-capmc_1 ... done
Starting hms-mountain-discovery_cray-sls_1   ... done
Starting hms-mountain-discovery_cray-smd_1   ... done
Recreating hms-mountain-discovery_rediscovery_1 ... done
Attaching to hms-mountain-discovery_cray-capmc_1, hms-mountain-discovery_cray-smd_1, hms-mountain-discovery_cray-sls_1, hms-mountain-discovery_rediscovery_1
cray-capmc_1   | 2019-11-13T16:56:03Z-INFO-Starting Synthetic-CAPMC
cray-capmc_1   | 2019-11-13T16:56:03Z-INFO-LOG_LEVEL: DEBUG; value: 10
cray-sls_1     | 2019-11-13T16:56:03Z-INFO-Starting Synthetic-CAPMC
cray-sls_1     | 2019-11-13T16:56:03Z-INFO-LOG_LEVEL: DEBUG; value: 10
cray-smd_1     | 2019-11-13T16:56:03Z-INFO-Starting Synthetic-HSM
cray-smd_1     | 2019-11-13T16:56:03Z-INFO-LOG_LEVEL: DEBUG; value: 10
cray-capmc_1   |  * Serving Flask app "app" (lazy loading)
cray-capmc_1   |  * Environment: production
cray-capmc_1   |    WARNING: This is a development server. Do not use it in a production deployment.
cray-capmc_1   |    Use a production WSGI server instead.
cray-capmc_1   |  * Debug mode: off
cray-smd_1     |  * Serving Flask app "app" (lazy loading)
cray-smd_1     |  * Environment: production
cray-smd_1     |    WARNING: This is a development server. Do not use it in a production deployment.
cray-smd_1     |    Use a production WSGI server instead.
cray-smd_1     |  * Debug mode: off
cray-sls_1     | 2019-11-13T16:56:03Z-INFO- * Running on http://0.0.0.0:8376/ (Press CTRL+C to quit)
cray-capmc_1   | 2019-11-13T16:56:03Z-INFO- * Running on http://0.0.0.0:37777/ (Press CTRL+C to quit)
cray-smd_1     | 2019-11-13T16:56:03Z-INFO- * Running on http://0.0.0.0:27779/ (Press CTRL+C to quit)
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Starting Mountain Discovery Helper
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-LOG_LEVEL: DEBUG; value: 10
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Configuring HSM connection: {'HSM_PROTOCOL': 'http://', 'HSM_HOST_WITH_PORT': 'cray-smd:27779', 'HSM_BASE_PATH': ''}
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Configuring SLS connection: {'SLS_PROTOCOL': 'http://', 'SLS_HOST_WITH_PORT': 'cray-sls:8376', 'SLS_BASE_PATH': ''}
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Configuring CAPMC connection: {'CAPMC_PROTOCOL': 'http://', 'CAPMC_HOST_WITH_PORT': 'cray-capmc:37777', 'CAPMC_BASE_PATH': ''}
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Configuring requests library ssl connection to use trusted connection: False
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Retrieving list of StateComponents ['Chassis', 'ComputeModule', 'RouterModule'] from HSM
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-preparing request url: http://cray-smd:27779/State/Components?type=Chassis&type=ComputeModule&type=RouterModule
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-Starting new HTTP connection (1): cray-smd:27779
cray-smd_1     | 2019-11-13T16:56:04Z-INFO-172.19.0.5 - - [13/Nov/2019 16:56:04] "GET /State/Components?type=Chassis&type=ComputeModule&type=RouterModule HTTP/1.1" 200 -
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-http://cray-smd:27779 "GET /State/Components?type=Chassis&type=ComputeModule&type=RouterModule HTTP/1.1" 200 7001
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-Retrieved StateComponents from HSM
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-targeted hardware: ['x1000c5s4', 'x1000c5s6', 'x1000c5r7', 'x1000c5r3', 'x1000c5s3', 'x1000c5s5', 'x1000c5s1', 'x1000c5s2', 'x1000c5s7', 'x1000c5', 'x1000c4s3', 'x1000c4s6', 'x1000c4s0', 'x1000c4s5', 'x1000c4r7', 'x1000c4s4', 'x1000c4', 'x1000c4r3', 'x1000c4s1', 'x1000c4s2', 'x1000c7s0', 'x1000c7', 'x1000c7r3', 'x1000c7s1', 'x1000c7r7', 'x1000c1s0', 'x1000c1', 'x1000c1r3', 'x1000c1s1', 'x1000c1r7', 'x1000c2s1', 'x1000c2s2', 'x1000c2s4', 'x1000c2s6', 'x1000c2s5', 'x1000c2', 'x1000c2r7', 'x1000c2s0', 'x1000c2s3', 'x1000c2r3', 'x1000c3', 'x1000c3s0', 'x1000c3s1', 'x1000c3r3', 'x1000c3r7', 'x1000c6r7', 'x1000c6s1', 'x1000c6r3', 'x1000c6s0', 'x1000c6', 'x1000c0', 'x1000c0s1', 'x1000c0r7', 'x1000c0s0', 'x1000c0r3']
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Retrieving xname power state from CAPMC: ['x1000c5s4', 'x1000c5s6', 'x1000c5r7', 'x1000c5r3', 'x1000c5s3', 'x1000c5s5', 'x1000c5s1', 'x1000c5s2', 'x1000c5s7', 'x1000c5', 'x1000c4s3', 'x1000c4s6', 'x1000c4s0', 'x1000c4s5', 'x1000c4r7', 'x1000c4s4', 'x1000c4', 'x1000c4r3', 'x1000c4s1', 'x1000c4s2', 'x1000c7s0', 'x1000c7', 'x1000c7r3', 'x1000c7s1', 'x1000c7r7', 'x1000c1s0', 'x1000c1', 'x1000c1r3', 'x1000c1s1', 'x1000c1r7', 'x1000c2s1', 'x1000c2s2', 'x1000c2s4', 'x1000c2s6', 'x1000c2s5', 'x1000c2', 'x1000c2r7', 'x1000c2s0', 'x1000c2s3', 'x1000c2r3', 'x1000c3', 'x1000c3s0', 'x1000c3s1', 'x1000c3r3', 'x1000c3r7', 'x1000c6r7', 'x1000c6s1', 'x1000c6r3', 'x1000c6s0', 'x1000c6', 'x1000c0', 'x1000c0s1', 'x1000c0r7', 'x1000c0s0', 'x1000c0r3']
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-preparing request url: http://cray-capmc:37777/get_xname_status
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-payload: {"xnames": ["x1000c5s4", "x1000c5s6", "x1000c5r7", "x1000c5r3", "x1000c5s3", "x1000c5s5", "x1000c5s1", "x1000c5s2", "x1000c5s7", "x1000c5", "x1000c4s3", "x1000c4s6", "x1000c4s0", "x1000c4s5", "x1000c4r7", "x1000c4s4", "x1000c4", "x1000c4r3", "x1000c4s1", "x1000c4s2", "x1000c7s0", "x1000c7", "x1000c7r3", "x1000c7s1", "x1000c7r7", "x1000c1s0", "x1000c1", "x1000c1r3", "x1000c1s1", "x1000c1r7", "x1000c2s1", "x1000c2s2", "x1000c2s4", "x1000c2s6", "x1000c2s5", "x1000c2", "x1000c2r7", "x1000c2s0", "x1000c2s3", "x1000c2r3", "x1000c3", "x1000c3s0", "x1000c3s1", "x1000c3r3", "x1000c3r7", "x1000c6r7", "x1000c6s1", "x1000c6r3", "x1000c6s0", "x1000c6", "x1000c0", "x1000c0s1", "x1000c0r7", "x1000c0s0", "x1000c0r3"]}
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-Starting new HTTP connection (1): cray-capmc:37777
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-<Request 'http://cray-capmc:37777/get_xname_status' [POST]>
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-json: {'xnames': ['x1000c5s4', 'x1000c5s6', 'x1000c5r7', 'x1000c5r3', 'x1000c5s3', 'x1000c5s5', 'x1000c5s1', 'x1000c5s2', 'x1000c5s7', 'x1000c5', 'x1000c4s3', 'x1000c4s6', 'x1000c4s0', 'x1000c4s5', 'x1000c4r7', 'x1000c4s4', 'x1000c4', 'x1000c4r3', 'x1000c4s1', 'x1000c4s2', 'x1000c7s0', 'x1000c7', 'x1000c7r3', 'x1000c7s1', 'x1000c7r7', 'x1000c1s0', 'x1000c1', 'x1000c1r3', 'x1000c1s1', 'x1000c1r7', 'x1000c2s1', 'x1000c2s2', 'x1000c2s4', 'x1000c2s6', 'x1000c2s5', 'x1000c2', 'x1000c2r7', 'x1000c2s0', 'x1000c2s3', 'x1000c2r3', 'x1000c3', 'x1000c3s0', 'x1000c3s1', 'x1000c3r3', 'x1000c3r7', 'x1000c6r7', 'x1000c6s1', 'x1000c6r3', 'x1000c6s0', 'x1000c6', 'x1000c0', 'x1000c0s1', 'x1000c0r7', 'x1000c0s0', 'x1000c0r3']}
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s4
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s6
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s5
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s2
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5s7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c5
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s6
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s5
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s4
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c4s2
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status off, xname x1000c7s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status off, xname x1000c7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c7r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c7s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c7r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c1s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c1r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c1s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c1r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s2
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s4
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s6
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s5
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2s3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c2r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c3s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c3s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c3r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c3r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c6r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c6s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c6r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c6s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status off, xname x1000c6
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c0s1
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c0r7
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c0s0
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-status on, xname x1000c0r3
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-total_count: 55
cray-capmc_1   | 2019-11-13T16:56:04Z-INFO-172.19.0.5 - - [13/Nov/2019 16:56:04] "POST /get_xname_status HTTP/1.1" 200 -
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-http://cray-capmc:37777 "POST /get_xname_status HTTP/1.1" 200 739
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-Retrieved xname power state from CAPMC: {"e": 0, "err_msg": "", "on": ["x1000c5s4", "x1000c5s6", "x1000c5r7", "x1000c5r3", "x1000c5s3", "x1000c5s5", "x1000c5s1", "x1000c5s2", "x1000c5s7", "x1000c5", "x1000c4s3", "x1000c4s6", "x1000c4s0", "x1000c4s5", "x1000c4r7", "x1000c4s4", "x1000c4", "x1000c4r3", "x1000c4s1", "x1000c4s2", "x1000c7r3", "x1000c7s1", "x1000c7r7", "x1000c1s0", "x1000c1", "x1000c1r3", "x1000c1s1", "x1000c1r7", "x1000c2s1", "x1000c2s2", "x1000c2s4", "x1000c2s6", "x1000c2s5", "x1000c2", "x1000c2r7", "x1000c2s0", "x1000c2s3", "x1000c2r3", "x1000c3", "x1000c3s0", "x1000c3s1", "x1000c3r3", "x1000c3r7", "x1000c6r7", "x1000c6s1", "x1000c6r3", "x1000c6s0", "x1000c0", "x1000c0s1", "x1000c0r7", "x1000c0s0", "x1000c0r3"], "off": ["x1000c7s0", "x1000c7", "x1000c6"]}
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-targeted xname for power on: ['x1000c7s0', 'x1000c7', 'x1000c6']
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-preparing request url: http://cray-capmc:37777/xname_on
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-payload: {"xnames": ["x1000c7s0", "x1000c7", "x1000c6"], "reason": "power on to facilitate mountain discovery"}
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-Starting new HTTP connection (1): cray-capmc:37777
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-<Request 'http://cray-capmc:37777/xname_on' [POST]>
cray-capmc_1   | 2019-11-13T16:56:04Z-DEBUG-json: {'xnames': ['x1000c7s0', 'x1000c7', 'x1000c6'], 'reason': 'power on to facilitate mountain discovery'}
cray-capmc_1   | 2019-11-13T16:56:04Z-INFO-172.19.0.5 - - [13/Nov/2019 16:56:04] "POST /xname_on HTTP/1.1" 200 -
rediscovery_1  | 2019-11-13T16:56:04Z-DEBUG-http://cray-capmc:37777 "POST /xname_on HTTP/1.1" 200 23
rediscovery_1  | 2019-11-13T16:56:04Z-INFO-Sleeping for 1 seconds before attempting to verify power state
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-preparing request url: http://cray-capmc:37777/get_xname_status
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-payload: {"xnames": ["x1000c7s0", "x1000c7", "x1000c6"]}
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Starting new HTTP connection (1): cray-capmc:37777
cray-capmc_1   | 2019-11-13T16:56:05Z-DEBUG-<Request 'http://cray-capmc:37777/get_xname_status' [POST]>
cray-capmc_1   | 2019-11-13T16:56:05Z-DEBUG-json: {'xnames': ['x1000c7s0', 'x1000c7', 'x1000c6']}
cray-capmc_1   | 2019-11-13T16:56:05Z-DEBUG-status on, xname x1000c7s0
cray-capmc_1   | 2019-11-13T16:56:05Z-DEBUG-status on, xname x1000c7
cray-capmc_1   | 2019-11-13T16:56:05Z-DEBUG-status on, xname x1000c6
cray-capmc_1   | 2019-11-13T16:56:05Z-DEBUG-total_count: 3
cray-capmc_1   | 2019-11-13T16:56:05Z-INFO-172.19.0.5 - - [13/Nov/2019 16:56:05] "POST /get_xname_status HTTP/1.1" 200 -
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-http://cray-capmc:37777 "POST /get_xname_status HTTP/1.1" 200 66
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Power on successfully applied to: ['x1000c7s0', 'x1000c7', 'x1000c6']
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Retrieving list of hardware ['comptype_chassis_bmc'] from SLS
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-preparing request url: http://cray-sls:8376/search/hardware?type=comptype_chassis_bmc&class=Mountain
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Starting new HTTP connection (1): cray-sls:8376
cray-sls_1     | 2019-11-13T16:56:05Z-DEBUG-[{'XName': 'x1000c4b0', 'Type': 'comptype_chassis_bmc', 'TypeString': 'ChassisBMC', 'Class': 'Mountain', 'ExtraProperties': {'IP4addr': '10.5.1.100', 'IP6addr': 'DHCPv6', 'Network': 'HMN', 'Password': 'vault://tok', 'Username': 'root', 'TESTING': 'does not exist in HSM, exists in SLS'}}, {'XName': 'x1000c5b0', 'Type': 'comptype_chassis_bmc', 'TypeString': 'ChassisBMC', 'Class': 'Mountain', 'ExtraProperties': {'IP4addr': '10.5.1.100', 'IP6addr': 'DHCPv6', 'Network': 'HMN', 'Password': 'vault://tok', 'Username': 'root', 'TESTING': 'does not exist in HSM, exists in SLS'}}, {'XName': 'x0c0b0', 'Type': 'comptype_chassis_bmc', 'TypeString': 'ChassisBMC', 'Class': 'Mountain', 'ExtraProperties': {'IP4addr': '10.5.1.100', 'IP6addr': 'DHCPv6', 'Network': 'HMN', 'Password': 'vault://tok', 'Username': 'root', 'TESTING': 'does not exist in HSM, exists in SLS'}}]
cray-sls_1     | 2019-11-13T16:56:05Z-INFO-172.19.0.5 - - [13/Nov/2019 16:56:05] "GET /search/hardware?type=comptype_chassis_bmc&class=Mountain HTTP/1.1" 200 -
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-http://cray-sls:8376 "GET /search/hardware?type=comptype_chassis_bmc&class=Mountain HTTP/1.1" 200 1097
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Retrieved ComponentEndpoints from HSM
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Retrieving list of StateComponents ['ChassisBMC'] from HSM
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-preparing request url: http://cray-smd:27779/State/Components?type=ChassisBMC
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Starting new HTTP connection (1): cray-smd:27779
cray-smd_1     | 2019-11-13T16:56:05Z-INFO-172.19.0.5 - - [13/Nov/2019 16:56:05] "GET /State/Components?type=ChassisBMC HTTP/1.1" 200 -
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-http://cray-smd:27779 "GET /State/Components?type=ChassisBMC HTTP/1.1" 200 1072
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Retrieved StateComponents from HSM
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-HSM ChassisBMC(CMM) population: ['x1000c5b0', 'x1000c4b0', 'x1000c7b0', 'x1000c1b0', 'x1000c2b0', 'x1000c3b0', 'x1000c6b0', 'x1000c0b0']
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-SLS ChassisBMC(CMM) population: ['x1000c4b0', 'x1000c5b0', 'x0c0b0']
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-SLS/HSM intersection: ['x1000c5b0', 'x1000c4b0']
rediscovery_1  | 2019-11-13T16:56:05Z-WARNING-HSM minus SLS: ['x1000c7b0', 'x1000c1b0', 'x1000c2b0', 'x1000c3b0', 'x1000c6b0', 'x1000c0b0']
rediscovery_1  | 2019-11-13T16:56:05Z-WARNING-SLS minus HSM: ['x0c0b0']
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Operation Summary:
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Targeted hardware types: 	 ['Chassis', 'ComputeModule', 'RouterModule']
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-HSM identified count of targeted hardware: 	 55
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-HSM identified population of targeted hardware: 	 ['x1000c5s4', 'x1000c5s6', 'x1000c5r7', 'x1000c5r3', 'x1000c5s3', 'x1000c5s5', 'x1000c5s1', 'x1000c5s2', 'x1000c5s7', 'x1000c5', 'x1000c4s3', 'x1000c4s6', 'x1000c4s0', 'x1000c4s5', 'x1000c4r7', 'x1000c4s4', 'x1000c4', 'x1000c4r3', 'x1000c4s1', 'x1000c4s2', 'x1000c7s0', 'x1000c7', 'x1000c7r3', 'x1000c7s1', 'x1000c7r7', 'x1000c1s0', 'x1000c1', 'x1000c1r3', 'x1000c1s1', 'x1000c1r7', 'x1000c2s1', 'x1000c2s2', 'x1000c2s4', 'x1000c2s6', 'x1000c2s5', 'x1000c2', 'x1000c2r7', 'x1000c2s0', 'x1000c2s3', 'x1000c2r3', 'x1000c3', 'x1000c3s0', 'x1000c3s1', 'x1000c3r3', 'x1000c3r7', 'x1000c6r7', 'x1000c6s1', 'x1000c6r3', 'x1000c6s0', 'x1000c6', 'x1000c0', 'x1000c0s1', 'x1000c0r7', 'x1000c0s0', 'x1000c0r3']
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Count of xnames for power on: 	 3
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Targeted population of xnames for power on: 	 ['x1000c7s0', 'x1000c7', 'x1000c6']
rediscovery_1  | 2019-11-13T16:56:05Z-INFO-Count of xnames successfully powered on: 	 3
rediscovery_1  | 2019-11-13T16:56:05Z-DEBUG-Targeted population of xnames successfully powered on: 	 ['x1000c7s0', 'x1000c7', 'x1000c6']
rediscovery_1  | 2019-11-13T16:56:05Z-ERROR-HSM is missing 1 CMM's as identified in SLS, it is possible not all CMMs have been powered on!
rediscovery_1  | 2019-11-13T16:56:05Z-ERROR-SLS minus HSM: ['x0c0b0']
hms-mountain-discovery_rediscovery_1 exited with code 0
Aborting on container exit...
Stopping hms-mountain-discovery_cray-smd_1      ...
Stopping hms-mountain-discovery_cray-capmc_1    ...
Stopping hms-mountain-discovery_cray-sls_1      ...
Killing hms-mountain-discovery_cray-smd_1       ... done
Killing hms-mountain-discovery_cray-capmc_1     ... done
Killing hms-mountain-discovery_cray-sls_1       ... done
```