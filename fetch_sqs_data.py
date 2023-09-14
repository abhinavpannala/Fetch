import hashlib
import boto3
import json
from typing import Dict
from datetime import datetime
from utils.read_json import read
cred_file_path = "credentials.json"

sqs_config = read(cred_file_path, "SQS")
region_name = sqs_config['region_name']
endpoint = sqs_config['endpoint']
queue_name = sqs_config['queue_name']
aws_access_key_id = sqs_config['aws_access_key_id']
aws_secret_access_key = sqs_config['aws_secret_access_key']

def cipher(data : str) -> str:
	if data is None:
		return data
	return hashlib.sha512(data.encode("utf-8")).hexdigest()

def fetch_sqs_data():
		sqs = boto3.client('sqs', region_name, endpoint_url = endpoint, aws_access_key_id = aws_access_key_id,
								aws_secret_access_key = aws_secret_access_key)
		wait_time = 25
			
		payload = sqs.receive_message(
						QueueUrl = endpoint + '/' + queue_name,
						MaxNumberOfMessages = 1,
						WaitTimeSeconds = wait_time
					)
		if 'Messages' in payload and len(payload['Messages']) > 0: #Handling key errors
			for record in payload['Messages']:
				postgres_data_dict = {}
				postgres_data_dict['MessageId'] = record['MessageId']
				
				if 'Body' in record.keys():
					body = json.loads(record['Body'])
					for field in body:
						if field == 'ip': ## PII field
							postgres_data_dict['masked_ip'] = cipher(body[field])
						elif field == 'device_id': ## PII field
							postgres_data_dict['masked_device_id'] = cipher(body[field])
						elif field == 'app_version':
							postgres_data_dict[field] = int(body[field].split('.')[0])
						else: 
							postgres_data_dict[field] = body[field]		
					postgres_data_dict['create_date'] = datetime.now().strftime("%Y-%m-%d")
				#else: Add logs to mention that the body is absent
				receipt_handle = record['ReceiptHandle']
				sqs.delete_message(
						QueueUrl = endpoint + '/' + queue_name,
						ReceiptHandle = receipt_handle
						)
				yield postgres_data_dict
			