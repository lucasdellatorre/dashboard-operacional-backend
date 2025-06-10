class MensagemPorIpResponseDTO:
    def __init__(
        self,
        ip: str,
        quantidade_mensagens: int,
    ):
        self.ip = ip
        self.quantidade_mensagens = quantidade_mensagens
    
    def to_dict(self) -> dict:
        return {
            "ip": self.ip,
            "quantidadeMensagens": self.quantidade_mensagens
        }
