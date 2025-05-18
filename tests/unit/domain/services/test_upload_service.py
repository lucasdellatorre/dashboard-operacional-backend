import pytest
from unittest.mock import Mock
from app.domain.services.uploadservice import UploadService


def test_save_calls_repository_with_correct_arguments():
    # Arrange
    mock_repository = Mock()
    service = UploadService(planilha_repository=mock_repository)

    file_buffer = b"fake file data"
    file_size = 1234
    filename = "planilha.xlsx"
    operacao_id = 42

    # Act
    service.save(file_buffer, file_size, filename, operacao_id)

    # Assert
    mock_repository.save.assert_called_once_with(file_buffer, file_size, filename, operacao_id)


@pytest.mark.parametrize("filename,expected", [
    ("file.xls", True),
    ("file.xlsx", True),
    ("file.xlsm", True),
    ("file.xlsb", True),
    ("file.odf", True),
    ("file.ods", True),
    ("file.odt", True),
    ("file.csv", False),
    ("file.txt", False),
    ("file", False),
    ("file.docx", False),
])
def test_allowed_file_returns_expected_result(filename, expected):
    assert UploadService.allowed_file(filename) == expected
