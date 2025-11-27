import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Carica il file
df = pd.read_csv("total_costs.csv")

print("🎓 ANALISI DETTAGLIATA COSTO CORSO ANNUALE")
print("=" * 55)
print("Formula: Costo_Corso_Annuale = (DM + LP) × NL + ALP")
print()

# Calcola le componenti
df['Costo_Materiale_NL'] = df['DM'] * df['NL']
df['Costo_Pianificazione_NL'] = df['LP'] * df['NL']
df['Costo_Lezioni_NL'] = (df['DM'] + df['LP']) * df['NL']
df['Costo_Corso_Annuale'] = df['Costo_Lezioni_NL'] + df['ALP']

# Statistiche
costo_annuale = df['Costo_Corso_Annuale']

print("📊 RISULTATI DETTAGLIATI PER PARTECIPANTE")
print("=" * 45)
for i, row in df.iterrows():
    print(f"\nPartecipante {i+1} (NL={row['NL']}):")
    print(f"  DM: ${row['DM']:.4f} × {row['NL']} = ${row['Costo_Materiale_NL']:.2f}")
    print(f"  LP: ${row['LP']:.4f} × {row['NL']} = ${row['Costo_Pianificazione_NL']:.2f}")
    print(f"  Costo lezioni: ${row['Costo_Lezioni_NL']:.2f}")
    print(f"  ALP: ${row['ALP']:.4f}")
    print(f"  TOTALE CORSO: ${row['Costo_Corso_Annuale']:.2f}")

# Statistiche riassuntive
stats = {
    'Mean': costo_annuale.mean(),
    'Median': costo_annuale.median(),
    'Std. Dev.': costo_annuale.std(),
    'IQR': costo_annuale.quantile(0.75) - costo_annuale.quantile(0.25),
    'Min': costo_annuale.min(),
    'Max': costo_annuale.max()
}

print(f"\n📈 STATISTICHE RIASSUNTIVE:")
print(f"Mean: ${stats['Mean']:.2f} ± ${stats['Std. Dev.']:.2f}")
print(f"Median: ${stats['Median']:.2f}")
print(f"Min: ${stats['Min']:.2f}")
print(f"Max: ${stats['Max']:.2f}")
print(f"Range: [${stats['Min']:.2f}, ${stats['Max']:.2f}]")

# Salva
df.to_csv("detailed_annual_course_cost_analysis.csv", index=False)

# Plot semplice
plt.figure(figsize=(10, 6))

# Punti allineati
metrics = list(stats.keys())
values = list(stats.values())
colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown']

plt.scatter(metrics, values, c=colors, s=200, alpha=0.7, edgecolors='black')

# Aggiungi valori
for i, (metric, value) in enumerate(zip(metrics, values)):
    plt.text(i, value + (max(values) * 0.02), f'${value:.2f}',
             ha='center', va='bottom', fontweight='bold', fontsize=10)

plt.title('', fontsize=14, fontweight='bold')
plt.ylabel('Cost ($)', fontsize=20)
plt.xticks(rotation=0, fontsize=20)
plt.grid(axis='y', alpha=0.9)
plt.tight_layout()
plt.show()

# Stampa valori
print("📊 STATISTICS:")
for metric, value in stats.items():
    print(f"{metric}: ${value:.2f}")