class MensagensRequestDTO:
    def __init__(self, numeros, suspeitos, operacoes, grupo, tipo, data_inicial, data_final, hora_inicio, hora_fim):
        self.numeros = numeros or []
        self.suspeitos = suspeitos or []
        self.operacoes = operacoes
        self.grupo = grupo
        self.tipo = tipo
        self.data_inicial = data_inicial
        self.data_final = data_final
        self.hora_inicio = hora_inicio
        self.hora_fim = hora_fim

    @classmethod
    def from_dict(cls, data: dict):
        # Validação básica obrigatória
        operacoes = data.get("operacoes")
        if operacoes and not isinstance(operacoes, list):
            raise ValueError("A lista de operações é obrigatória e deve ser uma lista.")

        # Valores padrões
        grupo = data.get("grupo", "all")
        if grupo and grupo.lower() not in ["group", "number", "all"]:
            raise ValueError("Grupo inválido. Valores permitidos: group, number, all.")

        tipo = data.get("tipo", "all")
        if tipo and tipo.lower() not in ["image", "audio", "video", "text", "all"]:
            raise ValueError("Tipo inválido. Valores permitidos: image, audio, video, text all")

        return cls(
            numeros=data.get("numeros", []),
            suspeitos=data.get("suspeitos", []),
            operacoes=operacoes,
            grupo=grupo,
            tipo=tipo,
            data_inicial=data.get("data_inicial"),
            data_final=data.get("data_final"),
            hora_inicio=data.get("hora_inicio"),
            hora_fim=data.get("hora_fim")
        )
