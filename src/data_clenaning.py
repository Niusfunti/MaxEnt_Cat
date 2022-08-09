import pandas as pd
from trans2UTM import project

#Which species
esp = "falsiot"

for num in range(3, 7):
    # Read data from different files of falsiot.
    df = pd.read_csv(f"../data/{esp}/distribucio_0{num}.csv")

    x_utm_list = []
    y_utm_list = []

    # Transform WGS84 to UTM 31N-ETRS89.
    for l in range(0, len(df)):
        long, lat = df.iloc[l, :]["x"], df.iloc[l, :]["y"]
        z, l, x_utm, y_utm = project((long, lat))
        x_utm_list.append(x_utm)
        y_utm_list.append(y_utm)

    # Delete columns not used in MaxEnd.
    df.drop('ID_GRAFIC', inplace=True, axis=1)
    df.drop('Grup_taxon', inplace=True, axis=1)
    df.drop('Data_obs', inplace=True, axis=1)
    df.drop('MAPX', inplace=True, axis=1)
    df.drop('MAPY', inplace=True, axis=1)
    df.drop('N_indi', inplace=True, axis=1)
    df.drop('N_obs', inplace=True, axis=1)
    df.drop('Nom_cat', inplace=True, axis=1)
    df.drop('x', inplace=True, axis=1)
    df.drop('y', inplace=True, axis=1)

    # Add new coordinates to dataframe
    df["x_UTM"] = x_utm_list
    df["y_UTM"] = y_utm_list

    df["Nom_cien"] = df["Nom_cien"].apply(lambda x: x.replace("Apus apus", f"Apus_apus_0{num}"))

    # Add month in nom cien


    # Save dataframe in csv file.
    df.to_csv(f"data/falsiot/distribucio_utm_0{num}.csv", index=False)


