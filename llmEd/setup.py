import os
import shutil
from xml.dom.minidom import Document

import streamlit as st
from pptx import Presentation
from docx import Document
import config
import json
import uuid

def on_submit_button3():

    progettazione = os.path.join(st.session_state["user_dir"], "progettazione.json")
    esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")

    if os.path.exists(progettazione):
        os.remove(progettazione)

    if os.path.exists(esecuzione):
        os.remove(esecuzione)

    if os.path.exists(esposizione):
        os.remove(esposizione)

    if os.path.exists(materiali):
        os.remove(materiali)

def create_unique_user_directory(nome, cognome):

    base_name = f"{nome.lower()}.{cognome.lower()}"
    user_dir = os.path.join(config.BASE_DIR, base_name)

    # Controlla se una cartella già esiste con questo nome
    if os.path.exists(user_dir):
        # Aggiungi un identificatore unico se esiste già
        unique_id = str(uuid.uuid4())[:8]  # Genera un identificatore breve
        user_dir = os.path.join(config.BASE_DIR, f"{base_name}_{unique_id}")

    os.makedirs(user_dir, exist_ok=True)
    return user_dir


def track_execution_time(materiale, start_time, end_time):
    # Crea o accedi al file di log dell'utente
    user_dir = st.session_state["user_dir"]
    log_file = os.path.join(user_dir, "execution_times.csv")

    # Calcola il tempo di esecuzione
    execution_time = end_time - start_time

    # Se il file non esiste, crea il file con le intestazioni
    if not os.path.exists(log_file):
        with open(log_file, "w") as file:
            file.write("Materiale,Tempo (secondi)\n")

    # Aggiungi il dato del tempo di esecuzione al file CSV
    with open(log_file, "a") as file:
        file.write(f"{materiale},{execution_time}\n")

def unable():
    del st.session_state["user_dir"]
    del st.session_state["docN"]
    del st.session_state["docC"]
    st.session_state["tipoS"] = None
    st.session_state["adr"] = None
    del st.session_state["ctx"]
    del st.session_state["ore_anno"]
    del st.session_state["oreSett"]
    st.session_state.uda_options = []
    st.session_state.materiale_options = []
    st.session_state.lezione_options = []
    st.session_state.disabled = False
    st.session_state.disabledScuola = False
    st.session_state.disabledCognome = False
    st.session_state.disabledL = True
    st.session_state.disabledLs = True
    st.session_state.disabledUDA = True
    st.session_state.disablednewPDD = True

