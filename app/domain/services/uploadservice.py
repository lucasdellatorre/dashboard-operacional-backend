from app.domain.repositories.planilharepository import IPlanilhaRepository

class UploadService:
    def __init__(self, planilha_repository: IPlanilhaRepository):
        self.repository = planilha_repository

    def save(self, file_buffer, file_size, filename, operacao_id, job_id=None):
        self.repository.save(
            file_buffer=file_buffer,
            file_size=file_size,
            filename=filename,
            operacao_id=operacao_id,
            job_id=job_id 
        )

    @staticmethod
    def allowed_file(filename):
        ALLOWED_EXTENSIONS = {'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt'}
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
