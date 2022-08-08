import pandas as pd
from trans2UTM import project

for num in range(3, 7):
    df = pd.read_csv(f"../data/falsiot/distribucio_0{num}.csv")

    x_utm_list = []
    y_utm_list = []

    for l in range(0, len(df)):
        long, lat = df.iloc[l, :]["x"], df.iloc[l, :]["y"]
        z, l, x_utm, y_utm = project((long, lat))
        x_utm_list.append(x_utm)
        y_utm_list.append(y_utm)

    df["x_UTM"] = x_utm_list
    df["y_UTM"] = y_utm_list

    df.to_csv(f"data/falsiot/distribucio_utm_0{num}.csv")


