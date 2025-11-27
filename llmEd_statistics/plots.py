import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carica i dati
df = pd.read_csv("summary_times.csv")

# Stampa anteprima dati
print("Anteprima dei dati:")
print(df.head())
plt.figure(figsize=(10, 6))
heatmap_data = df.set_index('Activity')
sns.heatmap(heatmap_data, annot=True, cmap='YlOrRd', fmt='.1f', linewidths=.5, cbar_kws={'label': 'Valore'})
plt.title('Mappa di Calore - Tutte le Metriche', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('heatmap_metriche.png', dpi=300, bbox_inches='tight')
plt.show()

