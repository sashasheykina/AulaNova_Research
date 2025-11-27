from xml.dom.minidom import Document

import streamlit as st  # Deve essere il primo import
from pptx import Presentation
from streamlit_option_menu import option_menu

from config_log import log_action

st.set_page_config(page_title="", layout='wide')  # Prima istruzione Streamlit
import os
import shutil
import streamlit.components.v1 as components
import time
from time import sleep
import pandas as pd
from streamlit_extras.stylable_container import stylable_container
import json
import Utility
from config import lezione_info, inizialization, client, commento, commentoEsposizione, commentoUda, commentoPdl
from merge_slides import insert_slides_at_tag, clenup_lezioneSimulata
from pd_class import ProgettazioneDidattica
from setup import unable, salva_dati, disable, track_execution_time, carica_json, \
    carica_dati_introduttiva, compileProgettazione, compileEsecuzione, \
    carica_dati_esposizione, compileMateriale, carica_dati_materiale, crea_unico_materiale, \
    compileProgettazioneDidattica, carica_dati_progettazione_didattica, compileProgettazioneDidatticaHead, \
    on_submit_button3, delete_pdd_info, delete_lezioni_info, delete_progettazione_info, delete_esposizione_info, \
    delete_materiale_info, callbackSalva
from tools import aggiorna_elencoUDA, aggiorna_elencoLezioni, lineeGuida, periodoUda, elencoLezioni, elencoUDA, \
    dettaglioUDA, genera_PDD, getEsecuzione, getProgettazione, getMateriale, compileFile, \
    compile_progettazione_didattica, getEsposizione
from wordX import replace_placeholder_in_paragraph, load_json_data
from pyngrok import ngrok

ngrok.set_auth_token("")

st.markdown(
    """
<style>
    div[data-testid="stVerticalBlock"] div:has(div.fixed-header) {
        position: sticky;
        top: 2.875rem;
        background-color: white;
        z-index: 999;
    }
    .fixed-header {
        border-bottom: 1px solid black;
    }
</style>
    """,
    unsafe_allow_html=True
)
from typing import Literal

MARGINS = {
    "top": "2.875rem",
    "bottom": "0",
}

STICKY_CONTAINER_HTML = """
<style>
div[data-testid="stVerticalBlock"] div:has(div.fixed-header-{i}) {{
    position: sticky;
    {position}: {margin};
    background-color: white;
    z-index: 999;
}}
</style>
<div class='fixed-header-{i}'/>
""".strip()


def callback():
    st.session_state.disabledUDA = True


def callbackLs():
    st.session_state.disabledLs = True


def callbackL():
    st.session_state.disabledL = True


def callbackPDL():
    st.session_state.disabledPDL = True


def callbackMateriale():
    st.session_state.disabledMateriale = True


def sticky_container(
        *,
        height: int | None = None,
        border: bool | None = None,
        mode: Literal["top", "bottom"] = "top",
        margin: str | None = None,
):
    if margin is None:
        margin = MARGINS[mode]

    global count
    html_code = STICKY_CONTAINER_HTML.format(position=mode, margin=margin, i=count)
    count += 1

    container = st.container(height=height, border=border)
    container.markdown(html_code, unsafe_allow_html=True)
    return container


# Not to apply the same style to multiple containers
count = 0
inizialization()
if "container2" not in st.session_state:
    st.session_state.container2=True
st.title("Benvenuto nell'esperimento")
st.logo("volpeLogo.png", size='large', icon_image="volpeLogo.png")

# CSS personalizzato per aumentare le dimensioni e l'allineamento del logo nella sidebar
st.markdown("""
    <style>
        /* Logo nella sidebar */
        div[data-testid="stSidebarHeader"] > img {
            height: 6rem !important;  
            width: auto !important;
        }

        /* Icona della sidebar chiusa */
        div[data-testid="collapsedControl"] img {
            height: rem !important;  
            width: auto !important;
        }
    </style>
""", unsafe_allow_html=True)


