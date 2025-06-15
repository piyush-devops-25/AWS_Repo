📸 AWS Lambda Image Resizer
This project automatically resizes images uploaded to an Amazon S3 bucket using an AWS Lambda function written in Python. When a new image is uploaded to the source bucket, the Lambda function resizes it (e.g., to 128×128 pixels) and saves the result to a destination S3 bucket.

🚀 How It Works
An image is uploaded to the source S3 bucket.

An S3 event triggers a Lambda function.

The function:

Downloads the image

Resizes it using Pillow

Uploads it to a destination S3 bucket

The resized image is saved with a resized- prefix


🛠️ Technologies Used
AWS Lambda

Amazon S3

IAM Roles & Policies

Python 3.9

Pillow (via Lambda Layer)


📋 Setup Instructions
1️⃣ Create S3 Buckets
Create a source bucket (e.g., image-upload-source)

Create a destination bucket (e.g., image-upload-resized)

2️⃣ Create IAM Role for Lambda
Attach the following inline policy to a new IAM role:

{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::image-upload-source/*",
        "arn:aws:s3:::image-upload-resized/*"
      ]
    }
  ]
}
3️⃣ Create Lambda Function
Runtime: Python 3.9

Attach the IAM role created above

Set memory: 512 MB

Set timeout: 30 seconds

4️⃣ Add Pillow Layer
Add this Lambda layer ARN (for eu-north-1, adjust region if needed):

arn:aws:lambda:eu-north-1:770693421928:layer:Klayers-p39-Pillow:9
Also attach the following Lambda resource policy to allow the layer:

{
  "Effect": "Allow",
  "Action": "lambda:GetLayerVersion",
  "Resource": "arn:aws:lambda:eu-north-1:770693421928:layer:Klayers-p39-Pillow:9"
}

5️⃣ Upload Lambda Code
Create a function.zip with the following lambda_function.py inside:

import boto3
from PIL import Image
from io import BytesIO

s3 = boto3.client('s3')

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    destination_bucket = 'image-upload-resized'

    response = s3.get_object(Bucket=source_bucket, Key=key)
    image = Image.open(response['Body'])
    image = image.resize((128, 128))

    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)

    new_key = f"resized-{key}"
    s3.put_object(Bucket=destination_bucket, Key=new_key, Body=buffer, ContentType='image/jpeg')

    return {
        'statusCode': 200,
        'body': f'Resized image uploaded as {new_key}'
    }
Upload this ZIP file to your Lambda function via the AWS Console.

6️⃣ Set S3 Trigger
Go to your source S3 bucket:

Click Properties

Scroll to Event notifications

Create an event:

Trigger on PUT events

Destination: your Lambda function

7️⃣ Allow S3 to Invoke Lambda
Add this resource-based policy to your Lambda:

Go to Configuration > Permissions > Add permissions

Select:

Principal: AWS service → S3

Action: lambda:InvokeFunction

Source ARN: arn:aws:s3:::image-upload-source

✅ Done!
Now, when you upload an image to your source bucket, a resized version will automatically appear in the destination bucket!






