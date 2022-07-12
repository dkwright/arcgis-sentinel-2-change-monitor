# # Automated Change Monitoring with Sentinel-2 L2A

# ## 02 - Manage Image Services

# #### Connect to the ArcGIS Online organization
from arcgis import GIS
from arcgis.features import FeatureLayerCollection
import getpass
from arcgis.raster.analytics import copy_raster

org_url = "https://cname.domain/portal"
uname = "your_username"
pw = "your_password"
gis = GIS(org_url, uname, pw, verify_cert=False)

# #### Load the Monitoring specification Feature Service
monitoring_aois_item = gis.content.get("the GUID for your Sentinel-2 L2A Monitoring Controls Feature Service") #IRS Enterprise
monitoring_aois_item

# #### Access the layer and query it for the active AOIs
monitoring_aois_layers = monitoring_aois_item.layers
monitoring_aois_layer = monitoring_aois_layers[0]

active_aois = monitoring_aois_layer.query(where="Active='True'",
                                          out_fields='name,description,active,startdate,enddate,lastmoddate,cloudcoverpct,notify,contactemail,imageservice,changeimageservice')
active_aois.sdf

# ### Copy Mosiac Dataset(s) to Image Hosting File Server

# This method transfers the File GeoDataBase to a Linux File Server configured with the Image Hosting Site. 
# Note that a Folder Datastore was configured using the Image Server Manager allow data access to the 
# File Server. Also note that there is a server folder created on the Image Hosting site "change_monitor" 
# that is in use to partition the Image Services created / updated by this code base. 
# The SCP method here passes the user's id_rsa key to authenticate with the Linux File Server. 
# If you are using a Windows host for your Image Hosting storage, please examine OpenSSH 
# to provide SCP capabilities for Windows, or consider an alternative file transfer method.

import subprocess
from datetime import datetime

for feature in active_aois:
    feature_name = feature.attributes["name"]
    # Using a time-stamped FGDB name so we can keep an archive of the Mosiac Datasets on the server
    gdb_name = feature_name + "_" + datetime.utcfromtimestamp(feature.attributes["lastmoddate"] / 1000).strftime("%m_%d_%Y_%H_%M_%S")
    md_name = feature_name
    print(f"Copying File GeoDataBase to server: {gdb_name}")
    print(f"C:\data\sentinel-2-l2a\change_monitor\{gdb_name}.gdb")
        
    if gdb_copy_result.returncode == 0:
        print(f"File GeoDataBase {gdb_name} copied successfully to Image Hosting File Server.")
    else:
        print(f"An error occurred while copying the File GeoDataBase {gdb_name} to Image Hosting File Server. Check that no locks exist on the FGDB(s) and try again.")
    print("File GeoDataBase transfers are complete.")

import requests
from urllib.parse import urlencode
import json
import warnings; warnings.simplefilter('ignore')
from os.path import join

try:
    from ujson import loads, dumps
except:
    from json import loads, dumps

# Function to generate token from ArcGIS Sharing API
def get_token_referer(username,password,portal_url,server_url,referer):
        # Function to get authentication token from portal
        flag = True
        print("Requesting authentication token")
        if flag:
            url = portal_url + '/sharing/rest/generateToken'
            payload = {
                "username": username,
                "password": password,
                "client": "referer",
                "referer": referer,
                "expiration": "120",
                "f": "pjson"
            }
            headers = {
                'Content-Type': "application/x-www-form-urlencoded"
            }
            try:
                response = requests.post(url, data=payload, headers=headers)
                if response.status_code == requests.codes.ok:
                    token = response.json()['token']
                    print(token)
                    return token
                else:
                    return False
                    pass
            except requests.RequestException as e:
                raise e
        else:
            print(server_url + "/rest is not reachable")
            return False


# #### Connect to ArcGIS Enterprise and generate token
portal_url = org_url # "https://cname.domain/portal"
image_url = "https://cname.domain/image" # Federated Image Hosting Site
portal_token = get_token_referer(uname,pw,portal_url,image_url,portal_url + '/sharing/rest')
image_token = get_token_referer(uname,pw,portal_url,image_url,image_url)

# funtion to publish a new Image Service to Image Server using admin REST
def publish_image_service(service_name, service_json):
    url = '{}/admin/services/change_monitor/createService'.format(image_url)
    payload = {"service": json.dumps(service_json)}
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    querystring = {"f": "pjson", "token": image_token}
    try:
        resp = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    except Exception as e:
        print("failure: " + e)

    return resp

