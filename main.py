#!/usr/bin/env python3
"""
Nubble Print Client - Client multipiattaforma per stampa automatica
"""
import asyncio
import logging
import signal
import sys
from pathlib import Path

from src.config import Config
from src.services import APIService, PrintService, PollingService


def setup_logging():
    """Configura il sistema di logging"""
    # Crea la directory dei log se non esiste
    log_path = Path(Config.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configura il formato del log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configura logging su file e console
    logging.basicConfig(
        level=getattr(logging, Config.LOG_LEVEL),
        format=log_format,
        handlers=[
            logging.FileHandler(Config.LOG_FILE),
            logging.StreamHandler(sys.stdout)
        ]
    )


async def main():
    """Entry point principale dell'applicazione"""
    logger = logging.getLogger(__name__)
    
    try:
        logger.info("=" * 60)
        logger.info("Nubble Print Client - Avviato")
        logger.info("=" * 60)
        
        # Valida la configurazione
        Config.validate()
        logger.info(f"API: {Config.API_URL}")
        
        # Inizializza i servizi
        api_service = APIService(
            api_url=Config.API_URL,
            api_token=Config.API_TOKEN,
            timeout=Config.API_TIMEOUT
        )
        
        print_service = PrintService(
            printer_url=Config.PRINTER_URL,
            timeout=Config.API_TIMEOUT
        )
        
        polling_service = PollingService(
            api_service=api_service,
            print_service=print_service,
            poll_interval=Config.POLL_INTERVAL,
            max_poll_interval=Config.MAX_POLL_INTERVAL,
            backoff_multiplier=Config.BACKOFF_MULTIPLIER
        )
        
        # Mostra stampante configurata
        printers = print_service.get_available_printers()
        logger.info(f"Stampante configurata: {', '.join(printers)}")
        
        # Test connessione API
        if not api_service.test_connection():
            logger.error("Impossibile connettersi all'API. Controlla la configurazione.")
            return 1
        
        # Test connessione stampante
        print_service.test_connection()
        
        # Gestione segnali per chiusura pulita
        def signal_handler(sig, frame):
            logger.info("Segnale di interruzione ricevuto...")
            polling_service.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        logger.info("Premi Ctrl+C per fermare il servizio")
        logger.info("-" * 60)
        
        # Avvia il polling
        await polling_service.start()
        
    except ValueError as e:
        logger.error(f"Errore di configurazione: {e}")
        return 1
    except Exception as e:
        logger.exception(f"Errore fatale: {e}")
        return 1
    finally:
        logger.info("=" * 60)
        logger.info("Nubble Print Client - Terminato")
        logger.info("=" * 60)
    
    return 0


if __name__ == "__main__":
    setup_logging()
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
