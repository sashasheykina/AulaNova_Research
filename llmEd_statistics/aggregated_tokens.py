import pandas as pd
import os

# Percorso dei CSV
path = r"/"

# Carica il file
file_path = os.path.join(path, "statistics/execution_tokens.csv")
df = pd.read_csv(file_path, sep=',')

activities = ["Annual Lesson Plan", "Uda Planning", "Didactic Material", "Lesson Total Generation", "Total Activity Generation"]

records_input = []
records_output = []

for participant_id in range(1, 21):
    participant_data = df[df['Participant_ID'] == participant_id]

    data_input = {"Partecipante": participant_id}
    data_output = {"Partecipante": participant_id}

    total_input = 0
    total_output = 0

    for activity in activities:
        # Input tokens - converti direttamente in int
        input_val = participant_data.loc[participant_data["Activity"] == activity, "Input_Tokens"]
        input_val = int(input_val.values[0]) if len(input_val) > 0 else 0
        data_input[activity] = input_val


        # Output tokens - converti direttamente in int
        output_val = participant_data.loc[participant_data["Activity"] == activity, "Output_Tokens"]
        output_val = int(output_val.values[0]) if len(output_val) > 0 else 0
        data_output[activity] = output_val


    records_input.append(data_input)
    records_output.append(data_output)

# Crea DataFrame
final_df_input = pd.DataFrame(records_input).sort_values(by="Partecipante", ascending=True)
final_df_output = pd.DataFrame(records_output).sort_values(by="Partecipante", ascending=True)

# Salva i file
final_df_input.to_csv(os.path.join(path, "statistics/input_tokens_aggregated.csv"), index=False)
final_df_output.to_csv(os.path.join(path, "statistics/output_tokens_aggregated.csv"), index=False)

print("✅ File creati con numeri interi!")
print(
    f"📊 Esempio valori: {final_df_input.iloc[0]['Didactic Material']} (tipo: {type(final_df_input.iloc[0]['Didactic Material'])})")