# Disable the submit button after it is clicked
def salva_dati(tipo_scuola, indirizzo, linee_guida, grado, contesto, nome, cognome, disciplina, articolazione, ore_set, ore_anno, warn, succ):
        if tipo_scuola is None or indirizzo is None or grado is None or contesto is None or contesto == "" or nome is None or nome == ""\
                or cognome is None or cognome == "" or ore_set == 0 or ore_anno ==0 or disciplina is None or articolazione is None:
            #print("Tipo scuola:")
            #print(tipo_scuola)
            #print("Indirizzo:")
            #print(indirizzo)
            #print("Grado:")
            #print(grado)
            #print("Contesto:")
            #print(contesto)
            #print("Nome:")
            #print(nome)
            #print("Cognome:")
            #print(cognome)
            #print("Ore sett:")
            #print(ore_set)
            #print("Ore anno:")
            #print(ore_anno)
            #print("Discplina:")
            #print(disciplina)
            #print("Articolazione:")
            #print(articolazione)
            return True
        else:
            st.session_state.disabledUDA = False
            st.session_state.disabledL = True
            st.session_state.disabledLs = True
            elencoUda = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
            dettaglioUda = os.path.join(st.session_state["user_dir"], "dettaglioUDA.json")
            elencoLezioni = os.path.join(st.session_state["user_dir"], "elencoLezioni.json")
            progettazioneDidattica = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
            if os.path.exists(elencoUda):
                os.remove(elencoUda)
            if os.path.exists(dettaglioUda):
                os.remove(dettaglioUda)
            if os.path.exists(elencoLezioni):
                os.remove(elencoLezioni)
            if os.path.exists(progettazioneDidattica):
                os.remove(progettazioneDidattica)
            progettazione = os.path.join(st.session_state["user_dir"], "progettazione.json")
            esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
            esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
            riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
            materiali = os.path.join(st.session_state["user_dir"], "materiali.json")
            prova = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

            if os.path.exists(progettazione):
                os.remove(progettazione)

            if os.path.exists(esecuzione):
                os.remove(esecuzione)

            if os.path.exists(esposizione):
                os.remove(esposizione)

            if os.path.exists(materiali):
                os.remove(materiali)

            if os.path.exists(riepilogo):
                os.remove(riepilogo)

            if os.path.exists(prova):
                os.remove(prova)

            simulata = os.path.join(st.session_state["user_dir"], "lezioneSimulata.pptx")
            nucleo = os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx")
            attivita = os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx")
            prerequisiti = os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx")
            if os.path.exists(simulata):
                os.remove(simulata)

            if os.path.exists(nucleo):
                os.remove(nucleo)

            if os.path.exists(attivita):
                os.remove(attivita)

            if os.path.exists(prerequisiti):
                os.remove(prerequisiti)
            materiale_didattico = os.path.join(st.session_state["user_dir"], "materiale_didattico")
            materiale_dir = os.path.join(st.session_state["user_dir"], "materiali")
            materiale_didattico_zip = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo.zip")
            if os.path.exists(materiale_didattico):
                shutil.rmtree(materiale_didattico)

            if os.path.exists(materiale_dir):
                shutil.rmtree(materiale_dir)

            if os.path.exists(materiale_didattico_zip):
                os.remove(materiale_didattico_zip)
            if "user_dir" not in st.session_state or not st.session_state["user_dir"]:
                st.session_state["user_dir"] = create_unique_user_directory(nome, cognome)

            succ.success('I tuoi dati sono stati salvati con successo!', icon="✅")

        return False

def delete_pdd_info():
    progettazione = os.path.join(st.session_state["user_dir"], "progettazione.json")
    esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
    riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")

    if os.path.exists(progettazione):
        os.remove(progettazione)

    if os.path.exists(esecuzione):
        os.remove(esecuzione)

    if os.path.exists(esposizione):
        os.remove(esposizione)

    if os.path.exists(materiali):
        os.remove(materiali)

    if os.path.exists(riepilogo):
        os.remove(riepilogo)
    elenco_uda = os.path.join(st.session_state["user_dir"], "elencoUDA.json")
    dettaglio_uda = os.path.join(st.session_state["user_dir"], "dettaglioUDA.json")
    elenco_lezioni = os.path.join(st.session_state["user_dir"], "elencoLezioni.json")
    progettazione_didattica = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
    if os.path.exists(elenco_uda):
        os.remove(elenco_uda)
    if os.path.exists(dettaglio_uda):
        os.remove(dettaglio_uda)
    if os.path.exists(elenco_lezioni):
        os.remove(elenco_lezioni)
    if os.path.exists(progettazione_didattica):
        os.remove(progettazione_didattica)
    progettazione = os.path.join(st.session_state["user_dir"], "progettazione.json")
    esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
    riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")
    prova = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

    if os.path.exists(progettazione):
        os.remove(progettazione)

    if os.path.exists(esecuzione):
        os.remove(esecuzione)

    if os.path.exists(esposizione):
        os.remove(esposizione)

    if os.path.exists(materiali):
        os.remove(materiali)

    if os.path.exists(riepilogo):
        os.remove(riepilogo)

    if os.path.exists(prova):
        os.remove(prova)

    simulata = os.path.join(st.session_state["user_dir"], "lezioneSimulata.pptx")
    nucleo = os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx")
    attivita = os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx")
    prerequisiti = os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx")
    if os.path.exists(simulata):
        os.remove(simulata)

    if os.path.exists(nucleo):
        os.remove(nucleo)

    if os.path.exists(attivita):
        os.remove(attivita)

    if os.path.exists(prerequisiti):
        os.remove(prerequisiti)
    materiale_didattico = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    materiale_dir = os.path.join(st.session_state["user_dir"], "materiali")
    materiale_didattico_zip = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo.zip")
    if os.path.exists(materiale_didattico):
        shutil.rmtree(materiale_didattico)

    if os.path.exists(materiale_dir):
        shutil.rmtree(materiale_dir)

    if os.path.exists(materiale_didattico_zip):
        os.remove(materiale_didattico_zip)


def delete_lezioni_info():
    progettazione = os.path.join(st.session_state["user_dir"], "progettazione.json")
    esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
    riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")
    elenco_lezioni = os.path.join(st.session_state["user_dir"], "elencoLezioni.json")

    if os.path.exists(progettazione):
        os.remove(progettazione)

    if os.path.exists(esecuzione):
        os.remove(esecuzione)

    if os.path.exists(esposizione):
        os.remove(esposizione)

    if os.path.exists(materiali):
        os.remove(materiali)

    if os.path.exists(riepilogo):
        os.remove(riepilogo)

    if os.path.exists(elenco_lezioni):
        os.remove(elenco_lezioni)

    prova = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

    if os.path.exists(prova):
        os.remove(prova)

    simulata = os.path.join(st.session_state["user_dir"], "lezioneSimulata.pptx")
    nucleo = os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx")
    attivita = os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx")
    prerequisiti = os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx")
    if os.path.exists(simulata):
        os.remove(simulata)

    if os.path.exists(nucleo):
        os.remove(nucleo)

    if os.path.exists(attivita):
        os.remove(attivita)

    if os.path.exists(prerequisiti):
        os.remove(prerequisiti)

    materiale_didattico = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    materiale_dir = os.path.join(st.session_state["user_dir"], "materiali")
    materiale_didattico_zip = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo.zip")
    if os.path.exists(materiale_didattico):
        shutil.rmtree(materiale_didattico)

    if os.path.exists(materiale_dir):
        shutil.rmtree(materiale_dir)

    if os.path.exists(materiale_didattico_zip):
        os.remove(materiale_didattico_zip)

def delete_progettazione_info():
    progettazione = os.path.join(st.session_state["user_dir"], "progettazione.json")
    esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
    riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")

    if os.path.exists(progettazione):
        os.remove(progettazione)

    if os.path.exists(esecuzione):
        os.remove(esecuzione)

    if os.path.exists(esposizione):
        os.remove(esposizione)

    if os.path.exists(materiali):
        os.remove(materiali)

    if os.path.exists(riepilogo):
        os.remove(riepilogo)

    prova = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

    if os.path.exists(prova):
        os.remove(prova)

    simulata = os.path.join(st.session_state["user_dir"], "lezioneSimulata.pptx")
    nucleo = os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx")
    attivita = os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx")
    prerequisiti = os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx")
    if os.path.exists(simulata):
        os.remove(simulata)

    if os.path.exists(nucleo):
        os.remove(nucleo)

    if os.path.exists(attivita):
        os.remove(attivita)

    if os.path.exists(prerequisiti):
        os.remove(prerequisiti)

    materiale_didattico = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    materiale_dir = os.path.join(st.session_state["user_dir"], "materiali")
    materiale_didattico_zip = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo.zip")
    if os.path.exists(materiale_didattico):
        shutil.rmtree(materiale_didattico)

    if os.path.exists(materiale_dir):
        shutil.rmtree(materiale_dir)

    if os.path.exists(materiale_didattico_zip):
        os.remove(materiale_didattico_zip)


def delete_esposizione_info():

    esecuzione = os.path.join(st.session_state["user_dir"], "esecuzione.json")
    esposizione = os.path.join(st.session_state["user_dir"], "esposizione.json")
    riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")

    if os.path.exists(esecuzione):
        os.remove(esecuzione)

    if os.path.exists(esposizione):
        os.remove(esposizione)

    if os.path.exists(materiali):
        os.remove(materiali)

    if os.path.exists(riepilogo):
        os.remove(riepilogo)

    prova = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

    if os.path.exists(prova):
        os.remove(prova)

    simulata = os.path.join(st.session_state["user_dir"], "lezioneSimulata.pptx")
    nucleo = os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx")
    attivita = os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx")
    prerequisiti = os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx")
    if os.path.exists(simulata):
        os.remove(simulata)

    if os.path.exists(nucleo):
        os.remove(nucleo)

    if os.path.exists(attivita):
        os.remove(attivita)

    if os.path.exists(prerequisiti):
        os.remove(prerequisiti)

    materiale_didattico = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    materiale_dir = os.path.join(st.session_state["user_dir"], "materiali")
    materiale_didattico_zip = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo.zip")
    if os.path.exists(materiale_didattico):
        shutil.rmtree(materiale_didattico)

    if os.path.exists(materiale_dir):
        shutil.rmtree(materiale_dir)

    if os.path.exists(materiale_didattico_zip):
        os.remove(materiale_didattico_zip)


