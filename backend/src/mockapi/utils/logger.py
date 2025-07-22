import logging
import os


from mockapi.core.config import app_settings
os.makedirs(app_settings.LOG_DIR, exist_ok=True)

def get_logger(name="mockapi"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.FileHandler(app_settings.LOG_FILE, encoding="utf-8")
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        if app_settings.SHOW_CONSOLE_LOG:
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
        logger.setLevel(logging.INFO)
    return logger
