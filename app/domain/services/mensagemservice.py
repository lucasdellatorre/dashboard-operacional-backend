from collections import defaultdict
from app.domain.repositories.mensagemrepository import IMensagemRepository
from app.domain.entities.numero import Numero
from app.application.dto.mensagensrequestdto import MensagensRequestDTO
from typing import List, Dict

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
        resultados = self.repository.contar_mensagens_por_contato(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        return resultados
    
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
        resultados = self.repository.contar_mensagens_por_horario(
            numeros=numeros,
            tickets=tickets,
            tipo=tipo,
            grupo=grupo,
            data_inicial=data_inicial,
            data_final=data_final,
            hora_inicio=hora_inicio,
            hora_fim=hora_fim
        )
        return resultados