def delete_materiale_info():

    riepilogo = os.path.join(st.session_state["user_dir"], "riepilogo.json")
    materiali = os.path.join(st.session_state["user_dir"], "materiali.json")

    if os.path.exists(materiali):
        os.remove(materiali)

    if os.path.exists(riepilogo):
        os.remove(riepilogo)

    prova = os.path.join(st.session_state["user_dir"], "materiale_prova.json")

    if os.path.exists(prova):
        os.remove(prova)

    simulata = os.path.join(st.session_state["user_dir"], "lezioneSimulata.pptx")
    nucleo = os.path.join(st.session_state["user_dir"], "nucleoCentrale.pptx")
    attivita = os.path.join(st.session_state["user_dir"], "riepilogoAttivita.pptx")
    prerequisiti = os.path.join(st.session_state["user_dir"], "verificaPrerequisiti.pptx")
    if os.path.exists(simulata):
        os.remove(simulata)

    if os.path.exists(nucleo):
        os.remove(nucleo)

    if os.path.exists(attivita):
        os.remove(attivita)

    if os.path.exists(prerequisiti):
        os.remove(prerequisiti)

    materiale_didattico = os.path.join(st.session_state["user_dir"], "materiale_didattico")
    materiale_dir = os.path.join(st.session_state["user_dir"], "materiali")
    materiale_didattico_zip = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo.zip")
    if os.path.exists(materiale_didattico):
        shutil.rmtree(materiale_didattico)

    if os.path.exists(materiale_dir):
        shutil.rmtree(materiale_dir)

    if os.path.exists(materiale_didattico_zip):
        os.remove(materiale_didattico_zip)


def disable():
    st.session_state.disabledUDA = True

def callbackSalva():
    st.session_state.disabledScuola = True
    st.session_state.disabled = True

def enable():
    st.session_state.disabledUDA = False

# Funzione per caricare il contenuto di un file JSON
def carica_json(file_name, percorso):
    file_path = os.path.join(percorso, file_name)
    if os.path.exists(file_path):  # Controllo se il file esiste
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        return None  # Ritorna None se il file non esiste