# JavaScript per aggiornare l'icona quando la sidebar viene chiusa
st.markdown("""
    <script>
        function resizeIcon() {
            let icon = document.querySelector('div[data-testid="collapsedControl"] img');
            if (icon) {
                icon.style.height = "6rem";
                icon.style.width = "auto";
            }
        }
        document.addEventListener("DOMContentLoaded", resizeIcon);
        setTimeout(resizeIcon, 1000);
    </script>
""", unsafe_allow_html=True)


with st.sidebar:

    nome = st.text_input('Nome Docente', key='docN', placeholder="Nome docente...",
                         label_visibility="collapsed", disabled=st.session_state.disabled)
    if nome:
        st.session_state.disabledCognome = False
    else:
        st.session_state.disabledCognome = True

    cognome = st.text_input('Cognome Docente', key='docC', placeholder="Cognome docente...",
                            label_visibility="collapsed", disabled=st.session_state.disabledCognome)

    if cognome:
        st.session_state.disabledScuola = False
    else:
        st.session_state.disabledScuola = True
    docente = nome + " " + cognome
    df = pd.DataFrame(lezione_info)
    print("Nome docente: ")
    print(docente)
    # feature_1 filters
    items_val = df["tipo_scuola"].unique()
    tipo_scuola = st.selectbox('Seleziona tipo scuola', items_val, key="tipoS", index=None,
                               placeholder="Seleziona tipo istituto...",
                               label_visibility="collapsed", disabled=st.session_state.disabledScuola)
    # filter out data
    df = df[(df["tipo_scuola"] == tipo_scuola)]

    # feature_2 filters
    feature_2_val = df["indirizzo"].unique()
    address = st.selectbox('Seleziona indirizzo', feature_2_val, key="adr", index=None,
                           placeholder="Seleziona indirizzo...",
                           label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["indirizzo"] == address)]
    # feature_3 filters
    art = df["articol"].unique()
    articolazione = st.selectbox('Seleziona articolazione', art, index=None, placeholder="Seleziona articolazione...",
                                 label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["articol"] == articolazione)]
    print("Terzo PRINT")
    # feature_4 filters
    matt = df["materia"].unique()
    disciplina = st.selectbox('Seleziona disciplina', matt, index=None, placeholder="Seleziona disciplina...",
                              label_visibility="collapsed", disabled=st.session_state.disabled)
    # filter out data
    df = df[(df["materia"] == disciplina)]
    grade = df["grado"].unique()
    grado = st.selectbox('Seleziona grado classe', grade, disabled=st.session_state.disabled)
    df = df[(df["grado"] == grado)]

    contesto = st.text_area('Contesto classe', key='ctx', label_visibility="collapsed",
                            placeholder="Inserisci contesto classe...", disabled=st.session_state.disabled, height=250,
                            max_chars=2000)
    linee_guida, ore_a, ore_s = lineeGuida(articolazione, disciplina, grado)
    ore_anno = int(ore_a)
    ore_sett = int(ore_s)

    print("ore anno a ore set e loro somma")
    print(ore_anno)
    print(ore_sett)
    numerooo=ore_anno+ore_sett
    print(numerooo)

    col1, col2 = st.columns(
        [1, 1])
    warn = st.container()
    succ = st.container()

    with col1:
        salva_button = st.button("Salva",
                                 use_container_width=True,
                                 disabled=st.session_state.disabled, on_click=callbackSalva)
        if salva_button:
            campi_vuoti = salva_dati(tipo_scuola, address, linee_guida, grado, contesto, nome, cognome, disciplina, articolazione,
                       ore_sett, ore_anno, warn, succ)
            if campi_vuoti:
                st.session_state.disabled = False
                warn.warning('Compila tutti i campi!', icon="⚠️")
            else:
                st.rerun()



    with col2:
        st.button(
            "Resetta",
            kwargs=None,
            on_click=unable,
            use_container_width=True,
        )

    modifica_button = st.button("Modifica",
                                use_container_width=True)

    if modifica_button:
        st.session_state.disabled = False
        st.rerun()

    with warn:
        alert = warn.warning('Compila tutti i campi!', icon="⚠️")
        alert.empty()



progm_didat = ProgettazioneDidattica(
    tipo_scuola=tipo_scuola,
    indirizzo=address,
    linee_guida=linee_guida,
    grado=grado,
    contesto=contesto,
    docente=docente,
    disciplina=disciplina,
    articolazione=articolazione,
    ore_anno=ore_anno,
    ore_sett=ore_sett
)

