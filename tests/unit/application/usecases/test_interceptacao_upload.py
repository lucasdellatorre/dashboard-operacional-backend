import io
import pytest
from unittest.mock import Mock
from app.application.dto.interceptacaouploaddto import InterceptacaoUploadDTO
from app.application.usecases.interceptacaouploadusecase import InterceptacaoUploadUseCase


class FakeFile:
    def __init__(self, filename, content=b"data"):
        self.filename = filename
        self.stream = io.BytesIO(content)
        self._file = self.stream
    def seek(self, offset, whence=0):
        return self.stream.seek(offset, whence)
    def tell(self):
        return self.stream.tell()


@pytest.fixture
def upload_service_mock():
    mock = Mock()
    # By default allow all files for simple tests
    mock.allowed_file.return_value = True
    return mock


@pytest.fixture
def operacao_service_mock():
    mock = Mock()
    mock.hasOperacao.return_value = True
    return mock


def test_execute_success(upload_service_mock, operacao_service_mock):
    # Arrange
    file = FakeFile(filename="file.xlsx", content=b"12345"*1024)  # 5KB data
    dto = Mock(spec=InterceptacaoUploadDTO)
    dto.file = file
    dto.operacao_id = "1"

    use_case = InterceptacaoUploadUseCase(upload_service_mock, operacao_service_mock)

    # Act
    use_case.execute(dto)

    # Assert
    upload_service_mock.allowed_file.assert_called_once_with("file.xlsx")
    operacao_service_mock.hasOperacao.assert_called_once_with(1)
    upload_service_mock.save.assert_called_once()

    args, kwargs = upload_service_mock.save.call_args
    assert kwargs['filename'] == "file.xlsx"
    assert kwargs['operacao_id'] == "1"
    # File size in KB, approx 5KB
    assert kwargs['file_size'] >= 5


def test_execute_raises_when_file_none(upload_service_mock, operacao_service_mock):
    dto = Mock(spec=InterceptacaoUploadDTO)
    dto.file = None
    dto.operacao_id = "1"
    use_case = InterceptacaoUploadUseCase(upload_service_mock, operacao_service_mock)

    with pytest.raises(ValueError, match="file not found!"):
        use_case.execute(dto)


def test_execute_raises_when_filename_none(upload_service_mock, operacao_service_mock):
    file = FakeFile(filename=None)
    dto = Mock(spec=InterceptacaoUploadDTO)
    dto.file = file
    dto.operacao_id = "1"
    use_case = InterceptacaoUploadUseCase(upload_service_mock, operacao_service_mock)

    with pytest.raises(ValueError, match="filename not found!"):
        use_case.execute(dto)


def test_execute_raises_when_file_extension_not_allowed(upload_service_mock, operacao_service_mock):
    file = FakeFile(filename="file.exe")
    dto = Mock(spec=InterceptacaoUploadDTO)
    dto.file = file
    dto.operacao_id = "1"
    upload_service_mock.allowed_file.return_value = False
    use_case = InterceptacaoUploadUseCase(upload_service_mock, operacao_service_mock)

    with pytest.raises(ValueError, match="file extension not allowed!"):
        use_case.execute(dto)


def test_execute_raises_when_operacao_id_not_exist(upload_service_mock, operacao_service_mock):
    file = FakeFile(filename="file.xlsx")
    dto = Mock(spec=InterceptacaoUploadDTO)
    dto.file = file
    dto.operacao_id = "999"
    operacao_service_mock.hasOperacao.return_value = False
    use_case = InterceptacaoUploadUseCase(upload_service_mock, operacao_service_mock)

    with pytest.raises(ValueError, match="operation id does not exist!"):
        use_case.execute(dto)
