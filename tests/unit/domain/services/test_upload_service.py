import pytest
from unittest.mock import Mock
from app.domain.services.uploadservice import UploadService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def service(mock_repository):
    return UploadService(mock_repository)


def test_save_calls_repository_with_correct_arguments(service, mock_repository):
    # Arrange
    file_buffer = b"some binary content"
    file_size = 1024
    filename = "planilha.xlsx"
    operacao_id = "123"
    job_id = "job-456"

    # Act
    service.save(file_buffer, file_size, filename, operacao_id, job_id)

    # Assert
    mock_repository.save.assert_called_once_with(
        file_buffer=file_buffer,
        file_size=file_size,
        filename=filename,
        operacao_id=operacao_id,
        job_id=job_id
    )


@pytest.mark.parametrize("filename,expected", [
    ("planilha.xlsx", True),
    ("relatorio.xlsm", True),
    ("dados.ods", True),
    ("documento.odt", True),
    ("imagem.png", False),
    ("texto.txt", False),
    ("", False),
    (None, False),
    ("arquivo_sem_extensao", False),
])
def test_allowed_file(filename, expected):
    result = UploadService.allowed_file(filename if filename is not None else "")
    assert result == expected
