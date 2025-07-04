import json
import boto3
from PIL import Image
from io import BytesIO
import os

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key    = event['Records'][0]['s3']['object']['key']

    # Download the image from S3
    response = s3.get_object(Bucket=bucket, Key=key)
    image_content = response['Body'].read()

    # Open the image
    image = Image.open(BytesIO(image_content))
    
    # Resize image
    image = image.resize((512, 512))  # Resize to 512X512
    
    # Save to bytes buffer
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    buffer.seek(0)
    
    # Upload to destination bucket
    destination_bucket = 'destination-buckett2025'
    new_key = f"resized-{key}"
    
    s3.put_object(
        Bucket=destination_bucket,
        Key=new_key,
        Body=buffer,
        ContentType='image/jpg'
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Resized image saved as {new_key}')
    }
