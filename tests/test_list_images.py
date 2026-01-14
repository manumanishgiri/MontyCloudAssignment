from handlers.image_handler import handler

def test_list_images_by_user(mock_dynamodb):
    mock_dynamodb.query.return_value = {
        "Items": [
            {"imageId": "1", "userId": "u1"},
            {"imageId": "2", "userId": "u1"}
        ]
    }

    event = {
        "httpMethod": "GET",
        "path": "/images",
        "queryStringParameters": {"userId": "u1"}
    }

    response = handler(event, None)
    assert response["statusCode"] == 200

def test_list_images_by_image_id(mock_dynamodb):
    mock_dynamodb.get_item.return_value = {
        "Item": {"imageId": "123"}
    }

    event = {
        "httpMethod": "GET",
        "path": "/images",
        "queryStringParameters": {"imageId": "123"}
    }

    response = handler(event, None)
    assert response["statusCode"] == 200

def test_list_images_no_filters():
    event = {
        "httpMethod": "GET",
        "path": "/images"
    }

    response = handler(event, None)
    assert response["statusCode"] == 400
