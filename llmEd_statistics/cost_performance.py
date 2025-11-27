import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Percorso della cartella
from matplotlib.patches import Patch

folder_path = r"/"

# =============================================================================
# ANALISI COSTI INPUT TOKENS
# =============================================================================

# Legge il file input tokens
input_file_path = os.path.join(folder_path, "statistics/input_tokens_aggregated.csv")
input_df = pd.read_csv(input_file_path)

# Rinomina le colonne
input_df_renamed = input_df.rename(columns={
    "Lesson Total Generation": "Lesson Planning",
    "Total Activity Generation": "Total Planning"
})

# Calcola i costi per ogni attività (formula: tokens / 1,000,000 * 2.50)
input_costs = pd.DataFrame({
    "ALP": (input_df_renamed["Annual Lesson Plan"] / 1000000) * 2.50,
    "UD": (input_df_renamed["Uda Planning"] / 1000000) * 2.50,
    "DM": (input_df_renamed["Didactic Material"] / 1000000) * 2.50,
    "LP": (input_df_renamed["Lesson Planning"] / 1000000) * 2.50,
    "TP": (input_df_renamed["Total Planning"] / 1000000) * 2.50
})

print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print(input_costs)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
# Calcola metriche aggregate per costi input
input_cost_metrics = pd.DataFrame({
    "Mean": input_costs.mean(),
    "Median": input_costs.median(),
    "Std. Dev.": input_costs.std(),
    "IQR": input_costs.quantile(0.75) - input_costs.quantile(0.25)
})

# Mostra metriche a video
print("📊 INPUT TOKENS COST - Metriche aggregate per attività:\n")
print(input_cost_metrics)

# Salva in CSV
input_cost_metrics_path = os.path.join(folder_path, "statistics/input_tokens_cost_performance.csv")
input_cost_metrics.to_csv(input_cost_metrics_path)
print(f"\n✅ File metriche COSTI INPUT tokens salvato in: {input_cost_metrics_path}")

'''# --- Visualizzazione grafica TUTTE le metriche Costi Input Tokens ---
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('INPUT Tokens Cost - Tutte le Metriche', fontsize=16, fontweight='bold')

# Media
input_cost_metrics["Media"].plot(kind="bar", ax=axes[0, 0], color='blue', alpha=0.7, edgecolor='black')
axes[0, 0].set_title("Media")
axes[0, 0].set_ylabel("Cost ($)")
axes[0, 0].tick_params(axis='x', rotation=0)
axes[0, 0].grid(axis="y", linestyle="--", alpha=0.7)

# Mediana
input_cost_metrics["Mediana"].plot(kind="bar", ax=axes[0, 1], color='green', alpha=0.7, edgecolor='black')
axes[0, 1].set_title("Mediana")
axes[0, 1].set_ylabel("Cost ($)")
axes[0, 1].tick_params(axis='x', rotation=0)
axes[0, 1].grid(axis="y", linestyle="--", alpha=0.7)

# Deviazione Standard
input_cost_metrics["STD"].plot(kind="bar", ax=axes[1, 0], color='red', alpha=0.7, edgecolor='black')
axes[1, 0].set_title("Deviazione Standard")
axes[1, 0].set_ylabel("Cost ($)")
axes[1, 0].tick_params(axis='x', rotation=0)
axes[1, 0].grid(axis="y", linestyle="--", alpha=0.7)

# IQR
input_cost_metrics["IQR"].plot(kind="bar", ax=axes[1, 1], color='purple', alpha=0.7, edgecolor='black')
axes[1, 1].set_title("IQR")
axes[1, 1].set_ylabel("Cost ($)")
axes[1, 1].tick_params(axis='x', rotation=0)
axes[1, 1].grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()

# --- Grafico combinato con tutte le metriche ---
plt.figure(figsize=(12, 8))
input_cost_metrics.plot(kind="bar", figsize=(12, 8))
plt.title("INPUT Tokens Cost - Tutte le Metriche")
plt.ylabel("Cost ($)")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()'''

