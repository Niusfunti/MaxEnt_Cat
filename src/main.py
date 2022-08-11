import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas.tools import sjoin
from shapely.geometry import Point, MultiLineString
from shapely.ops import polygonize

data = pd.read_csv(r"data/falsiot/distribucio_utm_03.csv")
points = gpd.GeoDataFrame({"x": data["x_UTM"].values, "y": data["y_UTM"].values})
points['geometry'] = points.apply(lambda p: Point(p.x, p.y), axis=1)


x = np.arange(260000, 530000, 10000, dtype=np.int64)
y = np.arange(4480000, 4750000, 10000, dtype=np.int64)

hlines = [((x1, yi), (x2, yi)) for x1, x2 in zip(x[:-1], x[1:]) for yi in y]
vlines = [((xi, y1), (xi, y2)) for y1, y2 in zip(y[:-1], y[1:]) for xi in x]

polys = list(polygonize(MultiLineString(hlines + vlines)))

id = [i for i in range(len(polys))]
grid = gpd.GeoDataFrame({"id": id, "geometry": polys})

pointInPolys = sjoin(points, grid, how='left')

print(pointInPolys)
