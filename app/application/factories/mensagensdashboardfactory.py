from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.targetresolverservice import TargetResolverService

from app.adapters.repositories.interceptacaonumerorepository import InterceptacaoNumeroRepository
from app.adapters.repositories.interceptacaorepository import InterceptacaoRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository

from app.application.usecases.getmensagensporcontatousecase import GetMensagensPorContatoUseCase

class MensagensDashboardFactory:
    @staticmethod
    def get_mensagens_por_contato():
        interceptacao_numero_repo = InterceptacaoNumeroRepository()
        interceptacao_repo = InterceptacaoRepository()
        suspeito_repo = SuspeitoRepository()
        mensagem_repo = MensagemRepository()

        interceptacao_numero_service = InterceptacaoNumeroService(interceptacao_numero_repo)
        interceptacao_service = InterceptacaoService(interceptacao_repo)
        suspeito_service = SuspeitoService(suspeito_repo, interceptacao_numero_repo)
        mensagens_service = MensagemService(mensagem_repo)

        target_resolver_service = TargetResolverService(
            suspeito_service,
            interceptacao_service,
            interceptacao_numero_service
        )

        return GetMensagensPorContatoUseCase(
            target_resolver_service=target_resolver_service,
            mensagens_service=mensagens_service
        )
