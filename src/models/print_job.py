"""
Modello dati per i job di stampa
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class PrintJob:
    """Rappresenta un job di stampa dal database"""
    id: int
    xml_body: str
    printed: int
    created_at: Optional[datetime] = None
    
    def __str__(self):
        return f"PrintJob(id={self.id}, printed={self.printed})"