def compileProgettazioneDidattica():
    for item in st.session_state.progett_didatt.get('Unita Didattiche', []):
      with st.expander(f"{item.get('UNITA DI APPRENDIMENTO', 'Dati mancanti')}"):
        #st.write(f"### Unità Didattica:{item.get('UNITA DI APPRENDIMENTO', 'Dati mancanti')}")
        st.write(f"**Fase di applicazione**: {item.get('fase_applicazione', 'Dati mancanti')}")
        st.write(f"**Utenti destinatari**: {item.get('utenti_destinatari', 'Dati mancanti')}")
        st.write(f"**Motivazioni**: {item.get('Motivazioni', 'Dati mancanti')}")
        st.write(f"**Tempi**: {item.get('Tempi', 'Dati mancanti')}")
        st.write(f"**Risorse umane**: {item.get('risorse_umane', 'Dati mancanti')}")
        st.write(f"#### Competenze Europee:")
        st.write(f"***Costruzione del sè (Imparare ad imparare/Progettare)***:")
        for costruzione in item.get('competenze_europee', {}).get('costruzione_del_se', {}).get('imparare_ad_imparare',
                                                                                                []):
            st.write(costruzione)
        for progettare in item.get('competenze_europee', {}).get('costruzione_del_se', {}).get('progettare', []):
            st.write(progettare)

        st.write(
            f"***Competenze sociali e relazione con gli altri (Comunicare/Collaborare e partecipare/Agire in modo autonomo)***:")
        for comunicare in item.get('competenze_europee', {}).get('competenze_sociali_relazione_con_altri', {}).get(
                'comunicare', []):
            st.write(comunicare)
        for collaborare in item.get('competenze_europee', {}).get('competenze_sociali_relazione_con_altri', {}).get(
                'collaborare_partecipare', []):
            st.write(collaborare)
        for agire in item.get('competenze_europee', {}).get('competenze_sociali_relazione_con_altri', {}).get(
                'agire_in_modo_autonomo', []):
            st.write(agire)

        st.write(
            f"***Rapporto con la realtà naturale e sociale (Risolvere i problemi/Individuare collegamenti e relazioni/Acquisire e interpretare le informazioni)***:")
        for problemi in item.get('competenze_europee', {}).get('rapporto_con_realta_naturale_sociale', {}).get(
                'risolvere_problemi', []):
            st.write(problemi)
        for relazioni in item.get('competenze_europee', {}).get('rapporto_con_realta_naturale_sociale', {}).get(
                'individuare_collegamenti_relazioni', []):
            st.write(relazioni)
        for acquisire in item.get('competenze_europee', {}).get('rapporto_con_realta_naturale_sociale', {}).get(
                'acquisire_interpretare_informazione', []):
            st.write(acquisire)

        st.write(f"#### Competenze professionali:")
        for professionali in item.get('competenze_professionali', []):
            st.write(professionali)

        st.write(f"#### Competenze di area:")
        for area in item.get('competenze_di_area', []):
            st.write(area)

        st.write(f"#### Abilità:")
        for abilita in item.get('abilita', []):
            st.write(abilita)

        st.write(f"#### Conoscenze:")
        for conoscenze in item.get('conoscenze', []):
            st.write(conoscenze)

        st.write(f"#### Obiettivi minimi:")
        for minimi in item.get('obiettivi_minimi', []):
            st.write(minimi)

        st.write(f"#### Prerequisiti:")
        for prerequisiti in item.get('prerequisiti', []):
            st.write(prerequisiti)

        st.write(f"#### Esperienze attivate:")
        for esperienze in item.get('esperienze_attivate', []):
            st.write(esperienze)

        st.write(f"#### Metodologie:")
        for esperienze in item.get('Metodologie', []):
            st.write(esperienze)

        st.write(f"#### Strumenti:")
        for strumenti in item.get('Strumenti', []):
            st.write(strumenti)

        st.write(f"#### Valutazioni:")
        for valutazioni in item.get('Valutazioni', []):
            st.write(valutazioni)
        st.write(f"#### Compito - Prodotto: {item.get('CP', {}).get('compito_prodotto', 'Dati mancanti')}")
        st.write(f"**Modalità**: {item.get('CP', {}).get('Modalita', 'Dati mancanti')}")
        st.write(f"**Artefatti consegnati**: {item.get('CP', {}).get('artefatti_consegnati', 'Dati mancanti')}")
        st.write(f"**Obiettivi**: {item.get('CP', {}).get('Obiettivi', 'Dati mancanti')}")
        st.write(f"**Tempi di svolgimento**: {item.get('CP', {}).get('Tempi', 'Dati mancanti')}")
        st.write(f"#### Strumenti:")
        for tools in item.get('CP', {}).get('Strumenti', []):
            st.write(tools)

        st.write(f"#### Criteri valutazione:")
        for criteri in item.get('CP', {}).get('criteri_valutazione', {}).get('Competenze', []):
            if "indicatore" in criteri:
                st.write(f"**Competenza**: {criteri.get('indicatore', 'Dati mancanti')}")
                st.write(f"Base: {criteri.get('Base', 'Dati mancanti')}")
                st.write(f"Intermedio: {criteri.get('Intermedio', 'Dati mancanti')}")
                st.write(f"Avanzato: {criteri.get('Avanzato', 'Dati mancanti')}")
        st.write(f"#### Relazione individuale:")
        for domande in item.get('CP', {}).get('relazione_individuale', {}).get('domande', []):
            st.write(domande)

