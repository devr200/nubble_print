"""
Configurazione dell'applicazione
"""
import os
from pathlib import Path
from dotenv import load_dotenv


# Carica variabili d'ambiente
load_dotenv()


class Config:
    """Configurazione centralizzata dell'applicazione"""
    
    # API
    API_URL = os.getenv('API_URL', 'https://app.nubble.it/api/printData')
    API_TOKEN = os.getenv('API_TOKEN', 'wqowok9emjibwc7adknn')
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', 10))
    
    # Printer
    PRINTER_URL = os.getenv('PRINTER_URL', 'http://192.168.1.100:9100')  # IP stampante
    
    # Polling
    POLL_INTERVAL = int(os.getenv('POLL_INTERVAL', 5))
    MAX_POLL_INTERVAL = int(os.getenv('MAX_POLL_INTERVAL', 30))
    BACKOFF_MULTIPLIER = float(os.getenv('BACKOFF_MULTIPLIER', 1.5))
    
    # Printer
    DEFAULT_PRINTER = os.getenv('DEFAULT_PRINTER', '')
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/nubble_print.log')
    
    @classmethod
    def validate(cls):
        """Valida la configurazione"""
        errors = []
        
        if not cls.API_URL:
            errors.append("API_URL non configurato")
        if not cls.PRINTER_URL:
            errors.append("PRINTER_URL non configurato")
        
        if errors:
            raise ValueError(f"Errori di configurazione: {', '.join(errors)}")
        
        return True
