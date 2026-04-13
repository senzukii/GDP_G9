import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name):
    # Créer le dossier /logs si inexistant
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, 'app.log')
    logger = logging.getLogger(name)

    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s | %(name)-12s | %(levelname)-8s | %(message)s')

        # Rotation : 1MB par fichier, max 5 fichiers
        handler = RotatingFileHandler(log_file, maxBytes=1*1024*1024, backupCount=5)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Affichage console pour le monitoring direct
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        console.setLevel(logging.INFO)
        logger.addHandler(console)

    return logger
