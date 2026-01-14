# Image Upload Service

AWS SAM · API Gateway · Lambda · S3 · DynamoDB

A serverless image upload and management service built using AWS SAM with a single Lambda handler and REST API Gateway.

## Architecture

- API Gateway (REST)
- AWS Lambda (single handler)
- Amazon S3 (image storage)
- Amazon DynamoDB (metadata)
- AWS SAM (IaC)

## Project Structure

.
├── template.yaml
├── samconfig.toml
├── README.md
├── requirements.txt
├── src/
│   └── handlers/
│       └── image_handler.py
├── tests/
│   ├── conftest.py
│   ├── test_get_image.py
│   ├── test_delete_image.py
│   ├── test_save_metadata.py
│   └── test_invalid_route.py
└── test-results/ (generated, ignored)

## API Endpoints

### POST /images/upload-url

Generates a presigned S3 upload URL.

### PUT Upload Image

Use the presigned URL:
curl -X PUT -H "Content-Type: image/jpeg" --data-binary "@cat.jpg" "<UPLOAD_URL>"

### POST /images

Stores image metadata in DynamoDB.

### GET /images

List or search images.

#### Query Parameters

- imageId (optional)
- userId (optional)

At least one parameter is required.

Examples:
GET /images?userId=user-123
GET /images?imageId=abc-123

### GET /images/{imageId}

Returns metadata and a presigned download URL.

### DELETE /images/{imageId}

Deletes the image from S3 and metadata from DynamoDB.

## Testing

Install dependencies:
pip install -r requirements.txt

Run tests:
pytest

## 🧪 Local Development with LocalStack

This project supports local AWS service emulation using LocalStack for integration-style testing without accessing real AWS resources.

### Supported Services

- S3
- DynamoDB
- API Gateway (via SAM Local)

### When to Use LocalStack

- Validate S3 and DynamoDB behavior locally
- Debug integration flows
- Avoid AWS costs during development

### Start LocalStack

docker run -d \
  -p 4566:4566 \
  -e SERVICES=s3,dynamodb \
  localstack/localstack

### Configure Environment Variables

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-2
export AWS_ENDPOINT_URL=http://localhost:4566

### Notes

- Unit tests do not require LocalStack
- LocalStack is optional and not required for CI
- Recommended only for local integration validation

## Persist Test Results

pytest tests \
  -v \
  --junitxml=test-results/junit.xml \
  --html=test-results/report.html \
  --self-contained-html \
  --cov=src/handlers \
  --cov-report=html:test-results/coverage

## Deployment

sam build
sam deploy --guided

## Cleanup

sam delete