def compileProgettazioneDidatticaHead():
    st.write(f"**Ordinamento scuola**: {st.session_state.progett_didatt.get('ordinamento scuola', 'Dati mancanti')}")
    st.write(f"**Tipo scuola**: {st.session_state.progett_didatt.get('tipo scuola', 'Dati mancanti')}")
    st.write(f"**Grado**: {st.session_state.progett_didatt.get('grado', 'Dati mancanti')}")
    st.write(f"**Indirizzo**: {st.session_state.progett_didatt.get('indirizzo', 'Dati mancanti')}")
    st.write(f"**Articolazione**: {st.session_state.progett_didatt.get('articolazione', 'Dati mancanti')}")
    st.write(f"**Disciplina**: {st.session_state.progett_didatt.get('disciplina', 'Dati mancanti')}")
    st.write(f"**Contesto**: {st.session_state.progett_didatt.get('contesto', 'Dati mancanti')}")
    st.write(f"**Docente**: {st.session_state.progett_didatt.get('docente', 'Dati mancanti')}")
    st.write(f"**Anno scolastico**: {st.session_state.progett_didatt.get('anno_scolastico', 'Dati mancanti')}")
    st.write(f"**Ore settimanali**: {st.session_state.progett_didatt.get('ore_settimanali', 'Dati mancanti')}")
    st.write(f"**Ore annue**: {st.session_state.progett_didatt.get('ore_annue', 'Dati mancanti')}")
    st.write(f"**BES**:")
    for bes in st.session_state.progett_didatt.get('BES', []):
        st.write(f"{bes.get('Nome', 'Dati mancanti')}")
    st.write(f"**Le fonti usati per la progettazione**:")
    st.write(f"1. INDICAZIONI NAZIONALI - LINEE GUIDA PER TUTTI GLI ORDINI E GRADI DI ISTRUZIONE disponibile al link https://www.e-santoni.org/Linee_guida/")
    st.write(
        f"2. Competenze chiave per l'applrendimento permanente. Raccomandazioni del parlamento Europeo e del Consiglio 2006, 2018 disponibile al link https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2006:394:0010:0018:it:PDF e https://www.luisatreccani.it/wp-content/uploads/2023/05/Raccomandazione-8-competenze-chiave-per-lapprendimento-permanente.pdf")



def carica_dati_progettazione_didattica(json_file):
    try:
        with open(json_file, "r", encoding="utf-8") as file:
            st.session_state.progett_didatt = json.load(file)
    except FileNotFoundError:
        st.warning("File non trovato. Usa valori predefiniti.")
    except json.JSONDecodeError:
        st.error("Errore nella lettura del file JSON.")

def compileProgettazione():
    st.write(f"**Titolo lezione**: {st.session_state.progettazione.get('titolo_lezione', 'Dati mancanti')}")
    st.write(f"**Anno Scolastico**: {st.session_state.progettazione.get('anno_scolastico', 'Dati mancanti')}")
    st.write(f"**Docente**: {st.session_state.progettazione.get('docente', 'Dati mancanti')}")
    st.write(f"**BES**:")
    # BES
    for item in st.session_state.progettazione.get('BES', {}).get('lista_bes', []):
        st.write(f"{item.get('bes', 'Dati mancanti')}")
        st.write(f"Misure dispensative: {item.get('misure_dispensative', 'Dati mancanti')}")
        st.write(f"Strumenti compensativi: {item.get('strumenti_compensativi', 'Dati mancanti')}")


    st.write("### Obiettivi Formativi")
    for obj in st.session_state.progettazione.get('obiettivi_formativi', {}).get('obiettivo', []):
        st.write(f"- {obj.get('o', 'Dati mancanti')}")

    st.write("### Abilità e Capacità")
    for abilita in st.session_state.progettazione.get('abilita_capacita', {}).get('abilita', []):
        st.write(f"- {abilita.get('a', 'Dati mancanti')}")

    st.write("### Conoscenze")
    for conoscenza in st.session_state.progettazione.get('conoscenze', {}).get('conoscenza', []):
        st.write(f"- {conoscenza.get('c', 'Dati mancanti')}")

    st.write("### Competenze di cittadinanza")
    for competenza in st.session_state.progettazione.get('cittadinanze', {}).get('competenze', []):
        st.write(f"- {competenza.get('c', 'Dati mancanti')}")

    st.write("### Prerequisiti")
    for prerequisito in st.session_state.progettazione.get('prerequisiti', {}).get('prerequisito', []):
        st.write(f"- {prerequisito.get('pr', 'Dati mancanti')}")

    st.write(
        f"**Strumenti utilizzati**: {st.session_state.progettazione.get('strumenti', {}).get('strumento', [{}])[0].get('s', 'Dati mancanti')}")

    st.write("### Metodologie")
    for metodologia in st.session_state.progettazione.get('metodologie', {}).get('metodologie', []):
        st.write(f"- {metodologia.get('m', 'Dati mancanti')}")

    st.write("### Compito prodotto")
    print("QUESTO é COMPITO PRODOTTO SE ESISTE")
    print(st.session_state.progettazione.get('cp'))
    if st.session_state.progettazione.get('cp') is None:
        st.session_state.cp = False
        st.write(f"Non è previsto")
    else:
        st.session_state.cp = True
        st.write(f"{st.session_state.progettazione.get('cp', {}).get('compito_prodotto', 'Dati mancanti')}")
        st.write(f"**Modalità**: {st.session_state.progettazione.get('cp', {}).get('modalita', 'Dati mancanti')}")
        st.write(f"**Tempi**: {st.session_state.progettazione.get('cp', {}).get('tempi', 'Dati mancanti')}")


    st.write("### Criteri di Valutazione")
    for criterio in st.session_state.progettazione.get('criteri_valutazione', {}).get('competenze_indicatori', {}).get(
            'competenza_indicatore', []):
        st.write(f"- {criterio.get('c/i', 'Dati mancanti')}")

    st.write("### Verifica")
    st.write(
        f"**Verifica orale**: {st.session_state.progettazione.get('verifica', {}).get('orali', [{}])[0].get('o', 'Dati mancanti')}")
    st.write(
        f"**Verifica scritta**: {st.session_state.progettazione.get('verifica', {}).get('scritte', [{}])[0].get('s', 'Dati mancanti')}")

