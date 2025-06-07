import threading
import time
from flask import current_app
from io import BytesIO  
from app.application.dto.interceptacaouploaddto import InterceptacaoUploadDTO
from app.domain.services.uploadservice import UploadService
from app.domain.services.operacaoservice import OperacaoService
from app.infraestructure.utils.progress_tracker import set_progress
from app.infraestructure.utils.logger import logger


class InterceptacaoUploadUseCase:
    def __init__(self, upload_service: UploadService, operacao_service: OperacaoService):
        self.upload_service = upload_service
        self.operacao_service = operacao_service

    def validate(self, dto: InterceptacaoUploadDTO):
        if dto.file is None:
            raise ValueError('file not found!')

        filename = dto.file.filename
        if filename is None:
            raise ValueError('filename not found!')

        if not self.upload_service.allowed_file(filename):
            raise ValueError('file extension not allowed!')

        if not self.operacao_service.hasOperacao(int(dto.operacao_id)):
            raise ValueError('operation id does not exist!')

    def start_upload(self, dto: InterceptacaoUploadDTO, job_id: str):
        """Cria a thread que executa o upload e retorna imediatamente"""
        # Lê o conteúdo do arquivo ainda no contexto da request
        file = dto.file
        content = file.read()
        file_buffer = BytesIO(content)
        file_size = int(len(content) / 1024)

        app = current_app._get_current_object()

        def process():
            with app.app_context():
                try:
                    set_progress(job_id, "Processando upload", 10)
                    start = time.time()

                    self.upload_service.save(
                        file_buffer=file_buffer,
                        file_size=file_size,
                        filename=file.filename,
                        operacao_id=dto.operacao_id,
                        job_id=job_id
                    )

                    duration = round(time.time() - start, 2)
                    logger.info(f"[UPLOAD] Finalizado em {duration} segundos")
                    set_progress(job_id, "Concluído", 100, erro=False, mensagem=None)

                except ValueError as e:
                    logger.warning(f"[UPLOAD] Erro de validação: {e}")
                    set_progress(job_id, "Erro de validação", 100, erro=True, mensagem=str(e))
                except Exception as e:
                    logger.exception("[UPLOAD] Erro interno no processamento")
                    set_progress(job_id, "Erro interno", 100, erro=True, mensagem="Erro interno no processamento")

        threading.Thread(target=process).start()