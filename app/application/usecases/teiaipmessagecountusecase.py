from app.application.dto.teiaipmessagecountdto import TeiaIPMessageCountRequestDTO, TeiaIPMessageCountResponseDTO

class TeiaIPMessageCountUseCase:
    def __init__(self, teia_ip_service, mensagem_service):
        self.teia_ip_service = teia_ip_service
        self.mensagem_service = mensagem_service

    def execute(self, request: TeiaIPMessageCountRequestDTO) -> TeiaIPMessageCountResponseDTO:
        nodes = []
        links = []
        RED = 3
        GRAY = 7

        for ip_id in request.ip_ids:
            ip_obj = self.teia_ip_service.find(ip_id)
            if not ip_obj:
                continue
            print(f"[DEBUG] Encontrado IP: {ip_obj.ip} (ID: {ip_id})")

            nodes.append({"id": ip_obj.ip, "group": RED})
            relations = self.mensagem_service.count_mensagens_por_ip(ip_obj)

            for target, count in relations.items():
                links.append({"source": ip_obj.ip, "target": target, "value": count})
                if not any(n['id'] == target for n in nodes):
                    nodes.append({"id": target, "group": GRAY})

        return TeiaIPMessageCountResponseDTO(nodes, links)