def compileEsecuzione():
    st.session_state.selected_materials = []
    # Verifica che esposizione sia inizializzata e contenga la chiave 'fasi'
    if "esposizione" in st.session_state and "fasi" in st.session_state.esposizione:
        for fase in st.session_state.esposizione.get("fasi"):
            st.write(f"## Fase: {fase['FASE']}")
            if fase['FASE'] == "Verifica dei prerequisiti":
                st.markdown('<div id="indice4"></div>', unsafe_allow_html=True)
            if fase['FASE'] == "Nucleo centrale":
                st.markdown('<div id="indice5"></div>', unsafe_allow_html=True)
            if fase['FASE'] == "Verifica degli obiettivi":
                st.markdown('<div id="indice6"></div>', unsafe_allow_html=True)
            for attivita in fase.get('lista_attivita', []):
                st.write(f"#### Attività: {attivita['attivita']}")
                st.write(f"**Descrizione**: {attivita['descr_att']}")
                st.write(f"**Metodologia**: {attivita['metodologia']}")
                st.write(f"**Strumenti**: {', '.join(attivita['strumenti'])}")
                st.write(f"**Durata**: {attivita['durata']}")
                st.write(f"**Materiali didattici**:")

                for idx, mater_didatt in enumerate(attivita.get('materiali_didattici', [])):
                    materiale = mater_didatt.get('materiale_didattico')
                    md = f"{fase['FASE']}_{attivita['attivita']}_{materiale}"
                    genera_md = f"Genera materiale didattico per {attivita['attivita']}"
                    if (fase['FASE'] == "Verifica degli obiettivi") or (fase['FASE'] == "Verifica dei prerequisiti"):
                        agree = st.checkbox(f"{genera_md}", key=f"{md}", value=True)

                        if agree and md not in st.session_state.selected_materials:
                            st.session_state.selected_materials.append(md)
                            print("MATERIALE DIDATTICO AGGIUNTO ALLA SESSIONE: ")
                            print(md)
                        elif not agree and md in st.session_state.selected_materials:
                            st.session_state.selected_materials.remove(md)


                # Controlla se 'sub_attivita' è un dizionario
                for sub_attivita in attivita.get('sub_attivita', []):
                    st.write(f"##### Sottoattività: {sub_attivita.get('sub_att')}")
                    st.write(f"**Descrizione breve**: {sub_attivita.get('descr_breve')}")
                    st.write(f"**Contenuto**: {sub_attivita.get('contenuto')}")
                    st.write(f"**Modalità di erogazione**: {sub_attivita.get('esposizione')}")
                    st.write(f"**Esempio**: {sub_attivita.get('esempio')}")

