import pandas as pd
from trans2UTM import project

#Which species
esp = "aligot"

# Read data from different files of species.
df = pd.read_csv(f"../data/{esp}/aligot.csv", sep=";")

# Change dtype
df["Data_obs"] = pd.to_datetime(df["Data_obs"])

m_groups = df.groupby(df['Data_obs'].dt.strftime('%B'))

df["month"] = df["Data_obs"].dt.month
df["year"] = df["Data_obs"].dt.year

if esp in ["abellerol", "falsiot"]:
    df = df[df["year"] == 2022]

df["name_month"] = df.apply(lambda row: f"oreneta_v_{row['month']}", axis=1)


df = df[(2 <= df["month"]) & (df["month"] <= 6)]


# m_groups.groups.keys()
df.reset_index()

x_utm_list = []
y_utm_list = []

# Transform WGS84 to UTM 31N-ETRS89.
for l in range(0, len(df)):
    long, lat = df.iloc[l, :]["x"], df.iloc[l, :]["y"]
    z, l, x_utm, y_utm = project((long, lat))
    x_utm_list.append(x_utm)
    y_utm_list.append(y_utm)

# # Delete columns not used in MaxEnd.
df.drop('Grup_taxon', inplace=True, axis=1)
df.drop('Data_obs', inplace=True, axis=1)
df.drop('N_indi', inplace=True, axis=1)
df.drop('N_obs', inplace=True, axis=1)
df.drop('Nom_cat', inplace=True, axis=1)
df.drop('Nom_cien', inplace=True, axis=1)
# df.drop('month', inplace=True, axis=1)
df.drop('x', inplace=True, axis=1)
df.drop('y', inplace=True, axis=1)
#
# # Add new coordinates to dataframe
df["x_UTM"] = x_utm_list
df["y_UTM"] = y_utm_list
#
# # df["Nom_cien"] = df["Nom_cien"].apply(lambda x: x.replace("abellerol", f"abellerol_0{num}"))
#
# # Add month in nom cien
#
#
# # Save dataframe in csv file.

df = df[["name_month", "x_UTM", "y_UTM"]]
df.to_csv(f"data/oreneta_v/oreneta_v_maxent.csv", index=False)



