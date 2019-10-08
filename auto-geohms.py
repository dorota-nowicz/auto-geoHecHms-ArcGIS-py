########################################################################################
## Copyright 2019 Dorota Nowicz
## Licensed under the terms of the MIT license
##
## This script automate task conected with preparetion of hydrology model using HecGeoHMS
## See more info about HecGeoHMS: https://www.hec.usace.army.mil/software/hec-geohms/
########################################################################################

### autoGeoHms.py

import arcpy 
arcpy.ImportToolbox(r"C:\path\to\GeoHMS Tools.tbx")  

# set specific input arguments for a model based on data prepared by ArcHydroTool
modelpath = r"path\to\geodatabase\of\model"
obra = 3
puente = 30230
nr = 5
obra = __builtins__.str(obra)
puente =__builtins__.str(puente)
nr =__builtins__.str(nr)
Subbasin, River = "Subbasin"+puente, "River"+puente
Slope = r"C:\path\to\slope\layer\wshslope"
Cat,Strlnk,Str,Fac,Fdr,Fil,ProjectPoint,DEM = "Cat","StrLnk","Str","Fac","Fdr","Fil","ProjectPoint"+puente,"RawDEM"

LongestFlowpath = "LongestFlowpath" + puente
BasinCentroid = "BasinCentroid" + puente
CentroidalLongestFlowpath = "CentroidalLongestFlowpath" + puente
ProjectPoint = "ProjectPoint"+puente

LongestFlowpath = modelpath+"\\LongestFlowpath"+puente
BasinCentroidpath = modelpath +"\\BasinCentroid"+puente
CentroidalLongestFlowpath = modelpath+"\\CentroidalLongestFlowpath"+puente

#  HecGeoHMS toolbox  tasks

# Calculate characteristics of layers
arcpy.RiverLength_geohms(River) 
arcpy.RiverSlope_geohms(DEM,River)  
arcpy.BasinSlope_geohms(Slope,Subbasin)
arcpy.LongestFlowpath_geohms(DEM,Fdr,Subbasin,LongestFlowpath)
arcpy.BasinCentroid_geohms("Longest flow path",Subbasin,BasinCentroid,Fac,River,LongestFlowpath)
arcpy.CentroidElevation_geohms(DEM,BasinCentroid)

# !WARNING! there may appear an error in CentroidalLongestFlowpath_geohms tool. More info:  https://geonet.esri.com/thread/171694
arcpy.CentroidalLongestFlowpath_geohms(Subbasin,"BasinCentroid"+puente,"LongestFlowpath"+puente,CentroidalLongestFlowpath)


# add CN (curve number) and Ia (initial abstraction) layers
CNgrid = r"path\to\cn\layer"
IAgrid = r"C:\PUNO\recursos\MAPAS CN\ia"
arcpy.MakeRasterLayer_management(CNgrid, "nciii")
arcpy.MakeRasterLayer_management(IAgrid, "ia")

# Set calculation methods
arcpy.SelectHMSProcesses_geohms(Subbasin,River, "SCS","SCS","None","Muskingum")

# Name Rivers and Basins
arcpy.RiverAutoName_geohms(River)
arcpy.BasinAutoName_geohms(Subbasin)


# export basin layer to KML format in order to use it in GoogleEarth
arcpy.LayerToKML_conversion(Subbasin, "subbain.kmz")




