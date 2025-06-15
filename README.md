📸 AWS Lambda Image Resizer
Automatically resize images uploaded to an Amazon S3 bucket using an AWS Lambda function written in Python.

When an image is uploaded to the source bucket, the Lambda function:

Resizes it (e.g., to 128×128 pixels)

Saves it to a destination S3 bucket with a resized- prefix

🚀 How It Works
📤 Upload an image to the source S3 bucket

⚡ S3 triggers the Lambda function

🐍 Lambda function:

Downloads the image

Resizes it using Pillow

Uploads it to the destination S3 bucket

Adds the prefix resized- to the filename

🛠️ Technologies Used
🟨 AWS Lambda

📦 Amazon S3

🔐 IAM Roles & Policies

🐍 Python 3.9

🖼️ Pillow (via Lambda Layer)

📋 Setup Instructions
1️⃣ Create S3 Buckets
Source bucket: image-upload-source

Destination bucket: image-upload-resized

2️⃣ Create IAM Role for Lambda
Attach the following inline policy:

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
3️⃣ Create the Lambda Function
Runtime: Python 3.9

Memory: 512 MB

Timeout: 30 seconds

Role: Attach the IAM role created above

4️⃣ Add Pillow Layer
Use this Lambda Layer ARN for Pillow (region: eu-north-1):

arn:aws:lambda:eu-north-1:770693421928:layer:Klayers-p39-Pillow:9
Attach this resource-based policy to allow the Lambda function to access the layer:

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
📥 Upload function.zip to the Lambda function using the AWS Console.

6️⃣ Set Up S3 Trigger
Go to your source bucket

Navigate to Properties → Event notifications

Create a new event:

Event type: PUT

Destination: Your Lambda function

7️⃣ Allow S3 to Invoke Lambda
Add a resource-based policy to your Lambda function:

Go to: Configuration → Permissions → Add permissions

Select:

Principal: AWS Service → S3

Action: lambda:InvokeFunction

Source ARN: arn:aws:s3:::image-upload-source

✅ You're All Set!
Now whenever you upload an image to image-upload-source, 🎉 a resized version will automatically appear in image-upload-resized!
