import json


class ProgettazioneDidattica:

    def __init__(self, tipo_scuola, indirizzo, linee_guida, grado, contesto, docente, disciplina, articolazione, ore_anno, ore_sett):
        """
        Inizializza la progettazione didattica con le informazioni di base.

        :param tipo_scuola: Tipo di scuola (es. "ITS", "Scuola Secondaria")
        :param indirizzo: Indirizzo del corso (es. "Informatica", "Amministrazione")
        :param grado: Grado della classe (es. "5° anno")
        :param contesto: Contesto della classe (es. "Classe con interesse per la programmazione")
        :param docente: Nome del docente responsabile della progettazione didattica
        """
        self.tipo_scuola = tipo_scuola
        self.indirizzo = indirizzo
        self.linee_guida = linee_guida
        self.grado = grado
        self.contesto = contesto
        self.docente = docente
        self.disciplina = disciplina
        self.articolazione = articolazione
        self.ore_anno = ore_anno
        self.ore_sett = ore_sett


    def visualizza_progettazione(self):
        """
        Visualizza tutte le informazioni relative alla progettazione didattica.
        """
        print(f"Progettazione Didattica per la Scuola: {self.tipo_scuola}")
        print(f"Indirizzo: {self.indirizzo}")
        print(f"Grado: {self.grado}")
        print(f"Contesto: {self.contesto}")
        print(f"Docente Responsabile: {self.docente}")
        print("\nUnità Didattiche di Apprendimento (UDA):")
        for uda in self.uda_list:
            print(f"- {uda['Nome UDA']} (Periodo: {uda['Periodo']})")
            print(f"  Motivazioni: {uda['Motivazioni']}")
        print("\n")

    def salva_progettazione(self, file_name="progettazione_didattica.json"):
        """
        Salva la progettazione didattica in un file JSON.

        :param file_name: Nome del file JSON dove salvare la progettazione (default: "progettazione_didattica.json")
        """
        progettazione_dict = {
            "Tipo Scuola": self.tipo_scuola,
            "Indirizzo": self.indirizzo,
            "Grado": self.grado,
            "Contesto": self.contesto,
            "Docente": self.docente,
            "UDA": self.uda_list
        }
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(progettazione_dict, file, ensure_ascii=False, indent=4)
        print(f"Progettazione salvata in {file_name}")

# Esempio di utilizzo della classe

# Crea una nuova progettazione didattica


# Aggiungi alcune UDA
#progettazione.aggiungi_uda("Introduzione ai Sistemi Informativi", "Settembre-Ottobre", "Introduzione ai sistemi informativi aziendali per comprendere le basi dell'organizzazione.")
#progettazione.aggiungi_uda("Progettazione di Basi di Dati", "Novembre-Dicembre", "L'insegnamento delle basi di dati è fondamentale per organizzare e gestire le informazioni aziendali.")

# Visualizza la progettazione
#progettazione.visualizza_progettazione()

# Salva la progettazione in un file JSON
#progettazione.salva_progettazione("progettazione_informatica.json")
