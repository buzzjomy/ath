# Automate the loading of input files to S3
import random, string
import boto3
import os
import shutil
import json
from test_event_json import json_str

# Create a session
s3 = boto3.client('s3', 'us-east-1')

# Specify bucket and file information
bucket_name = 'intake-api-firelight-s3-713881800640'

suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
file_path = f'C:\\Users\\E406692\\Downloads\\4_15_2025\\4_15_2025'
file_names = [f'TA1_{suffix}.xml',
              f'TA1_{suffix}_Single.pdf']
orig_file_names = [f'TA1.xml',f'TA1_Single.pdf']

for i in range(2):
    shutil.copyfile(os.path.join(file_path, orig_file_names[i]), 
                    os.path.join(file_path, file_names[i]))

object_name = 'input_path/'  # Optional; if not specified, file_name is used

# Upload the file
body = '{\"Records\":[{\"eventVersion\":\"2.1\",\"eventSource\":\"aws:s3\",\"awsRegion\":\"us-east-1\",\"eventTime\":\"2025-02-07T10:53:14.326Z\",\"eventName\":\"ObjectCreated:Put\",\"userIdentity\":{\"principalId\":\"AWS:AROA2MNVLZ7AP74VVIX7I:intake-api-s3-presigned-function\"},\"requestParameters\":{\"sourceIPAddress\":\"4.188.244.164\"},\"responseElements\":{\"x-amz-request-id\":\"0FEHYH94A3RCFQR0\",\"x-amz-id-2\":\"zl0mBoxKuGxeMI8sIYli1royiFw6YLwjjY/rSrePKI+fqiIFXjnf9gOssrzF6CUX7rKR+JtLFlUcyaFrHFLU0zb4Y60w7TjneEBR+0mzVmM=\"},\"s3\":{\"s3SchemaVersion\":\"1.0\",\"configurationId\":\"NzNhZjYyMjgtM2Y3NS00MGI2LWE0ZGMtMWFlNWNmYTNkNjUw\",\"bucket\":{\"name\":\"intake-api-firelight-s3-713881800640\",\"ownerIdentity\":{\"principalId\":\"A2QRQVI3CQ4H3L\"},\"arn\":\"arn:aws:s3:::intake-api-firelight-s3-713881800640\"},\"object\":{\"key\":\"input_path/"+ file_names[0] + "\",\"size\":4681479,\"eTag\":\"98a1903142b9e775eea900f648e0f54e\",\"versionId\":\"SA.JmpR.9X6w_.NxC1VnKaYEkpn07mB1\",\"sequencer\":\"0067A5E61A287AAC70\"}}}]}'.replace('"','\\"')
input(body)
try:
    for file_name in file_names:
        output = s3.upload_file(os.path.join(file_path, file_name), bucket_name, object_name + file_name)
        print(output)
        print(f"File {file_name} uploaded to {bucket_name}/{object_name + file_name}")
except Exception as ex:
    print(ex)


# Trigger the function to run intake api
# f = open('test_event.json',)
# test_event_json = json.load(f)

# test_event_json['Records'][0]['body']=test_event_json['Records'][0]['body']\
#     .replace('"', '\\"').replace("^^TEST_FL_XML^^", 
#              file_names[0])
# test_event_json_str = str(test_event_json).replace('\'', '"')
# input(test_event_json_str)
test_event_json_str = json_str.replace("TTTT.xml", file_names[0])
input(test_event_json_str)

lambda_client = boto3.client('lambda', 'us-east-1')

response = lambda_client.invoke(
    FunctionName='intake-api-firelight-function',
    InvocationType='RequestResponse',  # Or 'Event' for asynchronous invocation
    Payload=str(test_event_json_str).encode('utf-8')  # JSON payload as bytes
)

print(response['StatusCode'])

# Go to S3 to get the flight_output.json
# Get the transaction id and then search for the state machine execution which has transaction