selected = option_menu(None, ["Home", "Materiale didattico"],
                       icons=['house', "file-earmark-slides"],
                       styles={
                           "container": {"margin": "0px !important", "padding": "0!important", "align-items": "stretch",
                                         "background-color": "#fafafa"},
                           "icon": {"font-size": "15px"},
                           "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px",
                                        "--hover-color": "#eee"},
                           "nav-link-selected": {"font-size": "16px", "font-weight": "normal"}
                       },
                       menu_icon="cast", default_index=0, orientation="horizontal")
if selected == "Home":
    st.title("GENERAZIONE DELLA LEZIONE")
    st.markdown(
        "Gentile Docente, \n\nL'obiettivo di questo esperimento è valutare l'efficacia di uno strumento innovativo progettato per supportarvi nella creazione del materiale didattico per le vostre lezioni. Lo strumento è stato sviluppato per semplificare e velocizzare la produzione dei seguenti materiali: \n\nProgettazione Disciplinare per Competenze: Un documento che include l'analisi della classe, le unità di apprendimento, le competenze da sviluppare e le metodologie didattiche. \n\nSlides della Singola Lezione: Materiale visivo per la presentazione dei contenuti in classe. \n\nSuggerimenti per il Docente: Linee guida per lo svolgimento della lezione, comprensive di strumenti tecnologici per quiz, brainstorming e attività interattive. \n\nIl vostro contributo è fondamentale per valutare la qualità e l'utilità dei materiali generati dallo strumento rispetto ai metodi tradizionali. Durante l'esperimento, vi sarà chiesto di creare i materiali per una specifica lezione utilizzando sia lo strumento automatico che il metodo manuale. Successivamente, analizzeremo insieme vari aspetti qualitativi come la chiarezza, la comprensibilità e la completezza dei materiali generati, oltre alla velocità di produzione. \n\nLa partecipazione all'esperimento ci aiuterà a comprendere se e in che modo questo strumento possa facilitare il vostro lavoro e migliorare la qualità dei materiali didattici.")

