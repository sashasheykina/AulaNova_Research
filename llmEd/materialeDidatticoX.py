import json
from docx import Document
from docx.shared import Pt
import re
import copy


# Funzione per caricare i dati dal file JSON
def load_json_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        print("LOAD JSON DATA")
        print(json.load(file))
        return json.load(file)


# Funzione per ottenere il valore da una chiave nel JSON
def get_value_from_json(data, key_path):
    keys = key_path.split("->")
    current_data = data

    for key in keys:
        if isinstance(current_data, dict):
            current_data = current_data.get(key, None)
        else:
            return None
    return current_data


# Funzione per sostituire i segnaposto nel documento
def replace_placeholders(layout_docx, json_data, output_docx):
    doc = Document(layout_docx)
    pattern = r"<#(.*?)#>"

    # Impostiamo il font di default
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)

    paragraphs_to_remove = []

    if "diario" in json_data:
        # Iteriamo sulle colonne

        for domanda in json_data["diario"]["domande"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"DOMANDA {domanda['domanda']}")

            doc.add_paragraph("\n\n\n\n\n\n")  # Spazio tra le colonne

    if "orale" in json_data:
        print("entrato nel merito")
        doc.add_paragraph(f"{json_data['orale'][0]['tipo_materiale']}")
        doc.add_paragraph(f"Numero domande: {json_data['orale'][0]['numero_domande']}")
        doc.add_paragraph(f"Punteggio totale: {json_data['orale'][0]['punti']}")
        doc.add_paragraph(f"Criteri di valutazione: {json_data['orale'][0]['criteri_valutazione']}")
        doc.add_paragraph(f"Obiettivo minimo: {json_data['orale'][0]['obiettivo_minimo']}")
        doc.add_paragraph("\n\n")
        doc.add_paragraph(f"Istruzioni per lo svolgimento:")
        for istruzione in json_data["orale"][0]["istruzioni"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"{istruzione['descrizione']}")
        doc.add_paragraph("\n\n")
        for domanda in json_data["orale"][0]["domande"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"DOMANDA {domanda['id']}:  {domanda['domanda']}")

            doc.add_paragraph("\n\n\n\n\n\n")

    if "prerequisiti_orale" in json_data:
        print("entrato nel merito")
        doc.add_paragraph(f"{json_data['prerequisiti_orale'][0]['tipo_materiale']}")
        doc.add_paragraph(f"Numero domande: {json_data['prerequisiti_orale'][0]['numero_domande']}")
        doc.add_paragraph(f"Criteri di valutazione: {json_data['prerequisiti_orale'][0]['criteri_valutazione']}")
        doc.add_paragraph("\n\n")
        doc.add_paragraph(f"Istruzioni per lo svolgimento:")
        for istruzione in json_data["prerequisiti_orale"][0]["istruzioni"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"{istruzione['descrizione']}")
        doc.add_paragraph("\n\n")
        for domanda in json_data["prerequisiti_orale"][0]["domande"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"DOMANDA {domanda['id']}:  {domanda['domanda']}")

            doc.add_paragraph("\n\n\n\n\n\n")

    if "scritta" in json_data:
        doc.add_paragraph(f"{json_data['scritta'][0]['tipo_materiale']}")
        doc.add_paragraph(f"Numero domande: {json_data['scritta'][0]['numero_domande']}")
        doc.add_paragraph(f"Punteggio totale: {json_data['scritta'][0]['punti']}")
        doc.add_paragraph(
            f"Criteri di valutazione: {json_data['scritta'][0]['criteri_valutazione']}")
        doc.add_paragraph(
            f"Obiettivo minimo: {json_data['scritta'][0]['obiettivo_minimo']}")
        doc.add_paragraph("\n\n")
        doc.add_paragraph(f"Istruzioni per lo svolgimento:")
        for istruzione in json_data["scritta"][0]["istruzioni"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"{istruzione['descrizione']}")
        doc.add_paragraph("\n\n")
        for domanda in json_data["scritta"][0]["domande_sm_vf"][0]["domande"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"DOMANDA {domanda['id_d']}:  {domanda['domanda']}")
            i=97
            for opzione in domanda["opzioni"]:
                doc.add_paragraph(f"{chr(i)}. {opzione}")
                i=i+1
            doc.add_paragraph("Risposta:")
            doc.add_paragraph("\n")

        for domanda in json_data["scritta"][0]["domande_a"][0]["domande"]:
            # Scriviamo il titolo e l'obiettivo della colonna
            doc.add_paragraph(f"DOMANDA {domanda['id_d']}:  {domanda['domanda']}")
            doc.add_paragraph("Risposta:")
            doc.add_paragraph("\n")


    if "Brainstorming" in json_data:
        doc.add_paragraph(f"BRAINSTORMING")
        # Iteriamo sulle colonne
        for domanda in json_data["Brainstorming"]["domande"]:
            # Scriviamo il titolo e la domanda
            doc.add_paragraph(f"DOMANDA {domanda['id']}: {domanda['domanda']}")
            doc.add_paragraph(f"Tipo domanda: {domanda['tipo_domanda']}")

            # Aggiungiamo le risposte
            if "risposte" in domanda and domanda["risposte"]:
                doc.add_paragraph(f"Possibili risposte: {domanda['risposte']}")

            doc.add_paragraph("\n")

    if "TestNonStrutturato" in json_data:
        doc.add_paragraph(f"TEST NON STRUTTURATO")
        testo = json_data["TestNonStrutturato"]
        doc.add_paragraph(f"Tipo domanda: {testo['tipo_domanda']}")
        doc.add_paragraph(f"Punti totali: {testo['punti']}")
        doc.add_paragraph(f"Modalità valutazione: {testo['modalità_valutazione']}")
        doc.add_paragraph(f"Obiettivo minimo: {testo['obiettivo_minimo']}")


        # Iteriamo sulle colonne
        for domanda in json_data["TestNonStrutturato"]["domande"]:
            # Scriviamo il titolo e la domanda
            doc.add_paragraph(f"DOMANDA {domanda['id']}: {domanda['domanda']}")
            doc.add_paragraph(f"Criteri di valutazione {domanda['id']}: {domanda['criteri']}")

    if "TestStrutturato" in json_data:
        doc.add_paragraph(f"TEST STRUTTURATO")
        testo = json_data["TestStrutturato"]
        doc.add_paragraph(f"Tipo domanda: {testo['tipo_domanda']}")
        doc.add_paragraph(f"Punti totali: {testo['punti']}")
        doc.add_paragraph(f"Modalità valutazione: {testo['modalità_valutazione']}")
        doc.add_paragraph(f"Obiettivo minimo: {testo['obiettivo_minimo']}")

        # Iteriamo sulle colonne
        for domanda in json_data["TestStrutturato"]["domande"]:
            # Scriviamo il titolo e la domanda
            doc.add_paragraph(f"DOMANDA {domanda['id']}: {domanda['domanda']}")
            if domanda.get("opzioni"):
                for post in domanda["opzioni"]:
                    doc.add_paragraph(f"{post['id_o']}: {post['risposta']}")
            doc.add_paragraph(f"Risposta corretta: {domanda['risposta']}")

            doc.add_paragraph("\n")

    if "TestSemiStrutturato" in json_data:
        doc.add_paragraph(f"TEST SEMI STRUTTURATO")
        testo = json_data["TestSemiStrutturato"]
        doc.add_paragraph(f"Tipo domanda: {testo['tipo_domanda']}")
        doc.add_paragraph(f"Punti titali: {testo['punti_totali']}")
        doc.add_paragraph(f"Modalità valutazione: {testo['modalità_valutazione']}")
        doc.add_paragraph(f"Obiettivo minimo: {testo['obiettivo_minimo']}")


        for group in json_data["TestSemiStrutturato"]["domande_sm_vf"]:
            for domanda in group["domande"]:
                doc.add_paragraph(f"DOMANDA {domanda['id_d']}: {domanda['domanda']}")
                if domanda.get("opzioni"):
                    for opzione in domanda["opzioni"]:
                        doc.add_paragraph(f"  - {opzione['id_o']}: {opzione['risposta']}")
                doc.add_paragraph(f"Risposta corretta: {domanda['risposta_corretta']}")
                doc.add_paragraph("\n")

        for group in json_data["TestSemiStrutturato"]["domande_a"]:
            for domanda in group["domande"]:
                doc.add_paragraph(f"DOMANDA {domanda['id_d']}: {domanda['domanda']}")
                if domanda.get("opzioni"):
                    for opzione in domanda["opzioni"]:
                        doc.add_paragraph(f"  - {opzione['id_o']}: {opzione['risposta']}")
                doc.add_paragraph("\n")

    if "CaseStudy" in json_data:
        doc.add_paragraph(f"CASO D'USO")
        # Iteriamo sui casi
        for caso in json_data["CaseStudy"]["casi"]:
            doc.add_paragraph(f"GRUPPO {caso['id']}:")
            doc.add_paragraph(f"Descrizione: {caso['descrizione']}")
        doc.add_paragraph(f"DOMANDE")
        # Iteriamo sulle domande
        for domanda in json_data["CaseStudy"]["domande"]:
            doc.add_paragraph(f"Domanda {domanda['id']}: {domanda['domanda']}")

            # Iteriamo sulle sotto-domande, se presenti
            if "sub_domanda" in domanda:
                for sub in domanda["sub_domanda"]:
                    doc.add_paragraph(f"  - {sub['id']}: {sub['domanda']}")

            doc.add_paragraph("\n")

    if "Quiz" in json_data:
        doc.add_paragraph(f"QUIZ")
        # Iteriamo sulle colonne
        for domanda in json_data["Quiz"]["domande"]:
            # Scriviamo il titolo e la domanda
            doc.add_paragraph(f"DOMANDA {domanda['id_d']}: {domanda['domanda']}")
            doc.add_paragraph(f"Tipo domanda: {domanda['tipo_domanda']}")

            if domanda.get("opzioni"):
                for post in domanda["opzioni"]:
                    doc.add_paragraph(f"{post['id_o']}: {post['risposta']}")
            doc.add_paragraph(f"Risposta corretta: {domanda['risposta']}")

            doc.add_paragraph("\n")

    if "Mappa" in json_data:
        # Aggiungi il nodo centrale
        doc.add_paragraph(f"NODO CENTRALE: {json_data['Mappa']['nodo_centrale']}")

        # Iteriamo sui rami principali
        for domanda in json_data["Mappa"]["rami"]:
            # Scriviamo il ramo principale
            doc.add_paragraph(f"RAMO {domanda['id']}: {domanda['ramo_principale']}")

            # Aggiungere le risposte, se ci sono
            if "sotto_rami" in domanda and domanda["sotto_rami"]:
                for sotto_ramo in domanda["sotto_rami"]:
                    # Aggiungiamo ogni sotto-ramo
                    doc.add_paragraph(
                        f" - {sotto_ramo['sr']}")  # Ogni sotto_ramo è rappresentato come una stringa in 'sr'

            # Aggiungiamo una linea vuota per separare i rami
            doc.add_paragraph("\n")

    for paragraph in doc.paragraphs:
        matches = re.findall(pattern, paragraph.text)
        for match in matches:
            # Verifica se il segnaposto è istruzioni->id o istruzioni->descrizione
            if match.startswith("istruzioni->"):
                key = match.split("->")[1]  # Prendi la parte dopo 'istruzioni->' (id o descrizione)
                value = get_value_from_json(json_data, "istruzioni")

                if value is not None and isinstance(value, list):
                    if key == "descrizione":
                        # Restituisci le descrizioni
                        value = "\n".join(
                            f"{istruzione['id']}. {istruzione['descrizione']}" for istruzione in value)
                else:
                    value = "N/A"
            else:
                value = get_value_from_json(json_data, match)

                # Se il valore è una lista (come nel caso di "Obiettivi specifici"), trattalo come elenco puntato
                if isinstance(value, list):
                    value = "\n".join(f"• {item}" for item in value)

            # Se il valore è None, usa "N/A"
            if value is None:
                value = "N/A"

            # Converte qualsiasi altro tipo in stringa
            else:
                value = str(value)

            # Sostituisci il segnaposto con il valore nel paragrafo
            paragraph.text = paragraph.text.replace(f"<#{match}#>", str(value))

            # Se il valore è "N/A", aggiungi il paragrafo alla lista da rimuovere
            if "N/A" in value:
                paragraphs_to_remove.append(paragraph)

    # Rimuovi i paragrafi con "N/A"
    for para in paragraphs_to_remove:
        # Rimuovi il paragrafo dal documento
        p_element = para._element
        p_element.getparent().remove(p_element)

    # Salva il documento aggiornato
    doc.save(output_docx)

'''
if __name__ == "__main__":
    template_pptx = "LayoutPrerequisiti.pptx"
    json_file = "prerequisiti_orale.json"
    output_pptx = "prerequisiti_orale.docx"

    try:
        with open(json_file, 'r', encoding="utf-8") as f_json:
            json_data = json.load(f_json)  # Correctly load JSON data from file
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
        exit(1)  # Exit if the JSON file cannot be found
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {json_file}: {e}")
        exit(1)  # Exit if there's a JSON parsing error


    replace_placeholders("LayoutMateriale.docx", json_data, "autovalutazione.docx")'''