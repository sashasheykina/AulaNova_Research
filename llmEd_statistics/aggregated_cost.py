import pandas as pd
import os

# Percorso della cartella
path = r"/"

# Carica i file aggregati
input_file_path = os.path.join(path, "statistics/input_tokens_aggregated.csv")
output_file_path = os.path.join(path, "statistics/output_tokens_aggregated.csv")

input_df = pd.read_csv(input_file_path)
output_df = pd.read_csv(output_file_path)

# Lista delle attività da analizzare
activities = ["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Total Generation",
              "Total Activity Generation"]

# Prezzi per il calcolo dei costi
COST_PER_MILLION_INPUT = 2.50  # $ per 1M token input
COST_PER_MILLION_OUTPUT = 10.00  # $ per 1M token output

# Lista per raccogliere i risultati
cost_records = []

# Assicurati che entrambi i dataframe abbiano gli stessi partecipanti
participants = sorted(set(input_df['Partecipante']).union(set(output_df['Partecipante'])))

for participant_id in participants:
    # Trova i dati del partecipante in entrambi i file
    input_data = input_df[input_df['Partecipante'] == participant_id]
    output_data = output_df[output_df['Partecipante'] == participant_id]

    total_input_cost = 0.0
    total_output_cost = 0.0

    # Calcola i costi per ogni attività
    for activity in activities:
        # Costo Input
        if len(input_data) > 0 and activity in input_data.columns:
            input_tokens = input_data[activity].values[0]
            input_cost = (input_tokens / 1000000) * COST_PER_MILLION_INPUT
            total_input_cost += input_cost

        # Costo Output
        if len(output_data) > 0 and activity in output_data.columns:
            output_tokens = output_data[activity].values[0]
            output_cost = (output_tokens / 1000000) * COST_PER_MILLION_OUTPUT
            total_output_cost += output_cost

    # Calcola costo totale
    total_cost = total_input_cost + total_output_cost

    # Aggiungi al record
    cost_records.append({
        'Partecipante': participant_id,
        'Total_Input_Token_Cost': total_input_cost,
        'Total_Output_Token_Cost': total_output_cost,
        'Total_Cost': total_cost
    })

# Crea il DataFrame dei costi
costs_df = pd.DataFrame(cost_records)

# Ordina per partecipante
costs_df = costs_df.sort_values('Partecipante').reset_index(drop=True)

# Salva il file dei costi
output_cost_path = os.path.join(path, "statistics/token_costs_summary.csv")
costs_df.to_csv(output_cost_path, index=False)

print("✅ File dei costi creato con successo!")
print(f"📁 File salvato in: {output_cost_path}")

# Mostra anteprima
print(f"\n📊 ANTEPRIMA DEI COSTI:")
print(costs_df.head(10))

# Statistiche riassuntive
print(f"\n📈 STATISTICHE COSTI TOTALI:")
print(f"• Numero partecipanti: {len(costs_df)}")
print(f"• Costo Input totale: ${costs_df['Total_Input_Token_Cost'].sum():.2f}")
print(f"• Costo Output totale: ${costs_df['Total_Output_Token_Cost'].sum():.2f}")
print(f"• Costo complessivo totale: ${costs_df['Total_Cost'].sum():.2f}")
print(f"• Costo medio per partecipante: ${costs_df['Total_Cost'].mean():.4f}")
print(f"• Costo minimo: ${costs_df['Total_Cost'].min():.4f}")
print(f"• Costo massimo: ${costs_df['Total_Cost'].max():.4f}")
