import os
from datetime import datetime
import json
import streamlit as st
import Utility
import Utility_last
from materialeDidatticoX import replace_placeholders
from merge_slides import insert_slides_at_tag, clenup_lezioneSimulata, remove_slide_with_tag
import unicodedata
import re
import logging
import uuid
import shutil

from wordX import replace_placeholder_in_paragraph


def aggiorna_elencoUDA():
    # Carica i dati dal file JSON

    uda_file = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
    print(uda_file)
    with open(uda_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Estrai le "UDA" in una lista
    elencoUda = [unita["UDA"] for unita in data["Unita Didattiche"]]
    # Aggiorna la lista di UDA nello stato della sessione
    st.session_state.uda_options = elencoUda  # Questo aggiornerà il selectbox automaticamente


def calcola_durata_totale(elenco_path):
    durata_totale = 0

    # Carica il file esecuzione.json
    with open(elenco_path, 'r', encoding='utf-8') as file:
        esecuzione = json.load(file)

    # Somma le durate delle attività
    for fase in esecuzione.get("fasi", []):
        for attivita in fase.get("lista_attivita", []):
            durata_str = attivita.get("durata", "0 minuti")

            # Estrai il numero dalla durata
            match = re.search(r'\d+', durata_str)
            if match:
                durata_totale += int(match.group())
    warn = st.container()
    if durata_totale>500:
        alert = warn.warning('La durata della fase è troppo lunga; suggeriamo di ridurla, suddividerla in più segmenti o posticipare un\'attività alla lezione successiva.', icon="⚠️")
        alert.empty()
    if durata_totale<10:
        alert = warn.warning('La durata della fase è troppo breve;  suggeriamo di integrare con attività di approfondimento, esercitazioni pratiche, momenti di valutazione formativa o strumenti didattici multimediali per raggiungere la durata ottimale.', icon="⚠️")
        alert.empty()
    return durata_totale


def aggiorna_elencoLezioni():
    # Carica i dati dal file JSON
    lezioni_file = os.path.join(st.session_state["user_dir"], "elencoLezioni.json")
    with open(lezioni_file, 'r', encoding="utf-8") as f:
        data = json.load(f)

    # Estrai le "UDA" in una lista
    elencoLezioni = [unita["Lezione"] for unita in data["Lezioni"]]

    # Aggiorna la lista di UDA nello stato della sessione
    st.session_state.lezione_options = elencoLezioni

def lineeGuida(art, disciplina, grado):
    linee_guida = open("LINEE GUIDA/afm_rim_informatica", "r", encoding="utf-8").read()
    ore_anno = 66
    ore_settimana = 2
    if art == 'Relazioni internazionali per il Marketing':
        if disciplina == 'Tecnologie della comunicazione':
            linee_guida = open("LINEE GUIDA/afm_rim_tdc", "r", encoding="utf-8").read()
            ore_anno = 66
            ore_settimana = 2
    if art == 'Grafica e Comunicazione':
        if disciplina == 'Progettazione multimediale':
            linee_guida = open("LINEE GUIDA/gec_pm", "r", encoding="utf-8").read()
            if grado =="III":
                ore_anno = 99
                ore_settimana = 3
            else:
                ore_anno = 132
                ore_settimana = 4
    if art == 'Sistemi informativi aziendali':
        if disciplina == 'Informatica':
            linee_guida = open("LINEE GUIDA/afm_sia_informatica", "r", encoding="utf-8").read()
            if grado=="I" or grado =="II":
                ore_anno = 66
                ore_settimana = 2
            elif grado =="III":
                ore_anno = 132
                ore_settimana = 4
            else:
                ore_anno = 165
                ore_settimana = 5
    if art == 'Informatica':
        if disciplina == 'Sistemi e reti':
            linee_guida = open("LINEE GUIDA/iet_i_ser", "r", encoding="utf-8").read()
            ore_anno = 132
            ore_settimana = 4
        elif disciplina == 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_i_tpsit", "r", encoding="utf-8").read()
            if grado=="V":
                ore_anno = 132
                ore_settimana = 4
            else:
                ore_anno = 99
                ore_settimana = 3
        elif disciplina == 'Gestione progetto, organizzazione di impresa':
            linee_guida = open("LINEE GUIDA/iet_i_gpoi", "r", encoding="utf-8").read()
            ore_anno = 99
            ore_settimana = 3
        elif disciplina == 'Informatica':
            linee_guida = open("LINEE GUIDA/iet_i_inf", "r", encoding="utf-8").read()
            ore_anno = 198
            ore_settimana = 6
        elif disciplina == 'Telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_i_tel", "r", encoding="utf-8").read()
            ore_anno = 99
            ore_settimana = 3
    if art == 'Telecomunicazioni':
        if disciplina == 'Sistemi e reti':
            linee_guida = open("LINEE GUIDA/iet_t_ser", "r", encoding="utf-8").read()
            ore_anno = 132
            ore_settimana = 4
        elif disciplina == 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_t_tpsit", "r", encoding="utf-8").read()
            if grado=="V":
                ore_anno = 132
                ore_settimana = 4
            else:
                ore_anno = 99
                ore_settimana = 3
        elif disciplina == 'Gestione progetto, organizzazione di impresa':
            linee_guida = open("LINEE GUIDA/iet_t_gpoi", "r", encoding="utf-8").read()
            ore_anno = 99
            ore_settimana = 3
        elif disciplina == 'Informatica':
            linee_guida = open("LINEE GUIDA/iet_t_inf", "r", encoding="utf-8").read()
            ore_anno = 99
            ore_settimana = 3
        elif disciplina == 'Telecomunicazioni':
            linee_guida = open("LINEE GUIDA/iet_t_tel", "r", encoding="utf-8").read()
            ore_anno = 198
            ore_settimana = 6
    if art == 'Scienze Applicate':
        linee_guida = open("LINEE GUIDA/liceo", "r", encoding="utf-8").read()
        ore_anno = 66
        ore_settimana = 2
    if art == 'Biennio comune':
        if disciplina == 'Tecnologie informatiche':
            linee_guida = open("LINEE GUIDA/iet_bc_ti", "r", encoding="utf-8").read()
            ore_anno = 99
            ore_settimana = 3
        elif disciplina == 'Scienze e tecnologie applicate':
            linee_guida = open("LINEE GUIDA/iet_bc_sta", "r", encoding="utf-8").read()
            ore_anno = 99
            ore_settimana = 3
    return linee_guida, ore_anno, ore_settimana

def periodoUda(uda_name):
    uda_file = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
    with open(uda_file, 'r', encoding="utf-8") as f:
        data = json.load(f)
    # Carica il JSON
    for uda in data['Unita Didattiche']:
        if uda['UDA'] == uda_name:
            return uda['Periodo']
    return "UDA non trovata."

def elencoLezioni(its, grado, indirizzo, articolazione, linee_guida, disciplina, uda, periodo, ore_anno, ore_sett, contesto, client, commento):
    uda_file = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
    elencoUda = open(uda_file, "r").read()
    formato_output = open("formato_output_elenco_lezioni", "r").read()
    role_system = (
        f"Agisci da esperto docente di Informatica negli {its}. {linee_guida}. Il tuo compito è fornire l’elenco delle lezioni da attivare per una specifica Unità didattica di Apprendimento che ti fornirò nell’ambito della progettazione didattica. "
        f"per la disciplina {disciplina}. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}."
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE {contesto}. ### GRADO CLASSE  {grado}. ad indirizzo {indirizzo}, articolazione {articolazione}."
    )
    role_user = (
        f"Io ti fornirò l'analisi del profilo della classe, l'anno di riferimento, l'elenco delle UDA, la UDA di riferimento, priodo di svolgimento, ore setiimanali, monte ore annuo e tuo restituirai l’elenco "
        f"delle lezioni (concentrandoci esclusivamente sui contenuti teorici delle lezioni) per la Progettazione Disciplinare nel formato richiesto. ### CONTESTO CLASSE {contesto_classe}. ### ELENCO UNITA’ DIDATTICHE: {elencoUda}. ### UNITA’ DIDATTICA {uda}. "
        f"### PERIODO {periodo}. ### NUMERO DI ORE SETTIMANALI {str(ore_sett)}. ### TOTALE ORE ANNO SCOLASTICO {str(ore_anno)}.  **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento} "
        f"ELENCO LEZIONI: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ]
    )

    # Estrarre la risposta testuale dall'oggetto completion
    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            elenco_path = os.path.join(st.session_state["user_dir"], "elencoLezioni.json")
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)


