class MensagemPorDiaResponseDTO:
    def __init__(
        self,
        dia_semana: int,
        quantidade_mensagens: int
    ):
        self.dia_semana = dia_semana
        self.quantidade_mensagens = quantidade_mensagens

    def to_dict(self):
        return {
            "dia_semana": int(self.dia_semana),
            "quantidade_mensagens": int(self.quantidade_mensagens)
        }