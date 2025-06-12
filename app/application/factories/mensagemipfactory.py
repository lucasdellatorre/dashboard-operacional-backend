from app.adapters.repositories.interceptacaonumerorepository import InterceptacaoNumeroRepository
from app.adapters.repositories.interceptacaorepository import InterceptacaoRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository

from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.targetresolverservice import TargetResolverService

from app.application.usecases.buscarmensagemporipusecase import BuscarMensagemPorIPUseCase

class MensagemIpFactory:
    @staticmethod
    def buscar_mensagens_por_ip() -> BuscarMensagemPorIPUseCase:
        interceptacao_numero_repo = InterceptacaoNumeroRepository()
        interceptacao_repo = InterceptacaoRepository()
        suspeito_repo = SuspeitoRepository()
        mensagem_repo = MensagemRepository()

        interceptacao_numero_service = InterceptacaoNumeroService(interceptacao_numero_repo)
        interceptacao_service = InterceptacaoService(interceptacao_repo)
        suspeito_service = SuspeitoService(suspeito_repo, interceptacao_numero_repo)
        mensagem_service = MensagemService(mensagem_repo)
        target_resolver = TargetResolverService(suspeito_service, interceptacao_service, interceptacao_numero_service)

        return BuscarMensagemPorIPUseCase(mensagem_service, target_resolver)