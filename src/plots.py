import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from itertools import cycle, islice

birds = pd.read_csv(r"data/abellerol/abellerol_plot_indi.csv")

birds_grouped = birds.groupby(by=["month", "year"], dropna=False).sum()

birds_grouped["month_year"] = birds_grouped.index

birds_grouped["month"] = birds_grouped["month_year"].apply(lambda x: x[0])
birds_grouped["year"] = birds_grouped["month_year"].apply(lambda x: x[1])

b = sns.lineplot(data=birds_grouped, x="month", y="N_obs", hue="year", style="year",  ci=None)
b.set_xticks(range(1, 13))
b.set_xticklabels(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"], rotation = 30)

my_colors = list(islice(cycle(['b', 'r', 'g', 'y', 'k', 'p']), None, len("year")))

plt.show()