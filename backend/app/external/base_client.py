from abc import ABC, abstractmethod
from typing import Any, Dict
from backend.app.external.models import SecureDataPacket

class ExternalProviderAdapter(ABC):
    """Abstract interface for external governmental intelligence providers."""
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        pass

    @abstractmethod
    def request_data(self, resource_id: str, request_id: str) -> SecureDataPacket:
        """Executes challenge-response handshake and returns verified secure data packet."""
        pass
