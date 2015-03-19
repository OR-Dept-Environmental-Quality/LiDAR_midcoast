# ---------------------------------------------------------------------------
# workflow_rev.py
# Created on: 2015-03-06; M.S. Faizullabhoy
# Description: Procedure to create a conditioned Digital Elevation Model and Stream Network
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy, os
# Check out any necessary licenses
arcpy.CheckOutExtension("3D")
arcpy.CheckOutExtension("spatial")
CWDir = os.getcwd()
arcpy.env.workspace = CWDir
#-------
(filepath,filename)=os.path.split(CWDir)
WshName = filename
#-------
# Local variables: This script should reside in the same directory as these three required shapefiles 
cell_size = "9"  #This is the dem cell size (ft)
Rast9ftPts_shp = CWDir + "\\" + "nfsiuslawel9pt.shp" 
DamBreak_shp = CWDir + "\\" + "DamBreak.shp"
Boundary_shp = CWDir + "\\" + "Boundary.shp"
# Process:
#---
print	"Processing TopoToRaster..." 
DEM = "dem" + cell_size
DEM = CWDir + "\\DEM"						#outfile
if os.path.exists(DEM):
	arcpy.Delete_management(DEM)
arcpy.TopoToRaster_3d(Rast9ftPts_shp + " GRID_CODE PointElevation;" + DamBreak_shp + " # Stream;" + Boundary_shp + " # Boundary", DEM, cell_size, Boundary_shp, "20", "", "", "ENFORCE", "SPOT", "40", "0.5", "1", "0", "0", "200", "", "", "", "", "", "", "", "")
print 	"Finished Processing TopoToRaster located at " + DEM
#---
print	"Processing Fill Sink..." 
fill_DEM = CWDir + "\\fill_DEM" 				#outfile
if os.path.exists(fill_DEM):
	arcpy.Delete_management(fill_DEM)
arcpy.gp.Fill_sa(DEM, fill_DEM, "")
print 	"Finished Processing Fill located at " + fill_DEM
#---
print	"Processing Flow Direction Raster..." 
fdir_DEM = CWDir + "\\fdir_DEM" 				#outfile
if os.path.exists(fdir_DEM):
	arcpy.Delete_management(fdir_DEM)
arcpy.gp.FlowDirection_sa(fill_DEM, fdir_DEM, "FORCE", "")
print 	"Finished Processing Flow Direction Raster - located at " + fdir_DEM
#---
print	"Processing Accumulation..." 
facc_DEM = CWDir + "\\facc_DEM" 				#outfile
if os.path.exists(facc_DEM):
	arcpy.Delete_management(facc_DEM)
arcpy.gp.FlowAccumulation_sa(fdir_DEM, facc_DEM, "", "INTEGER")
print 	"Finished Processing Flow Accumulation Raster - located at" + facc_DEM
#---
print	"Reclassifying..."
recls_facc = CWDir + "\\recls_facc" 				#outfile
if os.path.exists(recls_facc):
	arcpy.Delete_management(recls_facc)
elevMAX = arcpy.GetRasterProperties_management(facc_DEM, "MAXIMUM")
SetThreshold = 8000   #refine if necessary to alter resolution of stream network
SetThresholdp1 =  SetThreshold + 1 
arcpy.Reclassify_3d(facc_DEM, "Value", "0 " + str(SetThreshold) + " NODATA;" + str(SetThresholdp1) + " " + str(elevMAX) + " 1", recls_facc, "DATA")
print 	"Finished Reclassifying - located at " + recls_facc
#---
strmNetwork_shp = WshName + str(SetThreshold) + ".shp" 
strmNetworkName = CWDir + "\\" +  strmNetwork_shp #outfile
if os.path.exists(strmNetworkName):
	arcpy.Delete_management(strmNetworkName)
arcpy.gp.StreamToFeature_sa(recls_facc, fdir_DEM, strmNetworkName, "SIMPLIFY")
print 	"Finished! Stream Network Location - " + strmNetworkName	

