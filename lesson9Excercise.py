import os
os.chdir('/home/user/git/GeoScripting/data')
try:
  from osgeo import ogr, osr
  print 'Import of ogr and osr from osgeo worked.  Hurray!\n'
except:
  print 'Import of ogr and osr from osgeo failed\n\n'
driverName = "ESRI Shapefile"
drv = ogr.GetDriverByName( driverName )
if drv is None:
    print "%s driver not available.\n" % driverName
else:
    print  "%s driver IS available.\n" % driverName
fn = "excercise.shp"
layername = "mylayer"
ds = drv.CreateDataSource(fn)
print ds.GetRefCount()
spatialReference = osr.SpatialReference()
spatialReference.ImportFromProj4('+proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs')
layer=ds.CreateLayer(layername, spatialReference, ogr.wkbPoint)
print(layer.GetExtent())
Gaia = ogr.Geometry(ogr.wkbPoint)
Forum = ogr.Geometry(ogr.wkbPoint)
Gaia.SetPoint(0,51.987423,5.665511) 
Forum.SetPoint(0,51.985288,5.663718)
print Gaia.ExportToKML()
print Forum.ExportToKML()
buffer = Forum.Buffer(4,4)
print buffer.Intersects(Gaia)
buffer.ExportToGML()
layerDefinition = layer.GetLayerDefn()
feature1 = ogr.Feature(layerDefinition)
feature2 = ogr.Feature(layerDefinition)
feature1.SetGeometry(Gaia)
feature2.SetGeometry(Forum)
layer.CreateFeature(feature1)
layer.CreateFeature(feature2)
print layer.GetExtent()
ds.Destroy()
qgis.utils.iface.addVectorLayer('/home/user/git/GeoScripting/data/excercise.shp', 'mylayer', "ogr")
import os,os.path
import mapnik
file_symbol=os.path.join("/home/user/git/GeoScripting/figs","http://www.google.com/mapfiles/marker.png")
map = mapnik.Map(800, 400)
map.background = mapnik.Color("skyblue")
r = mapnik.Rule()
s = mapnik.Style()
polyStyle= mapnik.PolygonSymbolizer(mapnik.Color("darkred"))
pointStyle = mapnik.PointSymbolizer(mapnik.PathExpression(file_symbol))
r.symbols.append(polyStyle)
r.symbols.append(pointStyle)
s.rules.append(r)
map.append_style("mapStyle", s)
layerPoint = mapnik.Layer("pointLayer")
layerPoint.datasource = mapnik.Shapefile(file=os.path.join("/home/user/git/GeoScripting/data","excercise.shp"))
layerPoint.styles.append("mapStyle")
layerPoly = mapnik.Layer("polyLayer")
layerPoly.datasource = mapnik.Shapefile(file=os.path.join("/home/user/git/GeoScripting/data","ne_110m_land.shp"))
layerPoly.styles.append("mapStyle")
boundsLL = (5.663718,5.665511,51.985288, 51.987423) #(minx, miny, maxx,maxy)
map.zoom_to_box(mapnik.Box2d(*boundsLL)) # zoom to bbox

map.layers.append(layerPoly)
map.layers.append(layerPoint)
mapnik.render_to_file(map, os.path.join("/home/user/git/GeoScripting/figs","map3.png"), "png")