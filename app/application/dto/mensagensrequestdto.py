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
        grupo = data.get("grupo", "AMBOS").upper()
        if grupo not in ["GRUPO", "NÚMERO", "AMBOS"]:
            raise ValueError("Grupo inválido. Valores permitidos: GRUPO, NÚMERO, AMBOS.")

        tipo = data.get("tipo", "TODOS").upper()
        if tipo not in ["TEXTO", "VÍDEO", "TODOS"]:
            raise ValueError("Tipo inválido. Valores permitidos: TEXTO, VÍDEO, TODOS.")

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
