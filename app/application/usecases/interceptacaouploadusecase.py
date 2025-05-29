from app.application.dto.interceptacaouploaddto import InterceptacaoUploadDTO
from app.domain.services.uploadservice import UploadService
from app.domain.services.operacaoservice import OperacaoService


class InterceptacaoUploadUseCase:
    def __init__(self, upload_service: UploadService, operacao_service: OperacaoService):
        self.upload_service = upload_service
        self.operacao_service = operacao_service

    def execute(self, intercept_upload_dto: InterceptacaoUploadDTO) -> None:
        file = intercept_upload_dto.file
        operacao_id = intercept_upload_dto.operacao_id
        filename = file.filename
        if file:
            file.seek(0,2)
            file_size = int(file.tell()/1024)
            file.seek(0)
               
        if file is None:
            raise ValueError('file not found!')
        
        if filename is None:
            raise ValueError('filename not found!')
        
        if not self.upload_service.allowed_file(filename):
            raise ValueError('file extension not allowed!')
        
        if not self.operacao_service.hasOperacao(int(operacao_id)):
            raise ValueError('operation id does not exist!')
        
        self.upload_service.save(
            file_buffer=file.stream,
            file_size=file_size,
            filename=filename,
            operacao_id=operacao_id,
        )