# funtion to edit an existing Image Service using admin REST
def edit_image_service(service_name, service_json):
    url = '{0}/admin/services/change_monitor/{1}.ImageServer/edit?'.format(image_url, service_name)
    payload = {"service": json.dumps(service_json)}
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    querystring = {"f": "pjson", "token": image_token}
    try:
        resp = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    except Exception as e:
        print("failure: " + e)

    return resp

# funtions to mange service JSON from a template or from an existing service
def update_service_path(current_path, new_gdb_md, md_name):
    gdb_path = current_path.rsplit('\\', 1)[0]
    path = gdb_path.rsplit('\\', 1)[0]
    updated_service_path = join(path, new_gdb_md, md_name)
    
    return updated_service_path

def create_service_json(service_name, service_exists, gdb_name, md_name):
    if not service_exists:
        # read JSON from a template
        with open(r"service_mgmt\\rest-create-service-s2l2a-template.json", "r") as template_file:
            data = template_file.read()
        obj = loads(data)
        servicename_replaced = dumps(obj).replace("MYSERVICENAME", service_name)
        obj2 = loads(servicename_replaced)
        gdb_replaced = dumps(obj2).replace("GDBNAME", gdb_name)
        obj3 = loads(gdb_replaced)
        md_replaced = dumps(obj3).replace("MDNAME", md_name)
        service_json = loads(md_replaced)
    else:
        # read the existing JSON from the service
        url = '{0}/admin/services/change_monitor/{1}.ImageServer'.format(image_url, service_name, image_token)
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        querystring = {"f": "pjson", "token": image_token}
        try:
            resp = requests.request("GET", url, headers=headers, params=querystring)
        except Exception as e:
            print("failure: " + e)

        current_svc_json = resp.json()
        print("current_svc_json: " + str(type(current_svc_json)))
        current_path = current_svc_json["properties"]["path"]
        new_path = update_service_path(current_path, gdb_name, md_name)
        current_svc_json["properties"]["path"] = new_path
        dumpobj = dumps(current_svc_json)
        service_json = current_svc_json
        
    return service_json

# Functions to start and stop services
def stop_service(image_url, service_name, image_token):
    url = '{0}/admin/services/change_monitor/{1}.ImageServer/stop?f=pjson&token={2}'.format(image_url, service_name, image_token)
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    payload = {}
    try:
        resp = requests.request("POST", url, data=payload, headers=headers)
    except Exception as e:
        print("failure: " + e)
    
    return resp.content

def start_service(image_url, service_name, image_token):
    url = '{0}/admin/services/change_monitor/{1}.ImageServer/start?f=pjson&token={2}'.format(image_url, service_name, image_token)
    headers = {'Content-Type': "application/x-www-form-urlencoded"}
    payload = {}
    try:
        resp = requests.request("POST", url, data=payload, headers=headers)
    except Exception as e:
        print("failure: " + e)

    return resp.content

for feature in active_aois:
    service_name = feature.attributes["name"]
    match_list = gis.content.search(service_name, item_type = "Image Service")
    print("Searching portal for item name: {0}".format(service_name))
    print("Potential matches:")
    print("-----------------")
    for match in match_list:
        print(match.title)
    message = "Service {} does not exist. Publishing...".format(service_name)
    service_exists = False
    
    for match in match_list:
        if match.title == feature.attributes["name"]:
            message = "Service {} already exists. Updating it...".format(service_name)
            service_exists = True
        else:
            service_exists = False
    print("\n" + message)
    
    if service_exists:
        gdb_name = feature_name + "_" + datetime.utcfromtimestamp(feature.attributes["lastmoddate"] / 1000).strftime("%m_%d_%Y_%H_%M_%S")
        md_name = feature_name
        service_json = create_service_json(service_name, True, gdb_name + ".gdb", service_name)
        if "success" in str(stop_service(image_url, service_name, image_token)):
            print("Service stopped.")
        edit_image_service(service_name, service_json)
        print("Service updated")
        if "success" in str(start_service(image_url, service_name, image_token)):
            print("Service started.")
    else:
        service_json = create_service_json(service_name, False, gdb_name + ".gdb", service_name)
        publish_image_service(service_name, service_json)
        print("New service published")