def setup_logger(user_id, function_name, log_file='loggingINFO.log'):
    if not os.path.exists(log_file):
        open(log_file, 'w').close()

    logger = logging.getLogger("LoggingINFO")
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [User ID: %(user_id)s] - [Function: %(function_name)s] - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logging.LoggerAdapter(logger, {"user_id": user_id, "function_name": function_name})

def dettaglioUDA(its, grado, indirizzo, articolazione, linee_guida, disciplina, uda, contesto, docente, ore_sett, ore_anno, client, commento):

    uda_file = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
    with open(uda_file, 'r', encoding="utf-8") as f:
        elencoUda = json.load(f)
    formato_output = open("formato_output_dettaglioUda", "r", encoding="utf-8").read()
    diario = open("diarioCp.json", "r", encoding="utf-8").read()
    ore_s = str(ore_sett)
    oa = str(ore_anno)
    response_data = None
    elenco_path = os.path.join(st.session_state["user_dir"], "dettaglioUDA.json")
    role_system = (
            f"Agisci da esperto docente di Informatica negli {its}. {linee_guida} "
            f"Il tuo compito è fornire il dettaglio dell’Unità didattica di Apprendimento che ti fornirò nell’ambito della progettazione didattica per la disciplina {disciplina}, "
            f"in linea con le indicazioni nazionali. Dovrai fornire la Progettazione Disciplinare tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE  {contesto}. ### GRADO CLASSE  {grado} ad indirizzo {indirizzo}, articolazione {articolazione}. "
    )
    role_user = (
            f"Io ti fornirò l'analisi del profilo della classe e l'anno di riferimento, numero ore settimanali, monte ore annuo, nome docente, l'elenco delle UDA, la UDA di riferimento, includi tutti metodologie didattiche nella progettazione, "
            f"esempio di relazione individuale da proporre allo studente e tu restituirai il dettaglio dell’unità didattica di apprendimento "
            f"per la Progettazione Disciplinare nel formato richiesto.  ### CONTESTO CLASSE {contesto_classe}  ### NUMERO ORE SETTIMANALI {ore_s} "
            f"### TOTALE ORE ANNO {oa}. ### DOCENTE: {docente}.  ### ELENCO UDA: {elencoUda}  ### UDA: {uda}."
            f"### RELAZIONE INDIVIDUALE: {diario}. **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento}." 
            f"DETTAGLIO UDA: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.7,
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ]
    )


    # Estrarre la risposta testuale dall'oggetto completion
    response_text = completion.choices[0].message.content


    # Se necessario, pulisci il contenuto per estrarre solo il JSON valido
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        cleaned_json_text = response_text[json_start:json_end]


        try:
            response_data = json.loads(cleaned_json_text)
            # Salvataggio della risposta in un file JSON
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            #print("Errore nel decodificare il JSON:", e)
            #print("Contenuto JSON estratto:", cleaned_json_text)
            logger = setup_logger(st.session_state["user_dir"], "dettaglioUDA")
            logger.debug(f"Errore nel decodificare il JSON: {e}")
            logger.debug(f"Contenuto JSON estratto:\n{cleaned_json_text}")
            logger.debug(f"role_system: {role_system}")
            logger.debug(f"role_user: {role_user}")
    else:
        #print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        #print("Contenuto della risposta:", response_data)
        logger = setup_logger(st.session_state["user_dir"], "dettaglioUDA")
        logger.debug("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        logger.debug(f"Contenuto della risposta:\n{response_text}")
        logger.debug(f"role_system: {role_system}")
        logger.debug(f"role_user: {role_user}")

    return response_data

'''
    response_data = None  # Inizializza response_data
    # Convertire in un oggetto Python
    try:
        response_data = json.loads(cleaned_json_text)

    except json.JSONDecodeError as e:
        # Stampa l'errore e la posizione
        print(f"Errore nella decodifica JSON: {e}")
        print("JSON problematica:", cleaned_json_text)

        # Aggiungi ulteriori controlli per trovare il problema
        for i, line in enumerate(cleaned_json_text.splitlines()):
            print(f"Riga {i + 1}: {line}")'''

def elencoUDA(its, grado, indirizzo, articolazione, linee_guida, disciplina, contesto, client, commento):

    formato_output = open("formato_output_elencoUda", "r").read()
    role_system = (
            f"Agisci da esperto docente di Informatica negli {its}. {linee_guida} "
            f"Il tuo compito è fornire la progettazione didattica per la disciplina {disciplina}, "
            f"in linea con le indicazioni nazionali. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
            f"### ANALISI PROFILO CLASSE  {contesto}. ### GRADO CLASSE DI RIFERIMENTO  {grado} ad indirizzo {indirizzo}, articolazione {articolazione} "
         )
    role_user = (
            f"Io ti fornirò l'analisi del profilo della classe e il grado classe di riferimento, "
            f"e tu restituirai la Progettazione Disciplinare nel formato richiesto JSON. {contesto_classe}. **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento} "
            f"ELENCO UDA: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ],
    )


    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]
        #print(json_text)

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            elenco_path = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
            print("Ciao")
            print(elenco_path)
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)
            print("la risposta è stato creata")
            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            print("Errore nel decodificare il JSON:", e)
            print("Contenuto JSON estratto:", json_text)
    else:
        print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        print("Contenuto della risposta:", response_text)

