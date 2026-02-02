"""
Servizio per la gestione delle chiamate API
"""
import logging
import requests
import base64
from typing import Optional


logger = logging.getLogger(__name__)


class APIService:
    """Gestisce le chiamate API al server Laravel"""
    
    def __init__(self, api_url: str, api_token: str, timeout: int = 10):
        self.api_url = api_url
        self.api_token = api_token
        self.timeout = timeout
        self.session = requests.Session()
    
    def get_print_data(self) -> Optional[str]:
        """
        Effettua una chiamata POST all'API per ottenere i dati da stampare
        
        Returns:
            XML string da stampare oppure None se non ci sono dati
        """
        try:
            response = self.session.post(
                self.api_url,
                data={'token': self.api_token},
                timeout=self.timeout
            )
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('success') and data.get('data'):
                xml_base64 = data['data']
                
                # Decodifica da base64
                try:
                    xml_data = base64.b64decode(xml_base64).decode('utf-8')
                    logger.info(f"Ricevuti e decodificati dati XML dall'API ({len(xml_data)} caratteri)")
                    return xml_data
                except Exception as e:
                    logger.error(f"Errore nella decodifica base64: {e}")
                    return None
            else:
                logger.debug("Nessun dato disponibile dall'API")
                return None
                
        except requests.exceptions.Timeout:
            logger.error(f"Timeout nella chiamata API (>{self.timeout}s)")
            return None
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Errore di connessione all'API: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logger.error(f"Errore HTTP dall'API: {e}")
            return None
        except ValueError as e:
            logger.error(f"Errore nel parsing JSON della risposta: {e}")
            return None
        except Exception as e:
            logger.error(f"Errore imprevisto nella chiamata API: {e}")
            return None
    
    def test_connection(self) -> bool:
        """Testa la connessione all'API"""
        try:
            response = self.session.post(
                self.api_url,
                data={'token': self.api_token},
                timeout=self.timeout
            )
            response.raise_for_status()
            logger.info(f"Connessione all'API riuscita: {self.api_url}")
            return True
        except Exception as e:
            logger.error(f"Impossibile connettersi all'API: {e}")
            return False
