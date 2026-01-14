
from src.handlers.image_handler import upload_image

def test_upload_image():
    event = {
        "body": '{"userId": "u1", "title": "test", "image": "abc"}'
    }
    response = upload_image(event, None)
    assert response["statusCode"] == 201
