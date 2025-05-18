from app.adapters.repositories.iprepository import IPRepository
from app.application.usecases.getallipusecase import GetAllIPUseCase
from app.domain.services.ipservice import IPService

class IPFactory:
    @staticmethod
    def get_all_IP():
        ip_repository = IPRepository()
        ip_service = IPService(ip_repository)
        return GetAllIPUseCase(ip_service)
