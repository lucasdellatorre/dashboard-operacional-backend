from app.adapters.repositories.interceptacaonumerorepository import InterceptacaoNumeroRepository
from app.adapters.repositories.interceptacaorepository import InterceptacaoRepository
from app.adapters.repositories.suspeitorepository import SuspeitoRepository
from app.adapters.repositories.mensagemrepository import MensagemRepository

from app.domain.services.interceptacaonumeroservice import InterceptacaoNumeroService
from app.domain.services.interceptacaoservice import InterceptacaoService
from app.domain.services.suspeitoservice import SuspeitoService
from app.domain.services.mensagemservice import MensagemService
from app.domain.services.exportservice import ExportService
from app.domain.services.targetresolverservice import TargetResolverService

from app.application.usecases.exportusecase import ExportUseCase


class ExportFactory:
    @staticmethod
    def export_use_case() -> ExportUseCase:
        interceptacao_numero_repo = InterceptacaoNumeroRepository()
        interceptacao_repo = InterceptacaoRepository()
        suspeito_repo = SuspeitoRepository()
        mensagem_repo = MensagemRepository()

        interceptacao_numero_service = InterceptacaoNumeroService(interceptacao_numero_repo)
        interceptacao_service = InterceptacaoService(interceptacao_repo)
        suspeito_service = SuspeitoService(suspeito_repo, interceptacao_numero_repo)
        mensagem_service = MensagemService(mensagem_repo)
        export_service = ExportService()
        target_resolver = TargetResolverService(suspeito_service, interceptacao_service, interceptacao_numero_service)

        return ExportUseCase(target_resolver, suspeito_service, mensagem_service, export_service)