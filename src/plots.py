import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle, islice

fig, ax = plt.subplots(figsize=(10, 8))


abellerol = pd.read_csv(r"data/abellerol/abellerol_plot.csv")
aligot = pd.read_csv(r"data/aligot/aligot_plot.csv")
falsiot = pd.read_csv(r"data/falsiot/falsiot_plot.csv")
mastegatatxes = pd.read_csv(r"data/mastegatatxes/mastegatatxes_plot.csv")
oreneta_c = pd.read_csv(r"data/oreneta_c/oreneta_c_plot.csv")
oreneta_v = pd.read_csv(r"data/oreneta_v/oreneta_v_plot.csv")


colors = {
    "abellerol": "#b870df",
    "aligot": "#e0ee22",
    "falsiot": "#07d273",
    "mastegatatxes": "#ee8413",
    "oreneta_c": "#ec81bf",
    "oreneta_v": "#72e61f"
}

names = {
    "abellerol": "Abellerol",
    "aligot": "Aligot vesper",
    "falsiot": "Falciot negre",
    "mastegatatxes": "Mastegatatxes",
    "oreneta_c": "Oreneta cuablanca",
    "oreneta_v": "Oreneta vulgar"
}

for esp in ["abellerol", "aligot", "falsiot", "oreneta_c"]:
    data = pd.read_csv(f"data/{esp}/{esp}_plot.csv")
    birds_grouped = data.groupby(by=["month", "year"], dropna=False).sum()
    birds_grouped["month_year"] = birds_grouped.index
    birds_grouped["month"] = birds_grouped["month_year"].apply(lambda x: x[0])

    birds_grouped = birds_grouped[ birds_grouped["month"] <= 8]

    # birds_grouped["year"] = birds_grouped["month_year"].apply(lambda x: x[1])

    sns.set_context("paper")
    sns.set(font_scale=1.4, style='ticks', rc=None, font="Times New Roman")

    b = sns.lineplot(ax=ax, data=birds_grouped, x="month", y="N_obs",  ci=None, color=colors[esp], label=names[esp])

ax.legend(title="Espècies", loc='upper left', fontsize= "medium", title_fontsize= "medium")

b.set_xticks(range(1, 9))
b.set_xticklabels(["January", "February", "March", "April", "May", "June", "July", "August"], fontsize= "small")
b.set_yticklabels(b.get_yticks(), fontsize= "small")

b.set_xlabel("Mes", fontsize="medium")
b.set_ylabel("Nombre d'observacions",fontsize="medium")

# my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k', 'p']), None, len("year")))

fig.savefig("all_spc_plot.png", dpi=300)

plt.show()