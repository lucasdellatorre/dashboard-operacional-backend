import pytest
from unittest.mock import Mock, patch
from flask import Flask
from io import BytesIO
from app.application.dto.interceptacaouploaddto import InterceptacaoUploadDTO
from app.application.usecases.interceptacaouploadusecase import InterceptacaoUploadUseCase


@pytest.fixture
def fake_app():
    app = Flask(__name__)
    with app.app_context():
        yield app


@pytest.fixture
def mock_upload_service():
    service = Mock()
    service.allowed_file.return_value = True
    return service


@pytest.fixture
def mock_operacao_service():
    service = Mock()
    service.hasOperacao.return_value = True
    return service


@pytest.fixture
def usecase(mock_upload_service, mock_operacao_service):
    return InterceptacaoUploadUseCase(mock_upload_service, mock_operacao_service)


def make_dto(filename="test.csv", content=b"example", operacaoId="1"):
    file = Mock()
    file.filename = filename
    file.read.return_value = content
    return InterceptacaoUploadDTO(file=file, operacaoId=operacaoId)


def test_validate_success(usecase):
    dto = make_dto()
    usecase.validate(dto)  # Should not raise any exception


def test_validate_file_none(usecase):
    dto = make_dto()
    dto.file = None
    with pytest.raises(ValueError, match="file not found!"):
        usecase.validate(dto)


def test_validate_filename_none(usecase):
    dto = make_dto()
    dto.file.filename = None
    with pytest.raises(ValueError, match="filename not found!"):
        usecase.validate(dto)


def test_validate_extension_not_allowed(usecase, mock_upload_service):
    dto = make_dto()
    mock_upload_service.allowed_file.return_value = False
    with pytest.raises(ValueError, match="file extension not allowed!"):
        usecase.validate(dto)


def test_validate_invalid_operacao(usecase, mock_operacao_service):
    dto = make_dto()
    mock_operacao_service.hasOperacao.return_value = False
    with pytest.raises(ValueError, match="operation id does not exist!"):
        usecase.validate(dto)


@patch("app.application.usecases.interceptacaouploadusecase.set_progress")
@patch("app.application.usecases.interceptacaouploadusecase.logger")
def test_start_upload_triggers_thread(mock_logger, mock_set_progress, usecase, fake_app):
    dto = make_dto()
    job_id = "1234"

    # Espera que o método upload_service.save seja chamado com os parâmetros corretos
    usecase.upload_service.save = Mock()

    with fake_app.app_context():
        usecase.start_upload(dto, job_id)

        # Dá um tempo pequeno para a thread começar
        import time
        time.sleep(0.1)

        usecase.upload_service.save.assert_called_once()
        mock_set_progress.assert_any_call(job_id, "Processando upload", 10)