# Funzione per caricare i dati dal file
def carica_dati_introduttiva(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            st.session_state.progettazione = json.load(file)
            print("entrato carica dati introduttiv")
    except FileNotFoundError:
        st.warning("File non trovato. Usa valori predefiniti.")
    except json.JSONDecodeError:
        st.error("Errore nella lettura del file JSON.")

def carica_dati_esposizione(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            st.session_state.esposizione = json.load(file)

    except FileNotFoundError:
        st.warning("File non trovato. Usa valori predefiniti.")
    except json.JSONDecodeError:
        st.error("Errore nella lettura del file JSON.")

def crea_unico_materiale():
    folder_path = os.path.join(st.session_state["user_dir"], "materiali")
    materiali = {"materiali_didattici": []}

    # Recupera tutti i file JSON nella cartella
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".json"):  # Verifica che sia un file JSON
            file_path = os.path.join(folder_path, file_name)

            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

                # Controlla se il file contiene una chiave specifica e inserisce i dati correttamente
                if "orale" in data:
                    materiali["materiali_didattici"].extend(data["orale"])
                elif "scritta" in data:
                    materiali["materiali_didattici"].extend(data["scritta"])
                elif "prerequisiti_orale" in data:
                    materiali["materiali_didattici"].extend(data["prerequisiti_orale"])
                elif "prerequisiti_scritto" in data:
                    materiali["materiali_didattici"].extend(data["prerequisiti_scritto"])


    # Salva il file unificato
    output_path = os.path.join(st.session_state["user_dir"], "materiali.json")
    with open(output_path, "w", encoding="utf-8") as out_f:
        json.dump(materiali, out_f, indent=4, ensure_ascii=False)

def compileMateriale():

    if "materiale" in st.session_state and "materiali_didattici" in st.session_state.materiale:
        #print(f"MATERIALE DIDATTICO: {st.session_state.materiale}")
        for materiale in st.session_state.materiale.get("materiali_didattici", []):

            st.write(f"## Materiale Didattico: {materiale.get('tipo_materiale')}")

            if "numero_domande" in materiale:
                st.write(f"**Numero domande:** {materiale.get('numero_domande')}")
                st.write(f"**Istruzioni**")
                for istruzioni in materiale.get('istruzioni', []):
                    st.write(f"{istruzioni['descrizione']}")
            if "descrizione" in materiale:
                st.write(f"**Descrizione materiale:** {materiale.get('descrizione')}")
            if "criteri_valutazione" in materiale:
                st.write(f"**Modalità valutazione:** {materiale['criteri_valutazione']}")
            if "obiettivo_minimo" in materiale:
                st.write(f"**Obiettivo minimo:** {materiale['obiettivo_minimo']}")
            if "domande" in materiale:
                st.write(f"#### Domande:")
                for domanda in materiale.get('domande', []):
                     st.write(f"{domanda['id']}. {domanda['domanda']}")
                     st.write(f"Criteri: {domanda['criteri']}")

            if "domande_sm_vf" in materiale:
                st.write(f"#### Domande:")
                for nodo in materiale.get('domande_sm_vf', []):
                    for domanda in nodo.get('domande', []):
                        st.write(f"{domanda['id_d']}. {domanda['domanda']}")
                        st.write(f"Opzioni: {domanda['opzioni']}")
                        st.write(f"Risposta corretta: {domanda['risposta_corretta']}")

            if "domande_a" in materiale:
                for  nodo in materiale.get('domande_a', []):
                    for domanda in nodo.get('domande', []):
                        st.write(f"{domanda['id_d']}. {domanda['domanda']}")
                        st.write(f"Criteri: {domanda['criteri']}")

def carica_dati_materiale(file_materiale_path):
    try:
        with open(file_materiale_path, "r", encoding="utf-8") as file:
            st.session_state.materiale = json.load(file)

    except FileNotFoundError:
        st.warning("File non trovato. Usa valori predefiniti.")
    except json.JSONDecodeError:
        st.error("Errore nella lettura del file JSON.")