"""
Servizio di polling ottimizzato con backoff esponenziale
"""
import logging
import asyncio
from typing import Callable
from .api_service import APIService
from .print_service import PrintService
from ..models import PrintJob


logger = logging.getLogger(__name__)


class PollingService:
    """Gestisce il polling ottimizzato dell'API"""
    
    def __init__(
        self,
        api_service: APIService,
        print_service: PrintService,
        poll_interval: int = 5,
        max_poll_interval: int = 30,
        backoff_multiplier: float = 1.5
    ):
        self.api = api_service
        self.printer = print_service
        self.poll_interval = poll_interval
        self.max_poll_interval = max_poll_interval
        self.backoff_multiplier = backoff_multiplier
        self.current_interval = poll_interval
        self.is_running = False
    
    async def start(self):
        """Avvia il servizio di polling"""
        self.is_running = True
        logger.info(f"Servizio di polling avviato (intervallo: {self.current_interval}s)")
        
        while self.is_running:
            try:
                await self._poll_and_process()
            except Exception as e:
                logger.error(f"Errore durante il polling: {e}")
            
            # Attendi prima del prossimo polling
            await asyncio.sleep(self.current_interval)
        
        logger.info("Servizio di polling fermato")
    
    async def _poll_and_process(self):
        """Esegue un ciclo di polling e processa i dati trovati"""
        # Chiama l'API per ottenere dati
        xml_data = self.api.get_print_data()
        
        if xml_data:
            logger.info("Ricevuti dati da stampare dall'API")
            
            # Reset dell'intervallo quando ci sono dati
            self.current_interval = self.poll_interval
            
            # Crea un PrintJob temporaneo per la stampa
            job = PrintJob(
                id=0,  # Non più necessario con API
                xml_body=xml_data,
                printed=0
            )
            
            try:
                # Stampa il documento
                success = self.printer.print_job(job)
                
                if success:
                    logger.info("Stampa completata con successo")
                else:
                    logger.warning("Stampa fallita, verrà ritentata al prossimo polling")
            
            except Exception as e:
                logger.error(f"Errore durante l'elaborazione: {e}")
        
        else:
            # Nessun dato: aumenta l'intervallo (backoff esponenziale)
            self._increase_interval()
    
    def _increase_interval(self):
        """Aumenta l'intervallo di polling con backoff esponenziale"""
        new_interval = int(self.current_interval * self.backoff_multiplier)
        
        if new_interval <= self.max_poll_interval:
            self.current_interval = new_interval
            logger.debug(f"Intervallo di polling aumentato a {self.current_interval}s")
        elif self.current_interval < self.max_poll_interval:
            self.current_interval = self.max_poll_interval
            logger.debug(f"Intervallo di polling al massimo: {self.current_interval}s")
    
    def stop(self):
        """Ferma il servizio di polling"""
        self.is_running = False
        logger.info("Richiesta di arresto del servizio di polling")
