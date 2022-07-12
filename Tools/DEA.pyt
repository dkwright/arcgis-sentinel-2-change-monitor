# ------------------------------------------------------------------------------
# Copyright 2016 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Version : 20170323
# ------------------------------------------------------------------------------


import arcpy
import arcpy
import sys, os
import subprocess
import time
import requests
import json
from datetime import datetime
from datetime import timedelta


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "DEA"
        self.alias = ""

        # List of tool classes associated with this toolbox
        #self.tools = [PL_QueryPlanet,PL_Download,PL_ActivateScenes,PL_ActivationStatus,PL_BuildMosaic]
        self.tools = [dea_mosaic]

class dea_mosaic(object):

    def __init__(self):
        self.label = "Build Mosaic Dataset"
        self.description = ""
        self.canRunInBackground = True
        self.tool = 'BuildMosaic'
        pass

    def getParameterInfo(self):
        inSourceGDB = arcpy.Parameter(
        displayName="Output Geodatabase:",
        name="inSourceGDB",
        datatype="DEWorkspace",
        parameterType="Required",
        direction="Input")

        outMDName = arcpy.Parameter(
        displayName="Mosaic Dataset Name",
        name="outMDName",
        datatype="GPString",
        parameterType="Required",
        direction="Input")

        inextent = arcpy.Parameter(
        displayName="Specify AOI",
        name="aoi",
        datatype="GPExtent",
        parameterType="Required",
        direction="Input")

        insrs = arcpy.Parameter(
        displayName = "Coordinate System",
        name = "srs",
        datatype = "GPSpatialReference",
        parameterType = "Required",
        direction = "Input")
        insrs.value ="PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0],AUTHORITY['EPSG',3857]]"


        incloudcover = arcpy.Parameter(
        displayName="Cloud Cover (0-100)",
        name="cloudCover",
        datatype="GPDouble",
        parameterType="Required",
        direction="Input")

        insdate = arcpy.Parameter(
        displayName="Start Date",
        name="startDate",
        datatype="GPDate",
        parameterType="Required",
        direction="Input")

        inedate = arcpy.Parameter(
        displayName="End Date",
        name="endDate",
        datatype="GPDate",
        parameterType="Required",
        direction="Input")

        parameters = [inSourceGDB,outMDName,inextent,insrs,insdate,inedate,incloudcover]
        return parameters

    def updateParameters(self, parameters):
        pass


    def updateMessages(self, parameters):
        pass

    def isLicensed(parameters):
        """Set whether tool is licensed to execute."""
        return True

    def execute(self, parameters, messages):

        solutionLib_path = os.path.dirname(os.path.realpath(__file__))
        solutionLib_path = os.path.join(os.path.dirname(solutionLib_path), "scripts")
        sys.path.append(solutionLib_path)
        parameterBase = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Parameter")
        configBase = os.path.join(parameterBase,"Config")

        import MDCS

        outGDB = parameters[0].valueAsText
        outMDName = parameters[1].valueAsText
        pextent = (parameters[2].valueAsText).replace(" ",",")
        psdate = parameters[4].value
        pstartdate = psdate.strftime('%Y') +'-'+psdate.strftime('%m')+'-'+psdate.strftime('%d')
        pedate = parameters[5].value
        penddate = pedate.strftime('%Y') +'-'+pedate.strftime('%m')+'-'+pedate.strftime('%d')
        pcloudcover = parameters[6].valueAsText
        args = []
        args = ['#gprun']



        configName = os.path.join(configBase,'DigitalAfrica.xml')
        outMD = os.path.join(outGDB,outMDName)
        psrs = parameters[3].valueAsText
        osrs = arcpy.SpatialReference()
        osrs.loadFromString(psrs)
        csrs= osrs.factoryCode


        args.append('-m:'+outMD)
        args.append('-i:'+configName)
        #args.append('-s:'+inPath)
        args.append("-p:"+str(pstartdate) +"$startDate")
        args.append("-p:"+str(penddate) +"$endDate")
        args.append("-p:"+str(pcloudcover) +"$cloud")
        args.append("-p:"+str(pextent) +"$coordinate")
        args.append("-p:"+str(csrs) +"$srs")
        args.append("-c:CM+sentinelModifySrc+AR+SP+CV")

#--------------

        argc = len(args)
        arcpy.AddMessage(args)
        ret = MDCS.main(argc,args)
        arcpy.AddMessage("Done.")
