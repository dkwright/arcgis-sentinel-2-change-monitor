# arcgis-sentinel-2-change-monitor
This project was presented at the Esri 2022 Imagery Summit (slides included as Esri_ImagerySummit2022_ChangeMonitoring_Demo.pdf). The project uses an ArcGIS feature service as the control for an automated change monitoring solution using Sentinel-2 L2A data from AWS Open Datasets (via STAC). Operators manage polygons and attributes in the feature service to define where and when Sentinel-2 imagery is needed for analysis. 

## Creating the Feature Service:
### the "ChangeMonitoringControls_FC" subdirectory includes a ZIP compressed File GeoDataBase Sentinel_2_L2A_Monitoring.gdb. Inside the GeoDataBase is a polygon feature class
    * Publish this feature class as an editable feature service
    * Share with collaborators using a Webmap, a Webapp, or ArcGIS Pro
    * Record the item guid after publishing for reference in python code listed below

This project uses Mosaic Dataset Configuration Script (MDCS) which in turn makes use of Arcpy to automate creation and updating of Mosaic Datasets. Next the project automates publishing of image services (or updating them when already existing). The project also uses ArcGIS API for Python to conduct change analysis - differencing NDVI from the two most recent acquisitions in the Mosaic Dataset. A significant part of the MDCS content is based on prior work by Esri that was done in support of Digital Earth Africa. Details on the requirements, setup, and operation of MDCS is covered in the documentation of that repository at https://github.com/Esri/mdcs-py

For a quicket start, clone this repository into this local path: "C:\Image_Mgmt_Workflows\MDCS\arcgis-sentinel-2-change-monitor"

## The "scripts" subdirectory 
### Contains three notebooks:
    * 01-manage-mosaic-datasets.ipynb
    * 02-manage-image-services.ipynb
    * 03-analyze-change.ipynb    
### This directory also contains script form of the management notebooks:
    * 01-manage-mosaic-datasets.py
    * 02-manage-image-services.py
    These scripts are intended for running without the need for user inateraction, or can be called within a scheduled task using:
    * change-monitor-windows-task.bat
    These scripts will require some variables to be set to match your ArcGIS Enterprise / Iamge Server configuration.
   
### A note about SCP
02-manage-image-services.ipynb, and 02-manage-image-services.py includes a method that transfers the File GeoDataBase (FGDB) to a Linux File Server configured with the Image Hosting Site. Note that a Folder Datastore was configured using the Image Server Manager application allowing data access to the File Server. Also note that there is a server folder created on the Image Hosting site "change_monitor" that is in use to partition the Image Services created / updated by this code base. The SCP method here passes the user's id_rsa key to authenticate with the Linux File Server. If you are using a Windows host for your Image Hosting storage, please examine OpenSSH to provide SCP capabilities for Windows, or consider an alternative file transfer method. Yet another alternative is to modify this code to create FGDB on the Image Server directly, or to create the Mosiac Dataset within an Enterprise GeoDataBase, either of which would altogether eliminate the need for the file transfer step.

## The "service_mgmt" directory 
### Contains a JSON template for publishing new image services:
    * rest-create-service-s2l2a-template.json
This template was originally built using ArcGIS Image Server version 10.9.1, and has also been tested with versions 11.0, 11.1 and 11.2.
Please note: You will need to edit some values in this JSON template before running the code."
    * "userName": "changemonitor_myorg" 
Replace "changemon_myorg" with a username in your ArcGIS Enterprise environment with Publisher privileges. This username will be the owner of the published / modified services.
    * "portalURL": "https://cname.domain/portal/" 
Replace https://cname.domain/portal/ with your actual portal URL (e.g https://remotesensing.imagery.esri.com/portal/)
    The onlineResource for WMSServer and WCSServer OGC Extensions will also need to have the base domain edited with just the https://cname.domain/ part of your site URL. Note that MYSERVICENAME (GDBNAME, and MDNAME too!) are already being substituted automatically by the code.
    * "onlineResource": "**https://cname.domain**/image/services/change_monitor/MYSERVICENAME/ImageServer/WCSServer"
    * "onlineResource": "**https://cname.domain**/image/services/change_monitor/MYSERVICENAME/ImageServer/WMSServer"
    
## Additional Requirements:
### Access to the Sentinel-2 Data STAC catalog requires installation of the pystac-client Python module
conda install -c conda-forge pystac-client

