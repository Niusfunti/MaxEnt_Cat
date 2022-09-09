import pandas as pd
import numpy as np
import geopandas as gpd
from geopandas.tools import sjoin
from shapely.geometry import Point, MultiLineString
from shapely.ops import polygonize
from sklearn.model_selection import train_test_split

input = "data/oreneta_v/oreneta_v_maxent.csv"

data = pd.read_csv(input)
points = gpd.GeoDataFrame({"x": data["x_UTM"].values, "y": data["y_UTM"].values})
points['geometry'] = points.apply(lambda p: Point(p.x, p.y), axis=1)


x = np.arange(250000, 540000, 10000, dtype=np.int64)
y = np.arange(4470000, 4760000, 10000, dtype=np.int64)

hlines = [((x1, yi), (x2, yi)) for x1, x2 in zip(x[:-1], x[1:]) for yi in y]
vlines = [((xi, y1), (xi, y2)) for y1, y2 in zip(y[:-1], y[1:]) for xi in x]

polys = list(polygonize(MultiLineString(hlines + vlines)))

id = [i for i in range(len(polys))]
grid = gpd.GeoDataFrame({"id": id, "geometry": polys})

pointInPolys = sjoin(points, grid, how='left')

data["grid"] = pointInPolys["id"]

data_per_month = data.groupby("name_month")

df_final_test = pd.DataFrame()
df_final_train = pd.DataFrame()

for month in data["name_month"].unique():
    df = data_per_month.get_group(month)
    grid_groups = df.groupby("grid")

    df_month_train = pd.DataFrame()
    df_month_test = pd.DataFrame()

    for g in df["grid"].unique():
        grid_m_df = grid_groups.get_group(g)
        if len(grid_m_df) == 1:
            df_train = grid_m_df
            df_month_train = pd.concat([df_month_train, df_train])
        else:
            df_train, df_test = train_test_split(grid_m_df, test_size=0.25, random_state=7)
            df_month_train = pd.concat([df_month_train, df_train])
            df_month_test = pd.concat([df_month_test, df_test])

    df_final_train = pd.concat([df_final_train, df_month_train])
    df_final_test = pd.concat([df_final_test, df_month_test])

output = input.split(".")[0]

df_final_train = df_final_train[["name_month", "x_UTM", "y_UTM"]]
df_final_test = df_final_test[["name_month", "x_UTM", "y_UTM"]]

print(len(df_final_train), len(df_final_test))

df_final_train.to_csv(f"{output}_train.csv", index=False)
df_final_test.to_csv(f"{output}_test.csv", index=False)


