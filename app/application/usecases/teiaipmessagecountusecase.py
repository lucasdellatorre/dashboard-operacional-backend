from app.application.dto.numeromessagecountdto import NumeroMessageCountResponseDTO
from app.application.dto.teiaipmessagecountdto import TeiaIPMessageCountRequestDTO
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.numeroservice import NumeroService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.targetresolverservice import TargetResolverService

class TeiaIPMessageCountUseCase:
    def __init__(
        self,
        suspeito_service: SuspeitoService,
        numero_service: NumeroService,
        mensagem_service: MensagemService,
        interceptacao_service: InterceptacaoService,
        target_resolver_service: TargetResolverService
    ):
        self.suspeito_service = suspeito_service
        self.numero_service = numero_service
        self.mensagem_service = mensagem_service
        self.interceptacao_service = interceptacao_service
        self.target_resolver_service = target_resolver_service    

    def execute(self, request: TeiaIPMessageCountRequestDTO) -> NumeroMessageCountResponseDTO:
        RED = 3  # Suspeito
        GRAY = 7  # Número avulso

        nodes = []
        links = []
        added_nodes = set()

        if not (request.suspeitos or request.numeros or request.operacoes):
            raise ValueError("É necessário informar ao menos um dos seguintes: suspeitos, números ou operações.")
        
        # Se tem apenas operações, busca numeros na target resolver
        if not request.suspeitos and not request.numeros:
            numero_ids, tickets = self.target_resolver_service.resolver_alvos_ip(request)
            request.numeros = numero_ids
            request.operacoes = tickets
        else:
            tickets = []
            if request.operacoes:
                interceptacoes = self.interceptacao_service.get_interceptacoes_por_operacoes(request.operacoes)
                tickets = [i.internalTicketNumber for i in interceptacoes]

            for suspeito_id in request.suspeitos:
                suspeito = self.suspeito_service.get_info_e_numeros_by_id(suspeito_id)
                if not suspeito:
                    continue
                nome = suspeito.get("apelido") or suspeito.get("nome") or "Desconhecido"
                node_id = nome

                if node_id not in added_nodes:
                    nodes.append({
                        "id": node_id,
                        "label": nome,
                        "group": RED
                    })
                    added_nodes.add(node_id)

                numeros_alvo = [
                    n for n in suspeito.get("numeros", [])
                ]

                if not numeros_alvo:
                    continue

                for numero in numeros_alvo:
                    resultados = self.mensagem_service.obter_quantidade_mensagens_por_ip(
                        numeros=[numero],
                        tickets=tickets,
                        tipo=None,
                        grupo=None,
                        data_inicial=request.data_inicial,
                        data_final=request.data_final,
                        hora_inicio=request.hora_inicio,
                        hora_fim=request.hora_fim
                    )

                    for resultado in resultados:
                        ip = resultado["ip"]
                        ocorrencias = resultado["qtdMensagens"]

                        links.append({
                            "source": node_id,
                            "target": ip,
                            "value": ocorrencias
                        })

        for numero in request.numeros:
            if numero not in added_nodes:
                nodes.append({
                    "id": numero,
                    "group": GRAY
                })
                added_nodes.add(numero)

            resultados = self.mensagem_service.obter_quantidade_mensagens_por_ip(
                numeros=[numero],   
                tickets=tickets,
                tipo=None,
                grupo=None,
                data_inicial=request.data_inicial,
                data_final=request.data_final,
                hora_inicio=request.hora_inicio,
                hora_fim=request.hora_fim
            )

            for resultado in resultados:
                ip = resultado["ip"]
                qtd = resultado["qtdMensagens"]

                links.append({
                    "source": numero,
                    "target": ip,
                    "value": qtd
                })
                
        return NumeroMessageCountResponseDTO(nodes=nodes, links=links)