def genera_PDD(its, grado, indirizzo, articolazione, linee_guida, disciplina, contesto, docente, ore_sett, ore_anno, client, commento):

    # Carica l'elenco delle UDA dal file JSON
    uda_file = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
    with open(uda_file, "r", encoding="utf-8") as f:
        elenco_uda = json.load(f)
        # Recupera il valore associato alla chiave "BES"
        valore_bes = elenco_uda.get("BES/DSA", None)  # Restituisce None se "BES" non esiste

    current_year = datetime.now().year
    anno = str(current_year)+"/"+str(current_year+1)
    dettagli_path = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
    try:
        with open(dettagli_path, 'w', encoding='utf-8') as json_file:
            dati = {
                "ordinamento scuola": "Scuola secondaria di II grado",
                "tipo scuola": its,
                "grado": grado,
                "indirizzo": indirizzo,
                "articolazione": articolazione,
                "disciplina": disciplina,
                "contesto": contesto,
                "docente": docente,
                "anno_scolastico": anno,
                "ore_settimanali": ore_sett,
                "ore_annue": ore_anno,
                "BES": valore_bes,
                "Unita Didattiche": []
            }
            json.dump(dati, json_file, ensure_ascii=False, indent=4)
        print(f"Dati scritti con successo nel file '{dettagli_path}'.")
    except Exception as e:
        print(f"Si è verificato un errore durante la scrittura nel file: {e}")

    # Itera su ciascuna UDA e genera il dettaglio
    for uda in elenco_uda["Unita Didattiche"]:
        #dettaglio = None
        #print("#################################################")
        dettaglio = dettaglioUDA(its, grado, indirizzo,  articolazione, linee_guida, disciplina, uda, contesto, docente, ore_sett, ore_anno, client, commento)
        #print("QUESTO é IL DETTAGLIO GENERATO:"+str(dettaglio))
        #print("#################################################")
        nome_file = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
        update_file_progettazione_didattica(dettaglio, nome_file)


def update_file_progettazione_didattica(response_text, nome_file):

    # Leggi il file JSON esistente
    try:
        with open(nome_file, 'r', encoding='utf-8') as file_json:
            dati = json.load(file_json)
            # Controlla che "Unita Didattiche" sia una lista
            if "Unita Didattiche" in dati and isinstance(dati["Unita Didattiche"], list):
                # Aggiungi il nuovo dato alla lista "Unita Didattiche"
                dati["Unita Didattiche"].append(response_text)
            else:
                print("Errore: 'Unita Didattiche' non è una lista o non esiste.")
                return
    except FileNotFoundError:
        print(f"Errore: il file '{nome_file}' non è stato trovato.")
        return
    except json.JSONDecodeError:
        print("Errore nella decodifica del file JSON.")
        return

    # Scrivi il file JSON aggiornato
    with open(nome_file, 'w', encoding='utf-8') as file_json:
        json.dump(dati, file_json, ensure_ascii=False, indent=4)

    print(f"File JSON '{nome_file}' aggiornato con successo.")

