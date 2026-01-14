
import json
from handlers.image_handler import handler

def test_save_metadata_success(mock_dynamodb, lambda_context):
    event = {
        "httpMethod": "POST",
        "path": "/images/metadata",
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "imageId": "123",
            "userId": "u1",
            "s3Key": "images/123.jpg"
        }),
        "isBase64Encoded": False
    }

    response = handler(event, lambda_context)

    assert response["statusCode"] in (200, 201)
    mock_dynamodb.put_item.assert_called_once()
