import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Percorso del file aggregato
folder_path = r"/"
file_path = os.path.join(folder_path, "results/aggregated_times.csv")

# Legge il dataset
df = pd.read_csv(file_path)

## Calcola metriche aggregate per attività
metrics = pd.DataFrame({
    "Media": df[["Annual Lesson Plan", "Uda Planning", "Lesson Planning", "Didactic Material", "Total Planning"]].mean(),
    "Mediana": df[["Annual Lesson Plan", "Uda Planning", "Lesson Planning", "Didactic Material", "Total Planning"]].median(),
    "STD": df[["Annual Lesson Plan", "Uda Planning", "Lesson Planning", "Didactic Material", "Total Planning"]].std(),
    "IQR": df[["Annual Lesson Plan", "Uda Planning", "Lesson Planning", "Didactic Material", "Total Planning"]].quantile(0.75) -
           df[["Annual Lesson Plan", "Uda Planning", "Lesson Planning", "Didactic Material", "Total Planning"]].quantile(0.25)
})

# Mostra metriche a video
print("📊 Metriche aggregate per attività:\n")
print(metrics)

# Salva in CSV
output_metrics_path = os.path.join(folder_path, "results/aggregated_metrics_activities.csv")
metrics.to_csv(output_metrics_path)
print(f"\n✅ File metriche salvato in: {output_metrics_path}")

# --- Visualizzazione grafica ---
metrics.plot(kind="bar", figsize=(8,5))

plt.ylabel("Seconds")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
