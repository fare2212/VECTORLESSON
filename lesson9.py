from osgeo import ogr
from osgeo import osr
import os
os.chdir('/home/user/git/GeoScripting/data')
print os.getcwd()
import os
os.chdir('/home/user/git/GeoScripting/data')
try:
  from osgeo import ogr, osr
  print 'Import of ogr and osr from osgeo worked.  Hurray!\n'
except:
  print 'Import of ogr and osr from osgeo failed\n\n'

## Is the ESRI Shapefile driver available?
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName

## choose your own name
## make sure this layer does not exist in your 'data' folder
fn = "testing.shp"
layername = "anewlayer"

## Create shape file
ds = drv.CreateDataSource(fn)
print ds.GetRefCount()

# Set spatial reference
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')

# you can also do the following
# spatialReference.ImportFromEPSG(4326)

## Create Layer
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
## Now check your data folder and you will see that the file has been created!
## From now on it is not possible anymore to CreateDataSource with the same name
## in your workdirectory untill your remove the name.shp name.shx and name.dbf file.
print(layer.GetExtent())

## What is the geometry type???
## What does wkb mean??

## ok lets leave the pyramid top and start building the bottom,
## let's do points
## Create a point
point1 = ogr.Geometry(ogr.wkbPoint)
point2 = ogr.Geometry(ogr.wkbPoint)

## SetPoint(self, int point, double x, double y, double z = 0)
point1.SetPoint(0,1.0,1.0) 
point2.SetPoint(0,2.0,2.0)

## Actually we can do lots of things with points: 
## Export to other formats/representations:
print "KML file export"
print point2.ExportToKML()

## Buffering
buffer = point2.Buffer(4,4)
print buffer.Intersects(point1)

## More exports:
buffer.ExportToGML()

## Back to the pyramid, we still have no Feature
## Feature is defined from properties of the layer:e.g:

layerDefinition = layer.GetLayerDefn()
feature1 = ogr.Feature(layerDefinition)
feature2 = ogr.Feature(layerDefinition)

## Lets add the points to the feature
feature1.SetGeometry(point1)
feature2.SetGeometry(point2)

## Lets store the feature in a layer
layer.CreateFeature(feature1)
layer.CreateFeature(feature2)
print "The new extent"
print layer.GetExtent()

## So what is missing ????
## Saving the file, but OGR doesn't have a Save() option
## The shapefile is updated with all object structure 
## when the script finished of when it is destroyed, 
# if necessay SyncToDisk() maybe used

ds.Destroy()
## below the output is shown of the above Python script that is run in the ter
qgis.utils.iface.addVectorLayer('/home/user/git/GeoScripting/data/
testing.shp', 'anewlayer', "ogr")
import mapnik

#First we create a map
map = mapnik.Map(600, 300) #This is the image final image size

#Lets put some sort of background color in the map
map.background = mapnik.Color("steelblue") # steelblue == #4682B4 

#To style the map we need to define a set or rules
#        Map
#  Style      Style
# Rule   Rule   Rule  Rule

# we normally start from the bottom creating an empty rule
rule = mapnik.Rule()

#1) rule that the polygon should be dark red
symbolizer = mapnik.PolygonSymbolizer(mapnik.Color("darkred"))
rule.symbols.append(symbolizer)

#2) The rule is added to the style
style = mapnik.Style()
style.rules.append(rule)

#3) Adding style to map, "mapStyle" is a simple name for our style
#Later we will define that our layer uses this style that is stored on the maps object
map.append_style("mapStyle", style)

#4) Adding the data first step is creating a layer, a map has mutiple layers
layer = mapnik.Layer("mapLayer")
layer.datasource = mapnik.Shapefile(file=os.path.join("/home/user/git/GeoScripting/data","world_borders.shp"))