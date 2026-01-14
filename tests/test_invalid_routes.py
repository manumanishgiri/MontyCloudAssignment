
from handlers.image_handler import handler

def test_invalid_route(lambda_context):
    event = {
        "httpMethod": "GET",
        "path": "/unknown/path"
    }

    response = handler(event, lambda_context)

    assert response["statusCode"] in (400, 404)
