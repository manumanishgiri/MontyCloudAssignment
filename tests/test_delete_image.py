
from handlers.image_handler import handler

def test_delete_image_success(mock_dynamodb, mock_s3, lambda_context):
    mock_dynamodb.get_item.return_value = {
        "Item": {
            "imageId": "123",
            "s3Key": "images/123.jpg",
            "s3Bucket": "monty.cloud.images.upload"
        }
    }

    event = {
        "httpMethod": "DELETE",
        "path": "/images/123",
        "pathParameters": {"imageId": "123"}
    }

    response = handler(event, lambda_context)

    assert response["statusCode"] == 200
    mock_s3.delete_object.assert_called_once()
    mock_dynamodb.delete_item.assert_called_once()
