import boto3
import config 
import json

def get_execution_details(execution_arn, tx_id):
    # Create a Step Functions client
    sfn = boto3.client('stepfunctions')
    # Describe the execution
    response = sfn.describe_execution(executionArn=execution_arn)

    # Access and print the input
    execution_input = json.loads(response['input'])
    execution_output = json.loads(response['output'])
    if tx_id==execution_input['transaction']['transaction_id']:
        return True
    else:
        return False
    


def get_sm_exec_info(tx_id):
    # Replace with your state machine ARN
    state_machine_arn = config.state_machine_arn

    # Create a Step Functions client
    client = boto3.client("stepfunctions", config.region)

    # List executions for the specified state machine
    response = client.list_executions(
        stateMachineArn=state_machine_arn,
    )

    # Print the execution details
    if "executions" in response:
        for execution in response["executions"]:
            print(f"Execution ARN: {execution['executionArn']}")
            if get_execution_details(execution['executionArn'], tx_id):
                return execution['executionArn']
    else:
        print("No executions found for this state machine.")

    # Handle pagination if more results are available
    if "nextToken" in response:
        next_token = response["nextToken"]
        while next_token:
            response = client.list_executions(
                stateMachineArn=state_machine_arn,
                nextToken=next_token,
            )
            if "executions" in response:
                for execution in response["executions"]:
                    print(f"Execution ARN: {execution['executionArn']}")
                    if get_execution_details(execution['executionArn'], tx_id):
                        return execution['executionArn']
            if "nextToken" in response:
                next_token = response["nextToken"]
            else:
                next_token = None


