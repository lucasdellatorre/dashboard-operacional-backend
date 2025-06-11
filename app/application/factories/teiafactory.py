from app.adapters.repositories.interceptacaonumerorepository import InterceptacaoNumeroRepository
from app.adapters.repositories.numerorepository import NumeroRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.interceptacaorepository import InterceptacaoRepository

from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.numeroservice import NumeroService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.targetresolverservice import TargetResolverService

from app.application.usecases.teiamessagecount import TeiaMessageCountUseCase

class TeiaFactory:
    @staticmethod
    def message_count():
        # Repositórios
        numero_repo = NumeroRepository()
        mensagem_repo = MensagemRepository()
        suspeito_repo = SuspeitoRepository()
        interceptacao_repo = InterceptacaoRepository()
        interceptacao_numero_repo = InterceptacaoNumeroRepository()

        # Serviços
        numero_service = NumeroService(numero_repo)
        mensagem_service = MensagemService(mensagem_repo)
        suspeito_service = SuspeitoService(suspeito_repo, numero_repo)
        interceptacao_service = InterceptacaoService(interceptacao_repo)
        interceptacao_numero_service = InterceptacaoNumeroService(interceptacao_numero_repo)

        target_resolver = TargetResolverService(suspeito_service, interceptacao_service, interceptacao_numero_service)

        return TeiaMessageCountUseCase(
            suspeito_service=suspeito_service,
            numero_service=numero_service,
            mensagem_service=mensagem_service,
            interceptacao_service=interceptacao_service,
            target_resolver_service=target_resolver
        )
