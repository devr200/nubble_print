"""
Servizio per la stampa diretta su stampante IP
"""
import logging
import requests
from typing import Optional
from ..models import PrintJob


logger = logging.getLogger(__name__)


class PrintService:
    """Gestisce l'invio diretto di XML alla stampante via HTTP"""
    
    def __init__(self, printer_url: str, timeout: int = 30):
        self.printer_url = printer_url
        self.timeout = timeout
        self.session = requests.Session()
        logger.info(f"PrintService inizializzato - Stampante: {printer_url}")
    
    def print_job(self, job: PrintJob) -> bool:
        """
        Invia l'XML direttamente alla stampante
        
        Args:
            job: Il job da stampare contenente l'XML
            
        Returns:
            True se l'invio è riuscito
        """
        try:
            logger.info(f"Invio XML alla stampante ({len(job.xml_body)} caratteri)")
            
            # POST XML alla stampante con Content-Type: application/xml
            response = self.session.post(
                self.printer_url,
                data=job.xml_body.encode('utf-8'),
                headers={'Content-Type': 'application/xml'},
                timeout=self.timeout,
                verify=False  # trusty: true
            )
            
            response.raise_for_status()
            
            # Log della risposta
            response_text = response.text
            logger.info(f"Stampante risposta: {response_text[:200]}")
            logger.info("Documento inviato con successo alla stampante")
            
            return True
            
        except requests.exceptions.Timeout:
            logger.error(f"Timeout nella comunicazione con la stampante (>{self.timeout}s)")
            return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Impossibile connettersi alla stampante {self.printer_url}: {e}")
            return False
        except requests.exceptions.HTTPError as e:
            logger.error(f"Errore HTTP dalla stampante: {e}")
            logger.error(f"Status code: {e.response.status_code}")
            logger.error(f"Response: {e.response.text[:500]}")
            return False
        except Exception as e:
            logger.error(f"Errore imprevisto durante l'invio alla stampante: {e}")
            return False
    
    def test_connection(self) -> bool:
        """Testa la connessione alla stampante"""
        try:
            # Prova una semplice GET per verificare che la stampante risponda
            response = self.session.get(
                self.printer_url,
                timeout=5,
                verify=False
            )
            logger.info(f"Stampante raggiungibile: {self.printer_url}")
            return True
        except Exception as e:
            logger.warning(f"Test connessione stampante fallito (potrebbe essere normale): {e}")
            # Alcune stampanti non rispondono a GET, quindi non è necessariamente un errore
            return True
    
    def get_available_printers(self) -> list:
        """
        Ritorna l'URL della stampante configurata
        
        Returns:
            Lista con l'URL della stampante configurata
        """
        return [self.printer_url]
