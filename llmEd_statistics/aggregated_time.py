import pandas as pd
import numpy as np
import glob
import os
import re

# Percorso dei CSV
path = r"/"



# Trova tutti i file
csv_files = glob.glob(os.path.join(path, "time log/execution_times_id*.csv"))
csv_files.sort()  # per mantenerli in ordine

records = []

for file in csv_files:
    df = pd.read_csv(file)
    base_name = os.path.basename(file)

    # Estrai solo l'id numerico dal nome del file
    match = re.search(r"execution_times_id(\d+)", base_name)
    participant_id = int(match.group(1)) if match else base_name

    # Estrai i valori richiesti
    data = {
        "Partecipante": participant_id,
        "Annual Lesson Plan": df.loc[df["Activity"] == "Annual Lesson Plan", "Time (seconds)"].values[0],
        "Uda Planning": df.loc[df["Activity"] == "Uda Planning", "Time (seconds)"].values[0],
        "Didactic Material": df.loc[df["Activity"] == "Didactic Material", "Time (seconds)"].values[0],
    }

    # Calcola Lesson Planning come somma delle 4 attività specifiche
    lesson_planning_sum = df.loc[
        df["Activity"].isin([
            "Lesson Planning Generation",
            "Lesson Execution Generation",
            "Didactic Material"
        ]),
        "Time (seconds)"
    ].sum()

    # Calcola Lesson Planning come somma delle 4 attività specifiche
    total_planning_sum = df.loc[
        df["Activity"].isin([
            "Annual Lesson Plan",
            "List of lessons",
            "Lesson Planning Generation",
            "Lesson Execution Generation",
            "Didactic Material"
        ]),
        "Time (seconds)"
    ].sum()

    data["Lesson Planning"] = lesson_planning_sum
    data["Total Planning"] = total_planning_sum
    records.append(data)

# Crea il DataFrame finale
final_df = pd.DataFrame(records)

# Ordina per Lesson Planning in modo crescente
final_df = final_df.sort_values(by="Partecipante", ascending=True)

# Salva il file finale
output_path = os.path.join(path, "results/aggregated_times.csv")
final_df.to_csv(output_path, index=False)

print("✅ File aggregato salvato in:", output_path)
print(final_df.head())