def getProgettazione(its, grado, indirizzo, articolazione, linee_guida, disciplina, lezione, contesto, docente, client, udaName, commento):

    data_oggi = datetime.now()
    current_year = datetime.now().year
    anno = str(current_year) + "/" + str(current_year + 1)

    # Controlla il mese corrente: se siamo prima di settembre, usa l'anno precedente
    if data_oggi.month < 9:
        anno = f"{current_year - 1}/{current_year}"
    pdd_file = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
    dettaglioUda = None
    elencoUda = open(os.path.join(st.session_state["user_dir"], "elencoUDA.json"), "r").read()
    with open(pdd_file, 'r', encoding="utf-8") as f:
        dettUda = json.load(f)
    trovata = False
    for uda in dettUda.get("Unita Didattiche", []):
        print(uda.get("UNITA DI APPRENDIMENTO"))
        if uda.get("UNITA DI APPRENDIMENTO") == udaName:
            dettaglioUda = uda
            trovata = True
            break  # Uscire dal ciclo una volta trovata l'UDA

    print(trovata)
    # Stampa il messaggio solo se l'UDA non è stata trovata
    if not trovata:
        print(f"L'UDA con nome '{udaName}' non è stata trovata.")

    elencoLezioni_file = os.path.join(st.session_state["user_dir"], "elencoLezioni.json")
    elencoLezioni = open(elencoLezioni_file, "r").read()
    # Carica il file JSON
    with open(elencoLezioni_file, "r", encoding="utf-8") as f:
        elencoLezioni_json = json.load(f)  # Converti il file JSON in un dizionario

    # Ora elencoLezioni è un dizionario e possiamo accedere a "Lezioni"
    lezioni = elencoLezioni_json["Lezioni"]

    # Controlla se è l'ultima lezione
    ultima_lezione = lezioni[-1]["Lezione"]

    # Se è l'ultima lezione, stampa "ciao"
    if lezione == ultima_lezione:
        formato_output = open("formato_output_progettazione", "r").read()

    else:
        formato_output = open("formato_output_progettazione_withoutCP", "r").read()

    role_system = (
        f"Agisci da esperto docente di Informatica negli {its}. {linee_guida}"
        f"Il tuo compito è fornire la progettazione didattica per la disciplina {disciplina}. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output}"
    )
    contesto_classe = (
        f"### ANALISI PROFILO CLASSE  {contesto}. ### GRADO CLASSE  {grado} ad indirizzo {indirizzo}, articolazione {articolazione}."
    )
    role_user = (
        f"Io ti fornirò elenco unità didattiche, unita di aprendimento, dettaglio unita didattica di riferimento, elenco lezioni, la lezione, l'analisi del profilo della classe, nome docente, data di oggi, anno scolastico corrente, "
        f"e tu restituirai la fase itroduttiva della lezione simulata nella Progettazione Disciplinare nel formato richiesto JSON. ### ELENCO UDA: {elencoUda}. "
        f"### UNITÀ DIDATTICA DI APPRENDIMENTO: {udaName}. ### DETTAGLIO UDA: {dettaglioUda}. ### ELENCO LEZIONI: {elencoLezioni}. ### LEZIONIE: {lezione}. ### CONTESTO CLASSE {contesto_classe}. ### DOCENTE: {docente}. ### DATA DI OGGI: {data_oggi}. ### ANNO SCOLASTICO: {anno}. **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento}"
        f"PROGETTAZIONE LEZIONE SIMULATA: "
    )

    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature = 0.7,
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ],
    )

    response_text = completion.choices[0].message.content
    response_text = unicodedata.normalize('NFKD', response_text)

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]
        # print(json_text)

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON
            elenco_path = os.path.join(st.session_state["user_dir"], "progettazione.json")
            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")

        except json.JSONDecodeError as e:
            #print("Errore nel decodificare il JSON:", e)
            #print("Contenuto JSON estratto:", json_text)
            logger = setup_logger(st.session_state["user_dir"], "getProgettazione")
            logger.debug(f"Errore nel decodificare il JSON: {e}")
            logger.debug(f"Contenuto JSON estratto:\n{json_text}")
            logger.debug(f"role_system: {role_system}")
            logger.debug(f"role_user: {role_user}")
    else:
        #print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        #print("Contenuto della risposta:", response_text)
        logger = setup_logger(st.session_state["user_dir"], "getProgettazione")
        logger.debug("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        logger.debug(f"Contenuto della risposta:\n{response_text}")
        logger.debug(f"role_system: {role_system}")
        logger.debug(f"role_user: {role_user}")

    # Percorso del file JSON
    elenco_path = os.path.join(st.session_state["user_dir"], "progettazione.json")

    # Leggi il file JSON
    with open(elenco_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    # Aggiorna il valore del contesto
    data["contesto"] = contesto

    # Scrivi di nuovo il file JSON
    with open(elenco_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def getEsecuzione(client, commento):

    progettazione_file = os.path.join(st.session_state["user_dir"], "progettazione.json")
    formato_output_esecuzione = open("formato_output_esposizione", "r").read()

    with open(progettazione_file, 'r', encoding="utf-8") as f:
        progettazione = json.load(f)
    # Recupera il valore della chiave "durata"
    durata = progettazione.get("durata")
    metodologie = progettazione.get("metodologie", {}).get("metodologie", [])
    metodologie_lista = [item["m"] for item in metodologie]
    # Controlla se il file esiste e cancellalo
    elenco_path = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    if os.path.exists(elenco_path):
        os.remove(elenco_path)
        print(f"Il file {elenco_path} è stato cancellato con successo.")
    else:
        print(f"Il file {elenco_path} non esiste.")
    elenco_path1 = os.path.join(st.session_state["user_dir"], "esposizione.json")
    if os.path.exists(elenco_path1):
        os.remove(elenco_path1)
        print(f"Il file {elenco_path1} è stato cancellato con successo.")
    else:
        print(f"Il file {elenco_path1} non esiste.")
    role_system = (
        f"Agisci da esperto docente di informatica nelle scuole secondarie di secondo grado. Stai progettando una lezione per la tua classe. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output_esecuzione}."
    )
    role_user = (
        f"Considera che le macrofasi della lezione sono: "
        f"    - Verifica dei prerequisiti "
        f"    - Nucleo centrale "
        f"    - Verifica degli obiettivi "
        f"Io ti fornirò la progettazione della lezione, le metodologie didattiche, durata della fase Nucleo centrale della lezione in minuti e tu restituirai le sottofasi per ciascuna delle fasi sopraindicate per utilizzare le metodologie didattiche e gli strumenti che abbiamo fino ad ora previsto."
        f"**Importante:** Devi creare un attività per ogni metodologia didattica. Nella FASE Verifica degli obiettivi, devi generare due attività: una per la metodologia Verifica scritta e l'altra per la metodologia Verifica orale. Nella FASE Verifica dei prerequisiti nella metodologia devi scegliere tra Verifica scritta e Verifica orale."
        f"Considera l'analisi della classe e la durata totale della fase Nucleo centrale della lezione, e trova un equilibrio con il numero e il tipo delle attività."
        f"### PROGETTAZIONE: {progettazione}. ### METODOLOGIE DIDATTICHE: {metodologie_lista}. ### DURATA TOTALE DELLA FASE NUCLEO CENTRALE IN MINUTI: {durata}. **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento}."
        f"ESPOSIZIONE LEZIONE SIMULATA: "
    )
    completion = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.7,
        messages=[
            {"role": "system", "content": role_system},
            {"role": "user", "content": role_user}
        ],
    )

    response_text = completion.choices[0].message.content

    # Pulire la risposta per trovare solo il JSON
    json_start = response_text.find('{')
    json_end = response_text.rfind('}') + 1

    if json_start != -1 and json_end != -1:
        json_text = response_text[json_start:json_end]

        try:
            response_data = json.loads(json_text)
            # Salvataggio della risposta in un file JSON

            with open(elenco_path, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=2)

            print(f"La risposta è stata salvata in {elenco_path}")
        except json.JSONDecodeError as e:
            #print("Errore nel decodificare il JSON:", e)
            #print("Contenuto JSON estratto:", json_text)
            logger = setup_logger(st.session_state["user_dir"], "getEsecuzione")
            logger.debug(f"Errore nel decodificare il JSON: {e}")
            logger.debug(f"Contenuto JSON estratto:\n{json_text}")
            logger.debug(f"role_system: {role_system}")
            logger.debug(f"role_user: {role_user}")
    else:
        #print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        #print("Contenuto della risposta:", response_text)
        logger = setup_logger(st.session_state["user_dir"], "getEsecuzione")
        logger.debug("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
        logger.debug(f"Contenuto della risposta:\n{response_text}")
        logger.debug(f"role_system: {role_system}")
        logger.debug(f"role_user: {role_user}")

    progettazione_finale_file = os.path.join(st.session_state["user_dir"], "progettazione_finale.json")
    durata_totale = calcola_durata_totale(elenco_path)
    # Leggi il contenuto del file di progettazione con la durata attuale

    with open(progettazione_file, 'r', encoding='utf-8') as file:
        progettazione_dati = json.load(file)

    # Aggiorna il valore della durata
    progettazione_dati['durata'] = str(durata_totale)

    # Scrivi i dati aggiornati nel nuovo file
    with open(progettazione_finale_file, 'w', encoding='utf-8') as file:
        json.dump(progettazione_dati, file, ensure_ascii=False, indent=2)

def getEsposizione(client, commento):
    progettazione_file = os.path.join(st.session_state["user_dir"], "progettazione_finale.json")

    with open(progettazione_file, 'r', encoding="utf-8") as f:
        progettazione = json.load(f)
    # Recupera il valore della chiave "docente"
    docente = progettazione.get("docente")
    user_dir = st.session_state["user_dir"]
    esecuzione_path = os.path.join(user_dir, "esecuzione.json")
    esposizione_path = os.path.join(user_dir, "esposizione.json")
    aggiorna_esposizione(esecuzione_path, esposizione_path, docente)
    try:
        with open(esecuzione_path, 'r', encoding='utf-8') as file:
            esecuzione = json.load(file)  # Carica il JSON come struttura Python (lista o dizionario)
    except FileNotFoundError:
        print(f"Errore: Il file {esecuzione_path} non esiste.")
        esecuzione = None
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing del JSON: {e}")
        esecuzione = None
    formato_output_sub_att = open("formato_output_sub_att", "r").read()
    # Verifica che esecuzione sia una lista
    if isinstance(esecuzione, dict):
        fasi = esecuzione.get("fasi", [])
        role_system = (
            f"Agisci da esperto docente di informatica nelle scuole secondarie di secondo grado. Stai progettando una lezione per la tua classe. Dovrai fornire la progettazione tramite un JSON strutturato come segue: {formato_output_sub_att}. Considera la seguente progettazione: {esecuzione}"
        )

        for fase_inst in fasi:
            fase = fase_inst.get("FASE", "Fase non specificata")
            #print(f"Elaborazione della fase: {fase}")
            for attivita_inst in fase_inst.get('lista_attivita', []):  # Usa get per evitare errori se 'lista_attivita' non esiste
                if isinstance(attivita_inst, dict):
                    attivita = attivita_inst['attivita']
                    print(f"  Attività: {attivita_inst['attivita']}")

                    role_user = (
                        f"Il tuo task è progettare nel dettaglio l'attività della fase che ti fornirò di seguito: {attivita}. **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento}"
                        f" Rispondi solo con il JSON e niente altro."
                    )
                    completion = client.chat.completions.create(
                        model="gpt-4o",
                        temperature = 0.7,
                        messages=[
                            {"role": "system", "content": role_system},
                            {"role": "user", "content": role_user}
                        ],
                    )
                    response_text = completion.choices[0].message.content

                    # Pulire la risposta per trovare solo il JSON
                    json_start = response_text.find('[')
                    json_end = response_text.rfind(']') + 1

                    if json_start != -1 and json_end != -1:
                        json_text = response_text[json_start:json_end]

                        try:
                            sub_attivita = json.loads(json_text)
                        except json.JSONDecodeError as e:
                            #print("Errore nel decodificare il JSON:", e)
                            #print("Contenuto JSON estratto:", json_text)
                            logger = setup_logger(st.session_state["user_dir"], "getEsposizione")
                            logger.debug(f"Errore nel decodificare il JSON: {e}")
                            logger.debug(f"Contenuto JSON estratto:\n{json_text}")
                            logger.debug(f"role_system: {role_system}")
                            logger.debug(f"role_user: {role_user}")
                    else:
                        #print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
                        #print("Contenuto della risposta:", response_text)
                        logger = setup_logger(st.session_state["user_dir"], "getEsposizione")
                        logger.debug("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
                        logger.debug(f"Contenuto della risposta:\n{response_text}")
                        logger.debug(f"role_system: {role_system}")
                        logger.debug(f"role_user: {role_user}")

                    update_esecuzione_with_subattivita(esposizione_path, fase, attivita, sub_attivita)

                else:
                    print("  Errore: 'attivita' non è un dizionario")
    else:
        print("Errore: Il contenuto del file JSON non è una lista. Tipo trovato:", type(esecuzione))


def aggiorna_esposizione(esecuzione_path, esposizione_path, docente):
    try:
        # Controlla se il file esposizione.json esiste
        if os.path.exists(esposizione_path):
            # Leggi il contenuto esistente del file esposizione.json
            with open(esposizione_path, 'r', encoding='utf-8') as esposizione_file:
                esposizione_data = json.load(esposizione_file)
                if "docente" in esposizione_data:
                    esposizione_data["docente"] = docente
        else:
            # Se il file non esiste, inizializza una nuova struttura
            esposizione_data = {
                "docente": docente,
                "fasi": []
            }

        # Leggi il contenuto del file esecuzione.json
        if os.path.exists(esecuzione_path):
            with open(esecuzione_path, 'r', encoding='utf-8') as esecuzione_file:
                esecuzione_data = json.load(esecuzione_file)
        else:
            print(f"Errore: Il file {esecuzione_path} non esiste.")
            return

        # Aggiungi i dati da esecuzione_path a esposizione_path
        if "fasi" in esecuzione_data:
            esposizione_data["fasi"].extend(esecuzione_data["fasi"])

        # Scrivi i dati aggiornati nel file esposizione.json
        with open(esposizione_path, 'w', encoding='utf-8') as esposizione_file:
            json.dump(esposizione_data, esposizione_file, ensure_ascii=False, indent=4)

        print(f"File '{esposizione_path}' aggiornato con successo.")
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing del JSON: {e}")
    except Exception as e:
        print(f"Errore generico: {e}")


def update_esecuzione_with_subattivita(esecuzione_path, fase, attivita, sub_attivita):
    """
    Aggiunge le sotto-attività generate da GPT all'attività corrispondente nel file esecuzione.json.

    Args:
        esecuzione_path (str): Percorso del file esecuzione.json.
        fase (str): Nome della fase in cui si trova l'attività.
        attivita (str): Nome dell'attività a cui aggiungere le sotto-attività.
        sub_attivita (list): Lista delle sotto-attività generate da GPT.
    """
    try:
        # Carica il file esecuzione.json
        with open(esecuzione_path, 'r', encoding='utf-8') as file:
            esecuzione = json.load(file)
    except FileNotFoundError:
        print(f"Errore: Il file {esecuzione_path} non esiste.")
        return
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing del JSON: {e}")
        return

        # Controlla se la struttura contiene le informazioni attese
    if isinstance(esecuzione, dict) and "fasi" in esecuzione:
        for fase_data in esecuzione["fasi"]:  # Itera sulla lista contenuta in "fasi"
            if fase_data['FASE'] == fase:
                for attivita_data in fase_data['lista_attivita']:
                    if attivita_data['attivita'] == attivita:
                        # Aggiungi le sotto-attività dopo la durata
                        attivita_data['sub_attivita'] = sub_attivita
                        break

        # Salva il file aggiornato
        try:
            with open(esecuzione_path, 'w', encoding='utf-8') as file:
                json.dump(esecuzione, file, ensure_ascii=False, indent=2)
            print("File esposizione.json aggiornato con successo.")
        except Exception as e:
            print(f"Errore durante il salvataggio del file: {e}")


def getMateriale(commento, client):
    progettazione_file = os.path.join(st.session_state["user_dir"], "progettazione_finale.json")

    with open(progettazione_file, 'r', encoding="utf-8") as f:
        progettazione = json.load(f)

    elenco_path = os.path.join(st.session_state["user_dir"], "materiale_prova.json")
    elenco_path1 = os.path.join(st.session_state["user_dir"], "materiale_prova1.json")

    # Controlla se il file esiste
    if os.path.exists(elenco_path):
        try:
            os.remove(elenco_path)  # Elimina il file esistente
            print(f"Il file {elenco_path} è stato eliminato.")
        except Exception as e:
            print(f"Errore durante l'eliminazione del file {elenco_path}: {e}")

    # Se la cartella esiste, cancellala e crea nuovamente la cartella

    cartella_materiali = os.path.join(st.session_state["user_dir"], "materiali")
    if os.path.exists(cartella_materiali):
        shutil.rmtree(cartella_materiali)

        # Creazione della nuova cartella
    os.makedirs(cartella_materiali)

    # Recupero dei valori
    tipo_scuola = progettazione["tipo_scuola"]
    grado = progettazione["grado"]
    indirizzo = progettazione["indirizzo"]
    articolazione = progettazione["articolazione"]
    disciplina = progettazione["disciplina"]
    docente = progettazione["docente"]
    durata = progettazione["durata"]
    Unita_didattica_apprendimento = progettazione["Unita_didattica_apprendimento"]
    contesto = progettazione["contesto"]
    titolo_lezione = progettazione["titolo_lezione"]
    anno_scolastico = progettazione["anno_scolastico"]
    data_oggi = progettazione["data_oggi"]
    numero_bes = progettazione["numero_bes"]
    pr=""
    # Definizione dei dati
    dati = {
        "ordinamento scuola": "Scuola secondaria di II grado",
        "tipo_scuola": tipo_scuola,
        "grado": grado,
        "indirizzo": indirizzo,
        "articolazione": articolazione,
        "disciplina": disciplina,
        "docente": docente,
        "durata": durata,
        "uda": Unita_didattica_apprendimento,
        "titolo_lezione": titolo_lezione,
        "anno_scolastico": anno_scolastico,
        "data_oggi": data_oggi,
        "numero_bes": numero_bes,
        "scritta": []  # Lista vuota, da riempire se necessario
    }
    dati1 = {
        "ordinamento scuola": "Scuola secondaria di II grado",
        "tipo_scuola": tipo_scuola,
        "grado": grado,
        "indirizzo": indirizzo,
        "articolazione": articolazione,
        "disciplina": disciplina,
        "docente": docente,
        "durata": durata,
        "uda": Unita_didattica_apprendimento,
        "titolo_lezione": titolo_lezione,
        "anno_scolastico": anno_scolastico,
        "data_oggi": data_oggi,
        "numero_bes": numero_bes,
        "diario": []  # Lista vuota, da riempire se necessario
    }
    dati2 = {
        "ordinamento scuola": "Scuola secondaria di II grado",
        "tipo_scuola": tipo_scuola,
        "grado": grado,
        "indirizzo": indirizzo,
        "articolazione": articolazione,
        "disciplina": disciplina,
        "docente": docente,
        "durata": durata,
        "uda": Unita_didattica_apprendimento,
        "titolo_lezione": titolo_lezione,
        "anno_scolastico": anno_scolastico,
        "data_oggi": data_oggi,
        "numero_bes": numero_bes,
        "orale": []  # Lista vuota, da riempire se necessario
    }
    dati3 = {
        "ordinamento scuola": "Scuola secondaria di II grado",
        "tipo_scuola": tipo_scuola,
        "grado": grado,
        "indirizzo": indirizzo,
        "articolazione": articolazione,
        "disciplina": disciplina,
        "docente": docente,
        "durata": durata,
        "uda": Unita_didattica_apprendimento,
        "titolo_lezione": titolo_lezione,
        "anno_scolastico": anno_scolastico,
        "data_oggi": data_oggi,
        "numero_bes": numero_bes,
        "prerequisiti_orale": []  # Lista vuota, da riempire se necessario
    }

    diario = os.path.join(cartella_materiali, "autovalutazione.json")

    # Scrittura del file JSON

    with open(diario, "w", encoding="utf-8") as file:
        json.dump(dati1, file, ensure_ascii=False, indent=2)

    user_dir = st.session_state["user_dir"]
    esposizione_path = os.path.join(user_dir, "esposizione.json")
    progettazione_path = os.path.join(user_dir, "progettazione.json")

    try:
        with open(esposizione_path, 'r', encoding='utf-8') as file:
            esposizione = json.load(file)  # Carica il JSON come struttura Python (lista o dizionario)
    except FileNotFoundError:
        print(f"Errore: Il file {esposizione_path} non esiste.")
        esposizione = None
    except json.JSONDecodeError as e:
        print(f"Errore nel parsing del JSON: {e}")
        esposizione = None

    # Sovrascrivi il file JSON con i dati aggiornati
    # Verifica che esecuzione sia una lista
    if isinstance(esposizione, dict):
        fasi = esposizione.get("fasi", [])

        for fase_inst in fasi:
          if (fase_inst['FASE'] == "Verifica degli obiettivi") or (fase_inst['FASE'] == "Verifica dei prerequisiti"):
            for attivita_inst in fase_inst.get('lista_attivita',
                                               []):  # Usa get per evitare errori se 'lista_attivita' non esiste
                if isinstance(attivita_inst, dict):
                    metodologia = attivita_inst['metodologia']
                    attivita = attivita_inst['attivita']
                    print(f"  Metodologia: {metodologia}")
                    for matt_didatt in attivita_inst.get('materiali_didattici',
                                                       []):
                        my_material = fase_inst.get('FASE')+"_"+attivita+"_"+matt_didatt['materiale_didattico']
                        print(st.session_state.selected_materials)
                        if my_material in st.session_state.selected_materials:
                            print('my_material:', my_material)
                            if bool(re.search(r'scritt', metodologia, re.IGNORECASE)):
                                if fase_inst['FASE'] == "Verifica degli obiettivi":
                                    scritta = os.path.join(cartella_materiali, "verifica_scritta.json")
                                    with open(scritta, "w", encoding="utf-8") as file_scritta:
                                        json.dump(dati, file_scritta, ensure_ascii=False, indent=2)
                                    with open("formato_output_verifica", "r", encoding="utf-8") as file1:
                                        formato_output_verifica = file1.read()
                                    file_lezione = os.path.join(cartella_materiali, "verifica_scritta.json")
                                    quale_file = "scritto"
                                else:
                                    scritta = os.path.join(cartella_materiali, "prerequisiti_scritto.json")
                                    with open(scritta, "w", encoding="utf-8") as file_scritta:
                                        json.dump(dati, file_scritta, ensure_ascii=False, indent=2)
                                    with open("formato_output_verifica", "r", encoding="utf-8") as file1:
                                        formato_output_verifica = file1.read()
                                    file_lezione = os.path.join(cartella_materiali, "prerequisiti_scritto.json")
                                    quale_file = "prerequisiti_scritto"
                                    # Carica il file JSON
                                    with open(progettazione_path, "r", encoding="utf-8") as file4:
                                        dataPr = json.load(file4)

                                    # Estrai i prerequisiti
                                    lista_prerequisiti = [item["pr"] for item in dataPr["prerequisiti"]["prerequisito"]]
                                    pr = ". Considera i seguenti prerequisiti per la verifica dei prerequisiti: " + ", ".join(lista_prerequisiti)
                            elif bool(re.search(r'oral', metodologia, re.IGNORECASE)):
                                if fase_inst['FASE'] == "Verifica degli obiettivi":
                                    orale = os.path.join(cartella_materiali, "verifica_orale.json")
                                    with open(orale, "w", encoding="utf-8") as file_orale:
                                        json.dump(dati2, file_orale, ensure_ascii=False, indent=2)
                                    with open("formato_output_orale", "r", encoding="utf-8") as file2:
                                        formato_output_verifica = file2.read()
                                    file_lezione = os.path.join(cartella_materiali, "verifica_orale.json")
                                    quale_file = "orale"
                                else:
                                    orale = os.path.join(cartella_materiali, "prerequisiti_orale.json")
                                    with open(orale, "w", encoding="utf-8") as file_orale:
                                        json.dump(dati3, file_orale, ensure_ascii=False, indent=2)
                                    with open("formato_output_prerequisiti", "r", encoding="utf-8") as file3:
                                        formato_output_verifica = file3.read()
                                    file_lezione = os.path.join(cartella_materiali, "prerequisiti_orale.json")
                                    quale_file = "prerequisiti_orale"
                                    with open(progettazione_path, "r", encoding="utf-8") as file4:
                                        dataPr = json.load(file4)
                                    # Estrai i prerequisiti
                                    lista_prerequisiti = [item["pr"] for item in dataPr["prerequisiti"]["prerequisito"]]
                                    pr = ". Considera i seguenti prerequisiti per la verifica dei prerequisiti: " + ", ".join(lista_prerequisiti)
                            role_system = (
                              f"Agisci da esperto docente di informatica nelle scuole secondarie di secondo grado. Stai progettando una lezione per la tua classe. Dovrai fornire il contenuto del materiale didattico tramite un JSON strutturato come segue: {formato_output_verifica}."
                            )
                            role_user = (
                                f"Il tuo task è fornire i materiali didattici a corredo alla lezione per l'attività che ti fornirò. Considera il contenuto della seguente attività: {attivita_inst}. Considera il materiale didattico: {matt_didatt}. Considera la seguente progettazione: {progettazione} {pr} **Importante:** Considera il seguente commento per fornire meglio la tua risposta se presente: {commento}. Rispondi solo con il JSON e niente altro."
                                f"MATERIALE DIDATTICO: "
                            )
                            completion = client.chat.completions.create(
                                model="gpt-4o",
                                temperature=0.7,
                                messages=[
                                    {"role": "system", "content": role_system},
                                    {"role": "user", "content": role_user}
                                ],
                            )
                            response_text = completion.choices[0].message.content

                            # Pulire la risposta per trovare solo il JSON
                            json_start = response_text.find('[')
                            json_end = response_text.rfind(']') + 1
                            if json_start != -1 and json_end != -1:
                                json_text = response_text[json_start:json_end]

                                try:
                                    response_data = json.loads(json_text)
                                    elenco_path = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

                                    # Salvare il file aggiornato
                                    with open(elenco_path, 'w', encoding='utf-8') as json_file:
                                        json.dump(response_data, json_file, ensure_ascii=False, indent=2)

                                    print(f"La risposta è stata salvata in {elenco_path}")
                                except json.JSONDecodeError as e:
                                    #print("Errore nel decodificare il JSON:", e)
                                    #print("Contenuto JSON estratto:", json_text)
                                    logger = setup_logger(st.session_state["user_dir"], "getMateriale")
                                    logger.debug(f"Errore nel decodificare il JSON: {e}")
                                    logger.debug(f"Contenuto JSON estratto:\n{json_text}")
                                    logger.debug(f"role_system: {role_system}")
                                    logger.debug(f"role_user: {role_user}")
                            else:
                                    #print("Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
                                    #print("Contenuto della risposta:", response_text)
                                    logger = setup_logger(st.session_state["user_dir"], "getMateriale")
                                    logger.debug(
                                        "Errore: non è stato possibile individuare un blocco JSON valido nella risposta.")
                                    logger.debug(f"Contenuto della risposta:\n{response_text}")
                                    logger.debug(f"role_system: {role_system}")
                                    logger.debug(f"role_user: {role_user}")
                            file_materiali = os.path.join(st.session_state["user_dir"], "materiale_prova.json")
                            # Caricamento dei dati esistenti in lezione.json
                            with open(file_lezione, "r", encoding="utf-8") as file:
                                dati_lezione = json.load(file)

                            # Caricamento dei materiali didattici da materiali_prova.json
                            with open(file_materiali, "r", encoding="utf-8") as file:
                                materiali_didattici = json.load(file)

                            if quale_file == "scritto":
                               dati_lezione["scritta"] = materiali_didattici

                            if quale_file == "orale":
                               dati_lezione["orale"] = materiali_didattici

                            if quale_file == "prerequisiti_scritto":
                                dati_lezione["scritta"] = materiali_didattici

                            if quale_file == "prerequisiti_orale":
                                dati_lezione["prerequisiti_orale"] = materiali_didattici

                            # Salvataggio del file aggiornato
                            with open(file_lezione, "w", encoding="utf-8") as file:
                                json.dump(dati_lezione, file, ensure_ascii=False, indent=2)

                else:
                    print("non hai selezionato il materiale da generare")
    else:
        print("Errore: Il contenuto del file JSON non è una lista. Tipo trovato:", type(esposizione))

    if st.session_state.cp:
        file_sorgente = "diarioCp.json"
        if os.path.exists(file_sorgente):
            with open(diario, "r", encoding="utf-8") as file:
                dati_lezione = json.load(file)
                print(dati_lezione)
            with open(file_sorgente, "r", encoding="utf-8") as file1:
                materiali_didattici = json.load(file1)
                print(materiali_didattici)
            # Aggiornamento del file lezione.json con i nuovi materiali
            dati_lezione["diario"] = materiali_didattici
            with open(diario, "w", encoding="utf-8") as file2:
                json.dump(dati_lezione, file2, ensure_ascii=False, indent=2)
        else:
            st.error("Errore: Il file sorgente non esiste.")
    elif any(attivita.get("di_gruppo", False) for attivita in esposizione.get("lista_attivita", [])):
        file_sorgente = "diarioGrp.json"  # Modifica con il percorso reale
        if os.path.exists(file_sorgente):
            with open(diario, "r", encoding="utf-8") as file:
                dati_lezione = json.load(file)
                print(dati_lezione)
            with open(file_sorgente, "r", encoding="utf-8") as file1:
                materiali_didattici = json.load(file1)
                print(materiali_didattici)
            # Aggiornamento del file lezione.json con i nuovi materiali
            dati_lezione["diario"] = materiali_didattici
            with open(diario, "w", encoding="utf-8") as file2:
                json.dump(dati_lezione, file2, ensure_ascii=False, indent=2)
        else:
            st.error("Errore: Il file sorgente non esiste.")
    else:
        file_sorgente = "diarioInd.json"  # Modifica con il percorso reale
        if os.path.exists(file_sorgente):
            with open(diario, "r", encoding="utf-8") as file:
                dati_lezione = json.load(file)
                print(dati_lezione)
            with open(file_sorgente, "r", encoding="utf-8") as file1:
                materiali_didattici = json.load(file1)
                print(materiali_didattici)
            # Aggiornamento del file lezione.json con i nuovi materiali
            dati_lezione["diario"] = materiali_didattici
            with open(diario, "w", encoding="utf-8") as file2:
                json.dump(dati_lezione, file2, ensure_ascii=False, indent=2)
        else:
            st.error("Errore: Il file sorgente non esiste.")


def genera_riepilogo_attivita():
    esposizione_file = os.path.join(st.session_state["user_dir"], "esposizione.json")
    # Carica il file JSON principale
    with open(esposizione_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Lista per le attività trasformate
    lista_attivita = []

    riepilogo_file = os.path.join(st.session_state["user_dir"], "riepilogo.json")

    for fase in data["fasi"]:
        for attivita in fase["lista_attivita"]:
            lista_attivita.append({"attivita": f"{attivita['attivita']} /{attivita['durata']} /{attivita['setting']} ({attivita['adattamento_BES']})"})

    # Creazione del nuovo JSON
    nuovo_json = {"lista_attivita": lista_attivita}

    # Salva il nuovo file JSON
    with open(riepilogo_file, 'w', encoding='utf-8') as f:
        json.dump(nuovo_json, f, ensure_ascii=False, indent=2)

def compile_progettazione_didattica():
    destinazione = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    os.makedirs(destinazione, exist_ok=True)
    json_file = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
    try:
        with open(json_file, 'r', encoding='utf-8') as f_json:
            json_data = json.load(f_json)  # Correctly load JSON data from file
            print(json_data)
    except FileNotFoundError:
        print(f"Error: File {json_file} not found.")
        exit(1)  # Exit if the JSON file cannot be found
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {json_file}: {e}")
        exit(1)  # Exit if there's a JSON parsing error
    replace_placeholder_in_paragraph('LayoutProgettazioneDidattica.docx', json_data,
                                     os.path.join(destinazione, "progettazione_didattica.docx"))


def compileFile():
    genera_riepilogo_attivita()

    folder_path = os.path.join(st.session_state["user_dir"], "materiali")
    folder_output = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    # Scorri tutti i file nella cartella
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Controlla se è un file (e non una cartella)
        if os.path.isfile(file_path):
            name, extension = os.path.splitext(filename)
            if extension == '.json':
                print(f'Nome del file senza estensione: {name}')
            try:
                with open(file_path, 'r', encoding="utf-8") as f_json:
                    json_data = json.load(f_json)  # Correctly load JSON data from file
            except FileNotFoundError:
                print(f"Error: File {file_path} not found.")
                exit(1)  # Exit if the JSON file cannot be found
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {file_path}: {e}")
                exit(1)  # Exit if there's a JSON parsing error
            output_file = os.path.join(folder_output, f'{name}.docx')
            replace_placeholders("LayoutMateriale.docx", json_data, output_file)

    formattingData = Utility.loadJsonData('formatting.json')


    Utility.replaceTag('LayoutLezioneSimulata.pptx', Utility.loadJsonData(os.path.join(st.session_state["user_dir"], "progettazione_finale.json")), formattingData, os.path.join(folder_output, "lezioneSimulata.pptx"))
    Utility_last.replaceTag('LayoutPrerequisiti.pptx', Utility.loadJsonData(os.path.join(st.session_state["user_dir"], "esposizione.json")), formattingData, os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx"))
    insert_slides_at_tag(os.path.join(folder_output, "lezioneSimulata.pptx"),
                         os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx"),
                         os.path.join(folder_output, "lezioneSimulata.pptx"),
                         "{{{verificaPrerequisiti.pptx}}}")
    Utility_last.replaceTag('LayoutNucleoCentrale.pptx', Utility.loadJsonData(os.path.join(st.session_state["user_dir"], "esposizione.json")), formattingData, os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx"))
    insert_slides_at_tag(os.path.join(folder_output, "lezioneSimulata.pptx"),
                         os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx"),
                         os.path.join(folder_output, "lezioneSimulata.pptx"),
                         "{{{nucleoCentrale.pptx}}}")
    if st.session_state.progettazione.get('cp') is None:
        remove_slide_with_tag(os.path.join(folder_output, "lezioneSimulata.pptx"), os.path.join(folder_output, "lezioneSimulata.pptx"), "{{{compitoProdotto.pptx}}}")
    else:
        Utility.replaceTag("LayoutCompitoProdotto.pptx",
                           Utility.loadJsonData(os.path.join(st.session_state["user_dir"], "progettazione_finale.json")),
                           formattingData,
                           os.path.join(st.session_state["user_dir"], "compitoProdotto.pptx"))
        insert_slides_at_tag(os.path.join(folder_output, "lezioneSimulata.pptx"),
                             os.path.join(st.session_state["user_dir"], "compitoProdotto.pptx"),
                             os.path.join(folder_output, "lezioneSimulata.pptx"),
                             "{{{compitoProdotto.pptx}}}")

    Utility.replaceTag("LayoutAttivita.pptx",
                       Utility.loadJsonData(os.path.join(st.session_state["user_dir"], "riepilogo.json")),
                       formattingData,
                       os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx"))
    insert_slides_at_tag(os.path.join(folder_output, "lezioneSimulata.pptx"),
                         os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx"),
                         os.path.join(folder_output, "lezioneSimulata.pptx"),
                         "{{{riepilogoAttivita.pptx}}}")
    clenup_lezioneSimulata(folder_output)




