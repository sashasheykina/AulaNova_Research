import logging
import os

# Configurazione base del logger
LOG_FILE = "global_actions.log"
LOG_DIR = "logs"
LOG_PATH = os.path.join(LOG_DIR, LOG_FILE)

os.makedirs(LOG_DIR, exist_ok=True)

def setup_logger():
    """Configura il logger globale se non esiste già."""
    if "global_logger" not in logging.root.manager.loggerDict:
        logger = logging.getLogger("global_logger")
        logger.setLevel(logging.INFO)

        # Rimuovi eventuali handler esistenti per sicurezza
        if logger.hasHandlers():
            logger.handlers.clear()

        # Configura i gestori
        file_handler = logging.FileHandler(LOG_PATH)
        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            '%(asctime)s | user_id=%(user_id)s | action=%(action)s | comment=%(comment)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

# Funzione per registrare l'azione
def log_action(user_id, action, comment=""):
    """Registra un'azione nel log con user_id, action e commento (opzionale)."""
    logger = logging.getLogger("global_logger")
    extra = {
        'user_id': user_id,
        'action': action,
        'comment': comment if comment else "N/A"
    }
    logger.info('Azione registrata', extra=extra)

# Assicurati che il logger sia configurato
setup_logger()
