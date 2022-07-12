# # Automated Change Monitoring with Sentinel-2 L2A

# ## 01 - Manage Mosiac Dataset(s) with Sentinel-2 Imagery for specified area, date range, and cloud cover threshold

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

# ## Execute Mosaic Dataset Configuration Script to create / update Mosaic Dataset for each active AOI
import MDCS
from os import makedirs
from os.path import join, abspath, dirname, exists
from datetime import date, datetime
from arcgis.geometry import Geometry, project

for feature in active_aois:

    today = date.today()
    
    # if EndDate is null we assume it should always be run into the future
    if feature.attributes["enddate"] != None:
        enddate_fmt = date.fromtimestamp(feature.attributes["enddate"] / 1e3)
        enddate = enddate_fmt.strftime("%Y-%m-%d")
    else:
        enddate = today.strftime("%Y-%m-%d")

    startdate_fmt = date.fromtimestamp(feature.attributes['startdate'] / 1e3)
    startdate = startdate_fmt.strftime("%Y-%m-%d")

    print("===========================================")
    print("Processing AOI: " + feature.attributes["name"])    
    print("Start Date: " + startdate)
    print("Todays Date: " + str(today))
    print("End Date: " + enddate)
    print("Cloud cover percent limit: " + str(feature.attributes["cloudcoverpct"]))
    
    geom = Geometry(feature.geometry)
    geom_reprojected = project([geom], in_sr = 3857, out_sr = 4326)[0]
    aoi = str(geom_reprojected.envelope.xmin) + "," + str(geom_reprojected.envelope.ymin) + "," + str(geom_reprojected.envelope.xmax)  + "," + str(geom_reprojected.envelope.ymax)

    print("BBOX: " + aoi)

    args= []

    args = ['#gprun']
    
    gdb_name = feature.attributes["name"]
    
    if not exists(r"C:\data\Sentinel-2-l2a\change_monitor"):
        makedirs(r"C:\data\Sentinel-2-l2a\change_monitor")
    base_path = f"C:\data\Sentinel-2-l2a\change_monitor\{gdb_name}.gdb"
    full_path = '-m:' + join(base_path, gdb_name)
    
    config = "-i:" + r"..\Parameter\Config\DEA.xml"
    cmd = "-c:CM+sentinelModifySrc+AF+AR+markduplicate+RRFMD+SP+CV"
    
    cloudcover = feature.attributes["cloudcoverpct"]
    
    args.append(full_path)
    args.append(config)
    args.append("-p:{0}$startdate".format(startdate))
    args.append("-p:{0}$enddate".format(enddate))
    args.append("-p:{0}$coordinate".format(aoi))
    #args.append("-p:{0}$aoisrs".format(aoisrs))
    args.append("-p:{0}$cloud".format(cloudcover))
    args.append(cmd)

    #messages.addMessage(time.ctime())

    argc = len(args)

    ret = MDCS.main(argc, args)
    
    print("\nMDCS command results:")
    
    update = False
    
    for command_result in ret:
        print(str(command_result["cmd"]) + " : " + str(command_result["value"]))
        if "AR" in command_result["cmd"] and command_result["value"] == True:
            update = True
        
    if update:
        print("New rasters have been added to this Mosaic Dataset.")
        # update the feature's LastModDate attribute with the current datetime stamp
        monitoring_aois_layer.calculate(where=f"name='{gdb_name}'", calc_expression={"field":"lastmoddate", "value": datetime.now()})

        if feature.attributes["notify"] == "True":
            print("Notifications are set to active for: " + feature.attributes["contactemail"])
            # notify by email to feature.attributes["ContactEmail"]
        else:
            print("Notifications are not active for this AOI.")
    
    print("\n")            
    print("AOI finished")

print("\n")
print("Finished all active AOIs")