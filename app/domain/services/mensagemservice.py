from collections import defaultdict
from typing import List

from app.application.dto.filtrodto import FiltroDTO
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from app.domain.repositories.mensagemrepository import IMensagemRepository
from app.domain.entities.numero import Numero
from datetime import datetime

DIAS_SEMANA = {
    0: "Segunda-feira",
    1: "Terça-feira",
    2: "Quarta-feira",
    3: "Quinta-feira",
    4: "Sexta-feira",
    5: "Sábado",
    6: "Domingo"
}

class MensagemService():
    def __init__(self, mensagem_repository: IMensagemRepository):
        self.repository = mensagem_repository
        
    def count_mensagens_por_alvo(self, numero: Numero) -> dict[str, int]:
        mensagens = self.repository.get_mensagens_from_numero_id(numero.id)
        mem = defaultdict(int)
        
        for mensagem in mensagens:
            numero_alvo = numero.numero
            remetente = mensagem.remetente
            destinatario = mensagem.destinatario
            
            if remetente == numero_alvo:
                mem[destinatario] += 1
            elif destinatario == numero_alvo:
                mem[remetente] += 1

        return dict(mem)

    def count_mensagens_por_ip(self, ip_obj):
        mensagens = self.repository.get_mensagens_by_ip(ip_obj.id)
        count_map = {}
        for msg in mensagens:
            dest = msg.destinatario
            count_map[dest] = count_map.get(dest, 0) + 1
        return count_map

    def obter_quantidade_mensagens_por_contato(
        self,
        numeros: list[str],
        tickets: list[str],
        tipo: str,
        grupo: str,
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> list[dict]:
        return self.repository.contar_mensagens_por_contato(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        
    def obter_quantidade_mensagens_por_ip(
        self,
        numeros: list[str],
        tickets: list[str],
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> list[dict]:
        return self.repository.contar_mensagens_por_ip(
            numeros=numeros,
            tickets=tickets,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
    
    def obter_quantidade_mensagens_por_horario(
        self,
        numeros: list[str],
        tickets: list[str],
        tipo: str,
        grupo: str,
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> list[dict]:
        """
        Agrupa e conta mensagens por faixas de horário (a cada 2 horas), com base nos filtros fornecidos.
        """
        return self.repository.contar_mensagens_por_horario(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

    def obter_quantidade_mensagens_por_dia(
        self,
        numeros: list[str],
        tickets: list[str],
        tipo: str,
        grupo: str,
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> list[dict]:
        """
        Agrupa e conta mensagens por dia, com base nos filtros fornecidos.
        """
        resultados = self.repository.contar_mensagens_por_dia(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        return self.mapear_para_dia_semana(resultados)

    def mapear_para_dia_semana(self, resultados: list[dict]) -> list[dict]:
        agrupado = defaultdict(int)

        for r in resultados:
            data_str = r["data"]  # formato: "YYYY-MM-DD"
            data_obj = datetime.strptime(data_str, "%Y-%m-%d")
            dia_index = data_obj.weekday()  # 0 = segunda, 6 = domingo
            dia_nome = DIAS_SEMANA[dia_index]
            agrupado[dia_nome] += r["qtdMensagens"]

        # Retorna dias na ordem da semana
        return [
            {"dia": DIAS_SEMANA[i], "qtdMensagens": agrupado.get(DIAS_SEMANA[i], 0)}
            for i in range(7)
        ]

    def obter_quantidade_mensagens_por_ip(
        self,
        numeros: list[str],
        tickets: list[str],
        tipo: str,
        grupo: str,
        data_inicial: str,
        data_final: str,
        hora_inicio: str,
        hora_fim: str
    ) -> list[dict]:
        """
        Retorna contagem de mensagens por IP, aplicando todos os filtros.
        """
        return self.repository.contar_mensagens_por_ip(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )

    def buscar_por_filtro(
            self,
            numeros: list[str],
            tickets: list[str],
            tipo: str,
            grupo: str,
            data_inicial: str,
            data_final: str,
            hora_inicio: str,
            hora_fim: str
    ) -> list[dict]:
        return self.repository.buscar_por_filtro(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )