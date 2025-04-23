from deepdiff import DeepDiff
import random, string
import boto3
import os
import shutil
import json
from test_event_json import json_str
import config
import sm

suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
test_file_names = [f'TA1_{suffix}.xml',
                f'TA1_{suffix}_Single.pdf']

def upload_fl_xml_to_s3():
    # Create a session
    s3 = boto3.client('s3', config.region)

    # Automate the loading of input files to S3
    # Specify bucket and file information
    firelight_bucket_name = config.firelight_bucket_name

   
    input_file_path = config.input_file_path
    
    orig_file_names = config.orig_file_names

    for i in range(2):
        shutil.copyfile(os.path.join(input_file_path, orig_file_names[i]), 
                        os.path.join(input_file_path, test_file_names[i]))

    object_name = 'input_path/'  # Optional; if not specified, file_name is used

    # Upload the file
    try:
        for file_name in test_file_names:
            output = s3.upload_file(os.path.join(input_file_path, file_name), firelight_bucket_name, object_name + file_name)
            print(f"File {file_name} uploaded to {firelight_bucket_name}/{object_name + file_name}")
    except Exception as ex:
        print(ex)


def trigger_intake():
    # Trigger the function to run intake api
    test_event_json_str = json_str.replace("TTTT.xml", test_file_names[0])

    lambda_client = boto3.client('lambda', config.region)

    response = lambda_client.invoke(
        FunctionName=config.firelight_lambda_func,
        InvocationType='RequestResponse',  # Or 'Event' for asynchronous invocation
        Payload=str(test_event_json_str).encode('utf-8')  # JSON payload as bytes
    )

    print(response['StatusCode'])
    print('RequestId ' + response['ResponseMetadata']['RequestId'])
    return response

def get_flight_json(response):
    # Go to S3 to get the flight_output.json
    hyperscience_bucket_name = config.hyperscience_bucket_name
    object_key = f'test14/{response['ResponseMetadata']['RequestId']}/flight_output.json'       
    try:
        s3 = boto3.client('s3', config.region)
        response = s3.get_object(Bucket=hyperscience_bucket_name, Key=object_key)
        content = response['Body'].read()
        actual_content = content.decode('utf-8') 
        actual_content = json.loads(actual_content)
        tx_id = actual_content['transaction']['transaction_id']
        with open("flight_output.json", "w") as f:
            f.write(str(actual_content))
    except Exception as e:
        print(f"Error retrieving object: {e}")
    return [actual_content, tx_id]

def compare_flight_vs_expected(actual_content):
    #Compare the flight output with the expected output
    with open(config.expected_flight_json_file, "r") as f:
        expected_content = json.load(f)
    dd_out = DeepDiff(actual_content, 
                    expected_content, 
                    ignore_order=False, 
                    exclude_paths=["root['transaction']['transaction_id']"],
                    exclude_regex_paths=[r"root\['annuitant'\]\['address'\]\[\d+\]\['item_id'\]"])

    print(dd_out)


upload_fl_xml_to_s3()
response = trigger_intake()
actual_content, tx_id = get_flight_json(response)
print(tx_id)
compare_flight_vs_expected(actual_content)


# Get the transaction id from flight json and 
# then search for the state machine execution which has transaction id
# print(sm.get_sm_exec_info(tx_id))