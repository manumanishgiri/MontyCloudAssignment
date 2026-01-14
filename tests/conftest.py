import sys
import os
import pytest
from unittest.mock import MagicMock

# --- FIX AWS REGION ERROR ---
os.environ["AWS_DEFAULT_REGION"] = "us-east-2"
os.environ["AWS_REGION"] = "us-east-2"

# Fix imports for pytest
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(ROOT_DIR, "src")
sys.path.insert(0, SRC_DIR)


@pytest.fixture
def lambda_context():
    class LambdaContext:
        aws_request_id = "test-request-id"
        function_name = "image-handler"
    return LambdaContext()


@pytest.fixture
def mock_dynamodb(mocker):
    mock_table = MagicMock()
    mocker.patch("handlers.image_handler.table", mock_table)
    return mock_table


@pytest.fixture
def mock_s3(mocker):
    mock_s3 = MagicMock()
    mocker.patch("handlers.image_handler.s3", mock_s3)
    return mock_s3
