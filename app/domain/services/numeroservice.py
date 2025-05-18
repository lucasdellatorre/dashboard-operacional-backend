from app.domain.repositories.numerorepository import INumeroRepository
from app.domain.entities.numero import Numero
from collections import defaultdict

class NumeroService():
    def __init__(self, numero_repository: INumeroRepository):
        self.repository = numero_repository
        
    def find(self, numero_id) -> Numero:
        return self.repository.find(numero_id)
    
    def isAlvo(self, numero_id) -> bool:
        return self.repository.isAlvo(numero_id)
    
    def listarNumeroOperacao(self, operacao_ids: list[int]):
    
        dadosbase = self.repository.buscaNumero(operacao_ids)
        operacoes = self.repository.BuscarOperacoesNumero()

        operacoes_numero = defaultdict(set)
        for row in operacoes:
            operacoes_numero[row["numero"]].add((row["operacaoId"], row["nome"]))

        numeros_unicos = {}
        for item in dadosbase:
            numero = item["numero"]
            if numero not in numeros_unicos:
                item["operacoes"] = [
                    {"id": op_id, "nome": nome}
                    for op_id, nome in operacoes_numero.get(numero, set())
                ]
                numeros_unicos[numero] = item

        return list(numeros_unicos.values())
    
    def listar_numeros(self) -> list[Numero]:
        return self.repository.listar_todos()
