import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("data/rule_engine_results.csv")
sns.set(style="whitegrid", font_scale=1.1)

plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="elevation", y="stress_index", hue="status")
plt.axhline(150, linestyle="--", color="red")
plt.title("Stress Index vs Elevation")
plt.show()
