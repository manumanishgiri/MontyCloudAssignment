# Image Upload Service
Single Lambda · Proxy API · S3 · DynamoDB

## Architecture
API Gateway (Proxy)
AWS Lambda (Single router handler)
Amazon S3 (Image storage)
Amazon DynamoDB (Metadata storage)

## Folder Structure
.
├── template.yaml
├── samconfig.toml
├── README.md
├── src/handlers/image_handler.py
├── infra/docker-compose.yml
└── tests/tigerbase64.txt

## API Endpoints

### POST /images/upload-url
Generates a presigned S3 upload URL.

### PUT Upload Image
Use presigned URL:
curl -X PUT -H "Content-Type: image/jpeg" --data-binary "@cat.jpg" "<UPLOAD_URL>"

### POST /images/metadata
Stores metadata in DynamoDB.

### GET /images/{imageId}
Previously not working due to missing pathParameters parsing.
Now fixed: validates imageId and returns 404 if not found.

### DELETE /images/{imageId}
Previously only deleted DynamoDB record.
Now deletes S3 object and DynamoDB record.

## Deployment
sam build
sam deploy --guided