if selected == "Materiale didattico":

    col3, col4 = st.columns([3, 1])
    with col3:
        with stylable_container(
                key="container1",
                css_styles="""
                    {
                    border: 1px solid #E9E9FA;
                    border-radius: 0.5rem;
                    background-color: #FAFAFD;
                    padding: calc(1em - 1px)
                }
                """
        ):
            st.markdown('<div id="container1"><h3>Progettazione didattica per disciplina</h3></div>',
                        unsafe_allow_html=True)

            col5, col6 = st.columns([1000, 1])
            with col5:
                st.text(
                    "SUGGERIMENTO: Genera la programmazione didattica annuale, revisiona il contenuto e, se necessario, utilizza l'area commenti per suggerire modifiche. Questo processo iterativo ti aiuterà a personalizzare e ottimizzare la pianificazione. Se stai già adottando un libro di testo e desideri che la progettazione didattica segua le sue unità, inserisci l’indice (o l’elenco dei capitoli) e specifica che la progettazione deve basarsi su di esse. Questo processo potrebbe impiegare fino a 5 minuti.")
                commentoUda = st.text_area("None", "", label_visibility="collapsed",
                                           placeholder="Inserisci qui il tuo commento", key="commentoUda")
            with col6:
                pass

            col7, col8 = st.columns([1000, 1])
            with col7:
                # Bottone per generare le UDA
                submit_button1 = st.button("Genera PDD", disabled=st.session_state.disabledUDA, on_click=callback)
                materiale_folder = os.path.join(st.session_state["user_dir"], "materiale_didattico")
                progettazione_file = os.path.join(materiale_folder, "progettazione_didattica.docx")
                progettazione_json = os.path.join(st.session_state["user_dir"], "progettazione_didattica.json")
            with col8:
                pass

            col9, col10 = st.columns([1000, 1])
            with col9:
                succ_pdd = st.container()
            with col10:
                pass
            if submit_button1:
                user_id = st.session_state["user_dir"]
                username = os.path.basename(user_id)
                log_action(username, "Progettazione didattica per disciplina", commentoUda)
                start_time = time.time()
                delete_pdd_info()
                elencoUDA(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.articolazione,
                          progm_didat.linee_guida, progm_didat.disciplina, progm_didat.contesto, client, commentoUda)
                aggiorna_elencoUDA()
                genera_PDD(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.articolazione,
                           progm_didat.linee_guida, progm_didat.disciplina, progm_didat.contesto, progm_didat.docente, ore_sett,
                           ore_anno, client, commentoUda)
                #print(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo, progm_didat.articolazione,
                #           progm_didat.linee_guida, progm_didat.disciplina, progm_didat.contesto, progm_didat.docente, ore_sett,
                #           ore_anno, client, commentoUda)
                compile_progettazione_didattica()
                end_time = time.time()
                track_execution_time("Progettazione didattica per disciplina", start_time, end_time)
                succ_pdd.success('La progettazione didattica è stata generata con successo!', icon="✅")
                time.sleep(5)
                st.session_state.disabledUDA = False
                st.session_state.disabledLs = False
                st.session_state.disabledL = True
                st.session_state.disabledPDL = True
                st.session_state.disabledMateriale = True
                st.session_state.disabledMD = True
                st.session_state.disabledZip = True
                st.rerun()

            if os.path.exists(progettazione_json):
                col9, col10 = st.columns([1000, 1])
                with col9:
                    st.markdown('<div id="indice1"></div>', unsafe_allow_html=True)
                    st.markdown("##### Informazioni generali")
                    st.markdown('<div id="indice2"></div>', unsafe_allow_html=True)
                    # Mostra i dati nel componente st.expander
                    with st.expander("Dettagli Progettazione Didattica"):
                        carica_dati_progettazione_didattica(progettazione_json)
                        compileProgettazioneDidatticaHead()
                    st.markdown("##### Unità Didattiche")
                    compileProgettazioneDidattica()
                with col10:
                    pass

        with stylable_container(
                key="container2",
                css_styles="""
                        {
                            border: 1px solid #E9E9FA;
                            border-radius: 0.5rem;
                            background-color: #FAFAFD;
                            padding: calc(1em - 1px)
                        }
                        """,
        ):
            formattingData = Utility.loadJsonData('formatting.json')
            st.markdown('<div id="container2"></div>', unsafe_allow_html=True)
            st.subheader("Progettazione della lezione")
            col11, col12 = st.columns([1000, 1])
            with col11:
                # Crea il selectbox prima del form, collegato a `st.session_state["uda_options"]`
                st.text(
                    "SUGGERIMENTO: Genera l'elenco delle lezioni, revisiona il contenuto e, se necessario, utilizza l'area commenti per suggerire modifiche.")

                uda = st.selectbox('Seleziona Unità Didattica', st.session_state.uda_options, key="uda")
                commentoLezione = st.text_area("None", "", label_visibility="collapsed",
                                               placeholder="Inserisci qui il tuo commento", key="commentoLezione")
                submit_button3 = st.button("Genera Elenco Lezioni", disabled=st.session_state.disabledLs, on_click=callbackLs)
                lezione = st.selectbox('Seleziona Lezione', st.session_state.lezione_options, key="less")
            with col12:
                pass

            col13, col14 = st.columns([1000, 1])
            with col13:
                succ_lesson = st.container()
            with col14:
                pass
            if submit_button3:
                user_id = st.session_state["user_dir"]
                username = os.path.basename(user_id)
                log_action(username, "Genera elenco lezioni", commentoLezione)
                start_time = time.time()
                periodo = periodoUda(uda)

                delete_lezioni_info()
                elencoLezioni(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo,
                              progm_didat.articolazione, progm_didat.linee_guida, progm_didat.disciplina, uda, periodo,
                              progm_didat.ore_anno, progm_didat.ore_sett, progm_didat.contesto, client, commentoLezione)
                aggiorna_elencoLezioni()
                end_time = time.time()
                track_execution_time("Genera elenco lezioni", start_time, end_time)
                succ_lesson.success('L\'elenco delle lezioni è stata generata con successo!', icon="✅")
                time.sleep(5)
                st.session_state.disabledPDL = True
                st.session_state.disabledMateriale = True
                st.session_state.disabledMD = True
                st.session_state.disabledZip = True
                st.session_state.disabledLs = False
                st.session_state.disabledL = False
                st.rerun()

        with stylable_container(
                key="container3",
                css_styles="""
                            {
                                border: 1px solid #E9E9FA;
                                border-radius: 0.5rem;
                                background-color: #FAFAFD;
                                padding: calc(1em - 1px)
                            }
                            """,
        ):
            st.markdown("<h4>Fase pre-attiva</h4>", unsafe_allow_html=True)
            # Percorso del file progettazione.json
            file_introduttiva_path = os.path.join(st.session_state["user_dir"], "progettazione.json")

            col15, col16 = st.columns([1000, 1])
            with col15:
                st.text(
                    "SUGGERIMENTO: Genera la progettazione della lezione, esamina il contenuto e, se necessario, utilizza l'area commenti per proporre modifiche. Questo ti permetterà di adattare la lezione alle tue esigenze didattiche. Questo processo potrebbe impiegare fino 1 minuto.")

                commentoPdl = st.text_area("None", "", label_visibility="collapsed",
                                           placeholder="Inserisci qui il tuo commento, se vuoi modificare la progettazione",
                                           key="commentoPdl")
                submit_button4 = st.button("Genera Progettazione Lezione", disabled=st.session_state.disabledL, on_click=callbackL)

            with col16:
                pass

            col17, col18 = st.columns([1000, 1])
            with col17:
                succ_pl = st.container()
            with col18:
                pass

            if submit_button4:
                user_id = st.session_state["user_dir"]
                username = os.path.basename(user_id)
                log_action(username, "Genera progettazione della lezione", commentoPdl)
                start_time = time.time()  # Tempo di inizio
                delete_progettazione_info()
                getProgettazione(progm_didat.tipo_scuola, progm_didat.grado, progm_didat.indirizzo,
                                 progm_didat.articolazione, progm_didat.linee_guida, progm_didat.disciplina, lezione,
                                 progm_didat.contesto, progm_didat.docente, client, uda, commentoPdl)
                end_time = time.time()
                track_execution_time("Genera progettazione della lezione", start_time, end_time)
                succ_pl.success('La progettazione della lezione è stata generata con successo!', icon="✅")
                time.sleep(5)
                st.session_state.disabledMateriale = True
                st.session_state.disabledMD = True
                st.session_state.disabledZip = True
                st.session_state.disabledPDL = False
                st.session_state.disabledL = False
                st.rerun()
            ready = False
            # Controllo se il file progettazione.json esiste
            if os.path.exists(file_introduttiva_path):
                col19, col20 = st.columns([1000, 1])
                with col19:
                    st.markdown('<div id="indice3"></div>', unsafe_allow_html=True)
                    # Mostra i dati nel componente st.expander
                    with st.expander("Dettagli della Lezione - Progettazione"):
                        carica_dati_introduttiva(file_introduttiva_path)
                        compileProgettazione()
                with col20:
                    pass

        with stylable_container(
                key="container4",
                css_styles="""
                            {
                                border: 1px solid #E9E9FA;
                                border-radius: 0.5rem;
                                background-color: #FAFAFD;
                                padding: calc(1em - 1px)
                                }
                                """,
        ):
            st.markdown("<h4>Fase attiva</h4>", unsafe_allow_html=True)
            col21, col22 = st.columns([1000, 1])
            with col21:
                st.text(
                    "SUGGERIMENTO: Dopo aver generato l’esposizione della lezione, esaminala attentamente. Se necessario, utilizza l'area commenti per suggerire modifiche e adattarla meglio al tuo stile di insegnamento e alle esigenze della classe. Questo processo potrebbe impiegare fino a 2 minuti.")

                commentoEsposizione = st.text_area("None", "", label_visibility="collapsed",
                                                   placeholder="Inserisci qui il tuo commento, se vuoi modificare l'esposizione",
                                                   key="commentoEsposizione")
            with col22:
                pass

            col23, col24 = st.columns([1000, 1])
            with col23:
                submit_buttonPDL = st.button("Genera Esposizione Lezione", disabled=st.session_state.disabledPDL, on_click=callbackPDL)
            with col24:
                pass

            file_esposizione_path = os.path.join(st.session_state["user_dir"], "esposizione.json")
            file_materiale_path = os.path.join(st.session_state["user_dir"], "materiali.json")

            col25, col26 = st.columns([1000, 1])
            with col25:
                succ_el = st.container()
            with col26:
                pass

            if submit_buttonPDL:
                user_id = st.session_state["user_dir"]
                username = os.path.basename(user_id)
                log_action(username, "Genera esposizione della lezione", commentoEsposizione)
                start_time = time.time()
                delete_esposizione_info()
                getEsecuzione(client, commentoEsposizione)
                getEsposizione(client, commentoEsposizione)
                end_time = time.time()
                track_execution_time("Genera esposizione della lezione", start_time, end_time)
                succ_el.success('La modalità  di erogazione della lezione è stata generata con successo!', icon="✅")
                time.sleep(5)
                st.session_state.disabledMateriale = True
                st.session_state.disabledMD = True
                st.session_state.disabledMateriale = False
                st.session_state.disabledZip = True
                st.session_state.disabledPDL = False
                st.rerun()

            # Controllo se il file esecuzione.json esiste
            if os.path.exists(file_esposizione_path):
                col27, col28 = st.columns([1000, 1])
                with col27:
                    # Mostra i dati nel componente st.expander
                    with st.expander("Dettagli della Lezione - Esecuzione"):
                        carica_dati_esposizione(file_esposizione_path)
                        compileEsecuzione()
                        pass
                with col28:
                    pass

        with stylable_container(
            key="container5",
            css_styles="""
                        {
                            border: 1px solid #E9E9FA;
                            border-radius: 0.5rem;
                            background-color: #FAFAFD;
                            padding: calc(1em - 1px)
                            }
                            """,
        ):
            st.markdown("<h4>Materiale didattico</h4>", unsafe_allow_html=True)
            col29, col30 = st.columns([1000, 1])
            with col29:
                st.text(
                    "SUGGERIMENTO: Dopo aver generato il materiale didattico, esaminalo con attenzione. Se desideri modificarlo o personalizzarlo, utilizza l'area commenti per suggerire miglioramenti in base alle esigenze della tua lezione. Questo processo potrebbe impiegare fino a 1 minuto.")

                commentoMateriale = st.text_area("None", "", label_visibility="collapsed",
                                                 placeholder="Inserisci qui il tuo commento, se vuoi modificare materiale didattico",
                                                 key="commentoMateriale")
            with col30:
                pass

            col31, col32 = st.columns([1000, 1])
            with col31:
                submit_buttonMateriale = st.button("Genera Materiale Didattico",
                                                   disabled=st.session_state.disabledMateriale, on_click=callbackMateriale)
            with col32:
                pass

            col33, col34 = st.columns([1000, 1])
            with col33:
                succ_mat = st.container()
            with col34:
                pass
            revision_check = st.checkbox(
                """
                Ho revisionato tutti i contenuti generati e verificato che:
                - Obiettivi e prerequisiti sono coerenti
                - I tempi sono consistenti e realistici  
                - Sono presenti adattamenti per BES/DSA
                - Le verifiche sono allineate agli obiettivi
                """,
                value=st.session_state.get('revision_checked', False),
                key="revision_complete"
            )

            if submit_buttonMateriale:
                user_id = st.session_state["user_dir"]
                username = os.path.basename(user_id)
                log_action(username, "Genera materiale didattico", commentoMateriale)
                start_time = time.time()
                delete_materiale_info()
                getMateriale(commentoMateriale, client)
                crea_unico_materiale()
                end_time = time.time()
                track_execution_time("Genera Materiale Didattico", start_time, end_time)
                succ_mat.success('Il materiale didattico è stato generato con successo!', icon="✅")
                st.session_state.disabledZip = True
                st.session_state.disabledMateriale = False
                st.session_state.disabledMD = False
                time.sleep(5)
                st.rerun()

            output_folder = os.path.join(st.session_state["user_dir"], "materiale_didattico")
            os.makedirs(output_folder, exist_ok=True)
            zip_file_path = os.path.join(st.session_state["user_dir"], "materiale_didattico_completo")

            st.markdown('<div id="container3"></div>', unsafe_allow_html=True)
            # Controllo se il file esecuzione.json esiste
            if os.path.exists(file_materiale_path):
                col35, col36 = st.columns([1000, 1])
                with col35:
                    # Mostra i dati nel componente st.expander
                    with st.expander("Dettagli della Lezione - Materiale Didattico"):
                        carica_dati_materiale(file_materiale_path)
                        compileMateriale()
                with col36:
                    pass
            st.markdown('<div id="container4"></div>', unsafe_allow_html=True)
            col37, col38 = st.columns([1000, 1])
            # Feedback visivo
            if revision_check:
                st.session_state.disabledMD = False
                st.success("🎉 Revisione approvata! Modalità modifica **abilitata**.")

            else:
                st.warning("📝 Completa la revisione per abilitare la modifica dei contenuti.")
                st.session_state.disabledMD = True
            with col37:
                if st.button("Salva tutto il Materiale Didattico",
                             disabled=st.session_state.disabledMD, key="submitMD"):
                    user_id = st.session_state["user_dir"]
                    username = os.path.basename(user_id)
                    log_action(username, "Salva tutto il materiale", "Nessun commento")
                    compile_progettazione_didattica()
                    compileFile()
                    st.session_state.disabledZip = False
                    succ_mat.success('Il materiale didattico è stato salvato con successo!', icon="✅")
            with col38:
                pass
            col39, col40 = st.columns([1000, 1])
            with col39:
                succ_salva = st.container()
            with col40:
                pass
            shutil.make_archive(zip_file_path, 'zip', output_folder)
            col41, col42 = st.columns([1000, 1])

            with col41:
                with open(f"{zip_file_path}.zip", "rb") as zip_file:
                    download_clicked = st.download_button(
                        label="Scarica la cartella compressa",
                        data=zip_file,
                        file_name="materiale_didattico.zip",
                        disabled=st.session_state.disabledZip,
                        mime="application/zip"
                    )
                    if download_clicked:
                        user_id = st.session_state["user_dir"]
                        username = os.path.basename(user_id)
                        log_action(username, "Scarica la cartella compressa", "Nessun commento")
            with col42:
                pass
    with col4:

        with sticky_container(mode="top", border=True):
            st.subheader("Indice")
            st.markdown("""
                      <ul id="indice">
    <li><a href="#container1" class="indice-link">Progettazione didattica per disciplina</a>
        <ul>
            <li><a href="#indice1" class="indice-link">Informazioni generali</a></li>
            <li><a href="#indice2" class="indice-link">Unità didattiche</a></li>
        </ul>
    </li>
    <li><a href="#container2" class="indice-link">Progettazione della lezione</a>
        <ul>
            <li><a href="#indice3" class="indice-link">Dettagli della progettazione della lezione</a></li>
            <li><a href="#indice4" class="indice-link">Verifica dei prerequisiti</a></li>
            <li><a href="#indice5" class="indice-link">Nucleo centrale</a></li>
            <li><a href="#indice6" class="indice-link">Verifica degli obiettivi</a></li>
        </ul>
    </li>
    <li><a href="#container3" class="indice-link">Materiale didattico</a>
        <ul>
            <li><a href="#container4" class="indice-link">Scarica materiale didattico</a></li>
        </ul>
    </li>
</ul>

                  """, unsafe_allow_html=True)

# JavaScript per evidenziare la voce dell'indice in base alla posizione del contenuto
components.html("""
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            var sections = document.querySelectorAll('div[id]');
            var links = document.querySelectorAll('.indice-link');

            function highlightLink() {
                let scrollPosition = window.scrollY + window.innerHeight / 3;

                sections.forEach((section, index) => {
                    let rect = section.getBoundingClientRect();
                    let link = links[index];

                    if (rect.top <= window.innerHeight / 3 && rect.bottom >= window.innerHeight / 3) {
                        links.forEach(l => l.style.color = ''); // Reset colori
                        link.style.color = 'red';  // Evidenzia la voce attiva
                    }
                });
            }

            window.addEventListener('scroll', highlightLink);
            highlightLink();  // Chiamata iniziale per aggiornare lo stato subito
        });
    </script>
""", height=0)