# =============================================================================
# ANALISI COSTI OUTPUT TOKENS
# =============================================================================

# Legge il file output tokens
output_file_path = os.path.join(folder_path, "statistics/output_tokens_aggregated.csv")
output_df = pd.read_csv(output_file_path)

# Rinomina le colonne
output_df_renamed = output_df.rename(columns={
    "Lesson Total Generation": "Lesson Planning",
    "Total Activity Generation": "Total Planning"
})

# Calcola i costi per ogni attività (formula: tokens / 1,000,000 * 10.00)
output_costs = pd.DataFrame({
    "ALP": (output_df_renamed["Annual Lesson Plan"] / 1000000) * 10.00,
    "UD": (output_df_renamed["Uda Planning"] / 1000000) * 10.00,
    "DM": (output_df_renamed["Didactic Material"] / 1000000) * 10.00,
    "LP": (output_df_renamed["Lesson Planning"] / 1000000) * 10.00,
    "TP": (output_df_renamed["Total Planning"] / 1000000) * 10.00
})
print("!!!!!!!!!!!!!!!!!!! OUTPUT COST !!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print(output_costs)
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

# Calcola metriche aggregate per costi output
output_cost_metrics = pd.DataFrame({
    "Mean": output_costs.mean(),
    "Median": output_costs.median(),
    "Std. Dev.": output_costs.std(),
    "IQR": output_costs.quantile(0.75) - output_costs.quantile(0.25)
})

# Mostra metriche a video
print("\n📊 OUTPUT TOKENS COST - Metriche aggregate per attività:\n")
print(output_cost_metrics)

# Salva in CSV
output_cost_metrics_path = os.path.join(folder_path, "results/output_tokens_cost_performance.csv")
output_cost_metrics.to_csv(output_cost_metrics_path)
print(f"\n✅ File metriche COSTI OUTPUT tokens salvato in: {output_cost_metrics_path}")

'''# --- Visualizzazione grafica TUTTE le metriche Costi Output Tokens ---
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
fig.suptitle('OUTPUT Tokens Cost - Tutte le Metriche', fontsize=16, fontweight='bold')

# Media
output_cost_metrics["Media"].plot(kind="bar", ax=axes[0, 0], color='blue', alpha=0.7, edgecolor='black')
axes[0, 0].set_title("Media")
axes[0, 0].set_ylabel("Cost ($)")
axes[0, 0].tick_params(axis='x', rotation=0)
axes[0, 0].grid(axis="y", linestyle="--", alpha=0.7)

# Mediana
output_cost_metrics["Mediana"].plot(kind="bar", ax=axes[0, 1], color='green', alpha=0.7, edgecolor='black')
axes[0, 1].set_title("Mediana")
axes[0, 1].set_ylabel("Cost ($)")
axes[0, 1].tick_params(axis='x', rotation=0)
axes[0, 1].grid(axis="y", linestyle="--", alpha=0.7)

# Deviazione Standard
output_cost_metrics["STD"].plot(kind="bar", ax=axes[1, 0], color='red', alpha=0.7, edgecolor='black')
axes[1, 0].set_title("Deviazione Standard")
axes[1, 0].set_ylabel("Cost ($)")
axes[1, 0].tick_params(axis='x', rotation=0)
axes[1, 0].grid(axis="y", linestyle="--", alpha=0.7)

# IQR
output_cost_metrics["IQR"].plot(kind="bar", ax=axes[1, 1], color='purple', alpha=0.7, edgecolor='black')
axes[1, 1].set_title("IQR")
axes[1, 1].set_ylabel("Cost ($)")
axes[1, 1].tick_params(axis='x', rotation=0)
axes[1, 1].grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()

# --- Grafico combinato con tutte le metriche ---
plt.figure(figsize=(12, 8))
output_cost_metrics.plot(kind="bar", figsize=(12, 8))
plt.title("OUTPUT Tokens Cost - Tutte le Metriche")
plt.ylabel("Cost ($)")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()'''

# =============================================================================
# VISUALIZZAZIONE COMPARATIVA TUTTE LE METRICHE
# =============================================================================

# Confronto di tutte le metriche Input vs Output
metrics_to_compare = ["Mean", "Median", "Std. Dev.", "IQR"]

fig, axes = plt.subplots(2, 2, figsize=(16, 12))

for i, metric in enumerate(metrics_to_compare):
    row = i // 2
    col = i % 2

    # Prepara i dati per il confronto
    comparison_data = pd.DataFrame({
        'INPUT': input_cost_metrics[metric],
        'OUTPUT': output_cost_metrics[metric]
    })

    comparison_data.plot(kind="bar", ax=axes[row, col], color=['blue', 'red'], alpha=0.7)
    axes[row, col].set_title(f"{metric}", fontsize=24)
    axes[row, col].set_ylabel("Cost ($)", fontsize=24)
    axes[row, col].tick_params(axis='y', labelsize=18)
    axes[row, col].tick_params(axis='x', rotation=0, labelsize=18)
    axes[row, col].grid(axis="y", linestyle="--", alpha=0.7)
    axes[row, col].legend()

plt.tight_layout()
plt.show()


#
# =============================================================================
# STATISTICHE RIASSUNTIVE COSTI
# =============================================================================

print("\n" + "=" * 60)
print("💰 STATISTICHE RIASSUNTIVE COSTI TOKENS")
print("=" * 60)

print(f"\n🔢 NUMERO DI PARTECIPANTI: {len(input_df_renamed)}")
print(f"👤 ID PARTECIPANTI: da {input_df_renamed['Partecipante'].min()} a {input_df_renamed['Partecipante'].max()}")

print(f"\n🔄 COLONNE RINOMINATE:")
print("   • Lesson Total Generation → Lesson Planning")
print("   • Total Activity Generation → Total Planning")

print(f"\n💵 COSTI TOTALI INPUT TOKENS:")
for activity in input_cost_metrics.index:
    total_cost = input_costs[activity].sum()
    mean_cost = input_cost_metrics.loc[activity, "Mean"]
    print(f"  • {activity}: ${total_cost:.4f} (media: ${mean_cost:.4f})")

print(f"\n💵 COSTI TOTALI OUTPUT TOKENS:")
for activity in output_cost_metrics.index:
    total_cost = output_costs[activity].sum()
    mean_cost = output_cost_metrics.loc[activity, "Mean"]
    print(f"  • {activity}: ${total_cost:.4f} (media: ${mean_cost:.4f})")


# Calcola il costo totale per ogni attività (Input + Output)
total_costs = pd.DataFrame({
        "ALP": input_costs["ALP"] + output_costs["ALP"],
        "UD": input_costs["UD"] + output_costs["UD"],
        "DM": input_costs["DM"] + output_costs["DM"],
        "LP": input_costs["LP"] + output_costs["LP"],
        "TP": input_costs["TP"] + output_costs["TP"]
    })

# Mostra metriche a video
print("\n📊 TOTAL TOKENS COST - Metriche aggregate per attività:\n")
print(total_costs)
    # Salva il file
total_costs.to_csv("results/total_costs_per_activity.csv", index=False)

print("✅ File 'total_costs_per_activity.csv' creato con successo!")
# Calcola metriche aggregate per costi output
total_cost_metrics = pd.DataFrame({
    "Mean": total_costs.mean(),
    "Median": total_costs.median(),
    "Std. Dev.": total_costs.std(),
    "IQR": total_costs.quantile(0.75) - output_costs.quantile(0.25)
})



# Salva in CSV
total_cost_metrics_path = os.path.join(folder_path, "results/total_tokens_cost_performance.csv")
total_cost_metrics.to_csv(total_cost_metrics_path)
