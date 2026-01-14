
from handlers.image_handler import handler

def test_get_image_success(mock_dynamodb, mock_s3, lambda_context):
    mock_dynamodb.get_item.return_value = {
        "Item": {
            "imageId": "123",
            "fileName": "cat.jpg",
            "s3Key": "images/123.jpg",
            "s3Bucket": "monty.cloud.images.upload"
        }
    }

    mock_s3.generate_presigned_url.return_value = "https://signed-url"

    event = {
        "httpMethod": "GET",
        "path": "/images/123",
        "pathParameters": {"imageId": "123"}
    }

    response = handler(event, lambda_context)

    assert response["statusCode"] == 200
