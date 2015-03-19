# ---------------------------------------------------------------------------
# PreProcessGrid.py
# Created on: 2015-03-06; M.S. Faizullabhoy
# Description: 	Resample the 3 feet grid to desired cell size; 
#				Convert the resulting Raster to Point at 9 feet spacing
# ---------------------------------------------------------------------------
import arcpy, os

CWDir = os.getcwd()
arcpy.env.workspace = CWDir
LiDAR_clip = "nfsiuslawel"    #Provide the correct name of the clipped HUC10 LiDAR raster/ Assumes raster is located in the same dir as the script!
Cell_size = "9"				  #Define cell size.  Testing for mid-coast HUC10 watersheds indicated that a 9ft cell size is a good starting point
print	"Resampling raster from 3 ft to " + Cell_size + " ft..."
if os.path.exists(LiDAR_clip[:3]):
	arcpy.Delete_management(LiDAR_clip[:3]) 
arcpy.Resample_management(LiDAR_clip, LiDAR_clip[:3], Cell_size, "NEAREST")
print	"Finished Resampling..." + LiDAR_clip[:3]

print	"Processing RasterToPoint..."
if os.path.exists(LiDAR_clip + Cell_size +"pt.shp"):
	arcpy.Delete_management(LiDAR_clip + Cell_size +"pt.shp") 
arcpy.RasterToPoint_conversion(LiDAR_clip[:3], LiDAR_clip + Cell_size + "pt.shp", "VALUE")
print	"Finished RasterToPoint..." + LiDAR_clip + Cell_size +"pt.shp"

print	"Deleting Resampled Temporary Raster" + LiDAR_clip[:3]
arcpy.Delete_management(LiDAR_clip[:3])
print 	"Finished!"
