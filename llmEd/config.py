from openai import OpenAI
import streamlit as st
from streamlit_option_menu import option_menu
import os

from pd_class import ProgettazioneDidattica

path = None

# Directly assign the API key
OPENAI_API_KEY = ''
client = OpenAI(api_key=OPENAI_API_KEY)



lezione_info = {'tipo_scuola':  ['Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Economico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico',  'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico','Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Istituti Tecnici Settore Tecnologico', 'Liceo', 'Liceo', 'Liceo', 'Liceo', 'Liceo'],
        'indirizzo': ['Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Amministrazione, finanza e marketing', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni','Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Informatica e Telecomunicazioni', 'Liceo Scientifico', 'Liceo Scientifico', 'Liceo Scientifico', 'Liceo Scientifico', 'Liceo Scientifico'],
        'articol': ['Relazioni internazionali per il Marketing', 'Relazioni internazionali per il Marketing', 'Relazioni internazionali per il Marketing', 'Relazioni internazionali per il Marketing', 'Sistemi informativi aziendali', 'Sistemi informativi aziendali', 'Sistemi informativi aziendali', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Grafica e comunicazione', 'Biennio comune', 'Biennio comune', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Scienze Applicate', 'Scienze Applicate', 'Scienze Applicate', 'Scienze Applicate', 'Scienze Applicate'],
        'materia': ['Informatica', 'Informatica', 'Tecnologie della comunicazione', 'Tecnologie della comunicazione', 'Informatica', 'Informatica', 'Informatica', 'Progettazione multimediale', 'Progettazione multimediale', 'Progettazione multimediale', 'Tecnologie informatiche', 'Scienze e tecnologie applicate', 'Sistemi e reti', 'Sistemi e reti', 'Sistemi e reti', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Gestione progetto, organizzazione di impresa',
                   'Informatica', 'Informatica', 'Informatica', 'Telecomunicazioni', 'Telecomunicazioni', 'Sistemi e reti', 'Sistemi e reti', 'Sistemi e reti', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Tecnologie e progettazione di sistemi informatici e di telecomunicazioni', 'Gestione progetto, organizzazione di inpresa',
                   'Informatica', 'Informatica', 'Telecomunicazioni', 'Telecomunicazioni', 'Telecomunicazioni', 'Informatica', 'Informatica', 'Informatica', 'Informatica', 'Informatica'],
        'grado' : ['III', 'IV', 'III', 'IV', 'III', 'IV', 'V', 'III', 'IV', 'V', 'I', 'II', 'III', 'IV', 'V', 'III', 'IV', 'V', 'V', 'III', 'IV', 'V', 'III', 'IV', 'III', 'IV', 'V', 'III', 'IV', 'V', 'V', 'III', 'IV', 'III', 'IV', 'V', 'I',  'II', 'III', 'IV', 'V']}

periodo = ""

def inizialization():
    if "docN" not in st.session_state:
        st.session_state["docN"] = ""

    if "docC" not in st.session_state:
        st.session_state["docC"] = ""

    # Inizializza la chiave se non esiste
    if "user_dir" not in st.session_state:
        st.session_state["user_dir"] = ""

    if "ctx" not in st.session_state:
        st.session_state["ctx"] = ""

    if "ore_anno" not in st.session_state:
        st.session_state["ore_anno"] = 0

    if "oreSett" not in st.session_state:
        st.session_state["oreSett"] = 0

    # Initialize disabled for form_submit_button to False
    if "disabled" not in st.session_state:
        st.session_state.disabled = False

    if "disabledCognome" not in st.session_state:
        st.session_state.disabledCognome = True

    if "disabledScuola" not in st.session_state:
        st.session_state.disabledScuola = True

    if "disabledEsposizione" not in st.session_state:
        st.session_state.disabledEsposizione = True

    if "disabledD" not in st.session_state:
        st.session_state.disabledD = False

    if "disabledUDA" not in st.session_state:
        st.session_state.disabledUDA = True

    if "task_running" not in st.session_state:
        st.session_state.task_running = False

    if "disabledLs" not in st.session_state:
        st.session_state.disabledLs = True

    if "disabledL" not in st.session_state:
        st.session_state.disabledL = True

    if "disabledC" not in st.session_state:
        st.session_state.disabledC = True

    if "disabledS" not in st.session_state:
        st.session_state.disabledS = True

    if "disabledNPDL" not in st.session_state:
        st.session_state.disabledNPDL = True

    if "disabledTemp" not in st.session_state:
        st.session_state.disabledTemp = True

    if "disabledConclusione" not in st.session_state:
        st.session_state.disabledConclusione = True

    if "disabledSimulata" not in st.session_state:
        st.session_state.disabledSimulata = True

    if "disablednewPDD" not in st.session_state:
        st.session_state["disablednewPDD"] = True

    if "disabledMD" not in st.session_state:
            st.session_state["disabledMD"] = True

    if "selected_materials" not in st.session_state:
        st.session_state.selected_materials = []

    if "disabledLS" not in st.session_state:
            st.session_state["disabledLS"] = True

    if "disableddownloadPDL" not in st.session_state:
        st.session_state.disableddownloadPDL = True

    if "disableddownloadnewPDL" not in st.session_state:
        st.session_state.disableddownloadnewPDL = True

    if "disabledPDL" not in st.session_state:
        st.session_state.disabledPDL = True

    if "disabledMateriale" not in st.session_state:
        st.session_state.disabledMateriale = True

    if "cp" not in st.session_state:
        st.session_state.cp = False

    if "ppt_bytes" not in st.session_state:
        ppt_bytes = ''
        st.session_state.ppt_bytes = ppt_bytes

    # Inizializza lo stato se non è già stato fatto
    if "uda_options" not in st.session_state:
        st.session_state.uda_options = []  # Inizialmente vuoto

    if "materiale_options" not in st.session_state:
        st.session_state.materiale_options = []

    if "lezione_options" not in st.session_state:
        st.session_state.lezione_options = []  # Inizialmente vuoto

    if "disabledZip" not in st.session_state:
        st.session_state.disabledZip = True

    # Inizializza lo stato se non è già stato fatto
    if "contenuto" not in st.session_state:
        st.session_state.contenuto = []  # Inizialmente vuoto

    # Inizializza lo stato se non è già stato fatto
    if "struttura" not in st.session_state:
        st.session_state.struttura = []  # Inizialmente vuoto

    if "progett_didatt" not in st.session_state:
        st.session_state.progett_didatt = {
            "ordinamento scuola": "",
            "tipo scuola": "",
            "grado":"",
            "indirizzo": "",
            "articolazione": "",
            "disciplina": "",
            "contesto": "",
            "docente": "",
            "anno_scolastico": "",
            "ore_settimanali": "",
            "ore_annue": "",
            "BES": [
                {"Nome": ""}
            ],
            "Unita Didattiche": [{
                "UNITA DI APPRENDIMENTO": "",
                "fase_applicazione": "",
                "utenti_destinatari": "",
                "Motivazioni": "",
                "competenze_europee": {
                    "costruzione_del_se": {
                        "imparare_ad_imparare": [],
                        "progettare": []
                    },
                    "competenze_sociali_relazione_con_altri": {
                        "comunicare": [],
                        "collaborare_partecipare": [],
                        "agire_in_modo_autonomo": []
                    },
                    "rapporto_con_realta_naturale_sociale": {
                        "risolvere_problemi": [],
                        "individuare_collegamenti_relazioni": [],
                        "acquisire_interpretare_informazione": []
                    }
                },
                "competenze_professionali": [],
                "competenze_di_area": [],
                "abilita": [],
                "conoscenze": [],
                "prerequisiti": [],
                "Tempi": "",
                "esperienze_attivate": [],
                "Metodologie": [],
                "risorse_umane": "",
                "Strumenti": [],
                "Valutazioni": [],
                "CP": {
                    "compito_prodotto": "",
                    "Modalita": "",
                    "artefatti_consegnati": "",
                    "Obiettivi": "",
                    "Tempi": "",
                    "Strumenti": [],
                    "criteri_valutazione": {
                        "Competenze": [{
                            "indicatore": "",
                            "Base": "",
                            "Intermedio": "",
                            "Avanzato": ""
                        }]
                    },
                    "relazione_individuale": {
                        "domande": []
                    }
                }
            }]}


    # Inizializza lo stato
    if "progettazione" not in st.session_state:
        st.session_state.progettazione = {
            "titolo_lezione": "",
            "anno_scolastico": "",
            "docente":"",
            "Unita_didattica_apprendimento": "",
            "contesto_classe":"",
            "BES": {
                "lista_bes": [
                    {"bes": "",
                     "misure_dispensative": "",
                     "strumenti_compensativi": ""
                     },
                    {"bes": "",
                     "misure_dispensative": "",
                     "strumenti_compensativi": ""
                     }
                ]},
            "obiettivi_formativi": {
                "obiettivo": [
                    {"o": ""},
                    {"o": ""}
                ]
            },
            "abilita_capacita": {
                "abilita": [
                    {"a": ""},
                    {"a": ""}
                ]
            },
            "conoscenze": {
                "conoscenza": [
                    {"c": ""},
                    {"c": ""}
                ]
            },
            "cittadinanze": {
                "competenze": [
                    {"c": ""},
                    {"c": ""}
                ]
            },
            "prerequisiti": {
                "prerequisito": [
                    {"pr": ""},
                    {"pr": ""}
                ]
            },
            "strumenti": {
                "strumento": [
                    {"s": ""}
                ]
            },
            "metodologie": {
                "metodologie": [
                    {"m": ""},
                    {"m": ""}
                ]
            },
            "cp": {
                "compito_prodotto": "",
                "modalita": "",
                "artefatti_consegnati": "",
                "tempi": ""
            },
            "criteri_valutazione": {
                "competenze_indicatori": {
                    "competenza_indicatore": [
                        {"c/i": ""},
                        {"c/i": "O"}
                    ]
                }
            },
            "verifica": {
                "orali": [
                    {"o": ""}
                ],
                "scritte": [
                    {"s": ""}
                ]
            }
        }
    if "esposizione" not in st.session_state:
            st.session_state.esposizione = {
                "docente":"",
                "lista_attivita":[{
                    "FASE": "",
                    "lista_attivita": [
                        {
                            "attivita": "",
                            "descr_att": "",
                            "metodologia": "",
                            "strumenti": [
                                ""
                            ],
                            "materiali_didattici":[""],
                            "durata": "",
                            "sub_attivita": [
                                {
                                    "sub_att": "",
                                    "descr_breve": "",
                                    "contenuto": "",
                                    "esposizione": ""
                                }
                            ]}
                ]}
        ]}
    if "materiale" not in st.session_state:
        st.session_state.materiale = {
            "materiali_didattici": [{
                "tipo_materiale": "",
                "numero_domande": "",
                "tipo_verifica": "",
                "struttra": "",
                "descrizione": "",
                "punti": "",
                "criteri_valutazione": "",
                "obiettivo_minimo": "",
                "domande_sm_vf": [
                    {
                        "domande": [{
                            "id_d": "",
                            "domanda": "",
                            "tipo": "",
                            "opzioni": "",
                            "risposta_corretta": ""
                        }]
                    }],
                "domande_a": [{
                    "tipo_domande": "",
                    "domande": [
                        {
                            "id_d": "",
                            "domanda": "",
                            "criteri": ""
                        }
                    ]
                }],
                "istruzioni": [
                    {"id": "",
                     "descrizione": ""}
                ]
            }
            ]}

# Directory principale dove salvare i file
BASE_DIR = "documenti"
os.makedirs(BASE_DIR, exist_ok=True)
nome = ""
cognome = ""
commentoUda = ""
commentoPdl = ""
intero = 0
commento = ""
commentoEsposizione = ""
commentoMateriale = ""



