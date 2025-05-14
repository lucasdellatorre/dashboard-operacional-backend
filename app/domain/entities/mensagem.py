from dataclasses import dataclass
from typing import Optional, Any

@dataclass
class Mensagem:
    id: int
    internalTicketNumber: str
    grupoId: str
    numeroId: int
    remetente: Optional[str] = None
    remetenteIp: Optional[str] = None
    remetenteDispositivo: Optional[str] = None
    tipoMensagem: Optional[str] = None
    estiloMensagem: Optional[str] = None
    tamanhoMensagem: Optional[str] = None
    data: Optional[str] = None
    hora: Optional[str] = None
    timestamp: Optional[Any] = None  # Use datetime if you know the type
    destinatario: Optional[str] = None
    messageExternalId: Optional[str] = None
    remetentePorta: Optional[str] = None
