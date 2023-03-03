import json
import hashlib
import psycopg2
import boto3
import datetime

# Connect to the AWS SQS queue
sqs = boto3.client("sqs", endpoint_url="http://localhost:4566/_aws/sqs/messages", region_name="us-east-1")
queue_url = sqs.get_queue_url(QueueName='login-queue')['QueueUrl']

# Connect to the Postgres database
conn = psycopg2.connect(host='localhost', port='5432', dbname='user_logins', user='postgres', password='yash1712')
cur = conn.cursor()

# Receive messages from the SQS queue
while True:
    
    response = sqs.receive_message(QueueUrl=queue_url)
    if 'Messages' not in response:
        break
    for message in response['Messages']:
        try:
            # Parse the JSON data
            data = message
            attributes = json.loads(data['Body'])
            # Mask PII data
            data['masked_device_id'] = hashlib.sha256(attributes['device_id'].encode()).hexdigest()
            data['masked_ip'] = hashlib.sha256(attributes['ip'].encode()).hexdigest()
            del attributes['device_id']
            del attributes['ip']
            print(data)
            # Insert data into the Postgres table
            cur.execute(
                "INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version, create_date) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                (attributes['user_id'], attributes['device_type'], data['masked_ip'], data['masked_device_id'], attributes['locale'], int(attributes['app_version'].replace('.','')), datetime.datetime.now())
            )
            conn.commit()
            print("Successfully processed SQS message.")
            # Delete the message from the SQS queue
            # sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
        except Exception as e:
            print(f"Failed to process message: {e}")

cur.close()
conn.close()

