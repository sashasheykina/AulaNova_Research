import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Percorso della cartella
folder_path = r"/"

# =============================================================================
# ANALISI INPUT TOKENS PERFORMANCE
# =============================================================================

# Legge il file input tokens
input_file_path = os.path.join(folder_path, "statistics/input_tokens_aggregated.csv")
input_df = pd.read_csv(input_file_path)

# Rinomina le colonne
input_df_renamed = input_df.rename(columns={
    "Lesson Total Generation": "Lesson Planning",
    "Total Activity Generation": "Total Planning"
})

# Calcola metriche aggregate per input tokens
input_metrics = pd.DataFrame({
    "Mean": input_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].mean(),
    "Median": input_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].median(),
    "Std. Dev.": input_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].std(),
    "IQR": input_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].quantile(0.75) -
           input_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].quantile(0.25)
})

# Mostra metriche a video
print("📊 INPUT TOKENS - Metriche aggregate per attività:\n")
print(input_metrics)

# Salva in CSV
input_metrics_path = os.path.join(folder_path, "results/input_tokens_performance.csv")
input_metrics.to_csv(input_metrics_path)
print(f"\n✅ File metriche INPUT tokens salvato in: {input_metrics_path}")

# --- Visualizzazione grafica Input Tokens ---
input_metrics.plot(kind="bar", figsize=(10,6))

plt.title("INPUT Tokens Performance")
plt.ylabel("Tokens")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()

# =============================================================================
# ANALISI OUTPUT TOKENS PERFORMANCE
# =============================================================================

# Legge il file output tokens
output_file_path = os.path.join(folder_path, "statistics/output_tokens_aggregated.csv")
output_df = pd.read_csv(output_file_path)

# Rinomina le colonne
output_df_renamed = output_df.rename(columns={
    "Lesson Total Generation": "Lesson Planning",
    "Total Activity Generation": "Total Planning"
})

# Calcola metriche aggregate per output tokens
output_metrics = pd.DataFrame({
    "Mean": output_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].mean(),
    "Median": output_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].median(),
    "Std. Dev.": output_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].std(),
    "IQR": output_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].quantile(0.75) -
           output_df_renamed[["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Planning", "Total Planning"]].quantile(0.25)
})

# Mostra metriche a video
print("\n📊 OUTPUT TOKENS - Metriche aggregate per attività:\n")
print(output_metrics)

# Salva in CSV
output_metrics_path = os.path.join(folder_path, "results/output_tokens_performance.csv")
output_metrics.to_csv(output_metrics_path)
print(f"\n✅ File metriche OUTPUT tokens salvato in: {output_metrics_path}")

# --- Visualizzazione grafica Output Tokens ---
output_metrics.plot(kind="bar", figsize=(10,6))

plt.title("OUTPUT Tokens Performance")
plt.ylabel("Tokens")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.show()
'''
# =============================================================================
# VISUALIZZAZIONE COMPARATIVA
# =============================================================================

# Confronto Media Input vs Output
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
input_metrics["Media"].plot(kind="bar", color='blue', alpha=0.7, edgecolor='black')
plt.title("INPUT Tokens - Media")
plt.ylabel("Tokens")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.subplot(1, 2, 2)
output_metrics["Media"].plot(kind="bar", color='red', alpha=0.7, edgecolor='black')
plt.title("OUTPUT Tokens - Media")
plt.ylabel("Tokens")
plt.xticks(rotation=0)
plt.grid(axis="y", linestyle="--", alpha=0.7)

plt.tight_layout()
plt.show()
'''
# =============================================================================
# STATISTICHE RIASSUNTIVE
# =============================================================================

print("\n" + "="*60)
print("📈 STATISTICHE RIASSUNTIVE TOKENS")
print("="*60)

print(f"\n🔢 NUMERO DI PARTECIPANTI: {len(input_df_renamed)}")
print(f"👤 ID PARTECIPANTI: da {input_df_renamed['Partecipante'].min()} a {input_df_renamed['Partecipante'].max()}")

print(f"\n🔄 COLONNE RINOMINATE:")
print("   • Lesson Total Generation → Lesson Planning")
print("   • Total Activity Generation → Total Planning")

print(f"\n💰 TOTALI INPUT TOKENS:")
for activity in input_metrics.index:
    total = input_df_renamed[activity].sum()
    print(f"  • {activity}: {total:,} tokens")

print(f"\n💰 TOTALI OUTPUT TOKENS:")
for activity in output_metrics.index:
    total = output_df_renamed[activity].sum()
    print(f"  • {activity}: {total:,} tokens")

print(f"\n📊 RAPPORTO OUTPUT/INPUT:")
total_input = input_df_renamed["Total Planning"].sum()
total_output = output_df_renamed["Total Planning"].sum()
ratio = total_output / total_input if total_input > 0 else 0
print(f"  • Totale Input: {total_input:,} tokens")
print(f"  • Totale Output: {total_output:,} tokens")
print(f"  • Rapporto Output/Input: {ratio:.2%}")