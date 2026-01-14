import json
import boto3
import uuid
import os
from datetime import datetime
from boto3.dynamodb.conditions import Key

# -----------------------
# AWS Clients
# -----------------------
s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")

TABLE_NAME = os.environ.get("TABLE_NAME", "Images")
BUCKET_NAME = os.environ.get("BUCKET_NAME", "monty.cloud.images.upload")

table = dynamodb.Table(TABLE_NAME)

# -----------------------
# Helpers
# -----------------------
def response(code, body):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }

def json_body(event):
    if not event.get("body"):
        return {}
    return json.loads(event["body"])

# -----------------------
# Main Lambda Router
# -----------------------
def handler(event, context):
    method = event.get("httpMethod")
    path = event.get("path", "")
    params = event.get("pathParameters") or {}

    # POST /images/upload-url
    if method == "POST" and path == "/images/upload-url":
        return get_upload_url(event)

    # POST /images/metadata
    if method == "POST" and path == "/images/metadata":
        return save_metadata(event)

    # GET /images?userId=
    if method == "GET" and path == "/images":
        return list_images(event)

    # GET /images/{imageId}
    if method == "GET" and "imageId" in params:
        return get_image(event, params["imageId"])

    # DELETE /images/{imageId}
    if method == "DELETE" and "imageId" in params:
        return delete_image(event, params["imageId"])

    return response(404, {"error": "Route not found"})

# -----------------------
# Business Logic
# -----------------------

# 1️⃣ Generate pre-signed upload URL
def get_upload_url(event):
    body = json_body(event)

    user_id = body.get("userId")
    if not user_id:
        return response(400, {"error": "userId is required"})

    content_type = body.get("contentType", "image/jpeg")

    image_id = str(uuid.uuid4())
    s3_key = f"images/{user_id}/{image_id}.jpg"

    upload_url = s3.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET_NAME,
            "Key": s3_key,
            "ContentType": content_type
        },
        ExpiresIn=300
    )

    return response(200, {
        "imageId": image_id,
        "uploadUrl": upload_url,
        "s3Key": s3_key
    })

# 2️⃣ Save metadata (Instagram-style)
def save_metadata(event):
    body = json_body(event)

    required_fields = ["imageId", "userId", "s3Key"]
    for field in required_fields:
        if field not in body:
            return response(400, {"error": f"{field} is required"})

    item = {
        "imageId": body["imageId"],
        "userId": body["userId"],
        "s3Bucket": BUCKET_NAME,
        "s3Key": body["s3Key"],
        "createdAt": datetime.utcnow().isoformat()
    }

    # Optional metadata (fully flexible)
    optional_fields = [
        "caption",
        "tags",
        "location",
        "visibility",
        "mentions",
        "extraMetadata"
    ]

    for field in optional_fields:
        if field in body:
            item[field] = body[field]

    table.put_item(Item=item)

    return response(201, {
        "message": "Metadata stored successfully",
        "imageId": body["imageId"]
    })

# 3️⃣ List images by user
def list_images(event):
    params = event.get("queryStringParameters") or {}
    user_id = params.get("userId")

    if not user_id:
        return response(400, {"error": "userId is required"})

    result = table.scan(
        FilterExpression=Key("userId").eq(user_id)
    )

    return response(200, result.get("Items", []))

# 4️⃣ Get image (download URL)
def get_image(event, image_id):
    result = table.get_item(Key={"imageId": image_id})
    item = result.get("Item")

    if not item:
        return response(404, {"error": "Image not found"})

    download_url = s3.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": item["s3Bucket"],
            "Key": item["s3Key"]
        },
        ExpiresIn=3600
    )

    return response(200, {"downloadUrl": download_url})

# 5️⃣ Delete image
def delete_image(event, image_id):
    result = table.get_item(Key={"imageId": image_id})
    item = result.get("Item")

    if not item:
        return response(404, {"error": "Image not found"})

    s3.delete_object(
        Bucket=item["s3Bucket"],
        Key=item["s3Key"]
    )

    table.delete_item(Key={"imageId": image_id})

    return response(200, {"message": "Image deleted successfully"})
