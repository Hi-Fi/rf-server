from google.cloud import tasks_v2beta3
import json
from config import GAE_PROJECT

def create_execution_task(run_id, test_suite, *arguments):
    payload = {
        "run_id": run_id,
        "test_suite": test_suite,
        "variables": []
    }

    for argument in arguments:
        payload['variables'].append(argument)

    create_and_submit_task(payload, 'rf-execution', '/robot/execute')

def create_metrics_task(run_id):
    payload = {
        "run_id": run_id
    }

    create_and_submit_task(payload, 'rf-metrics', '/robot/generate/metrics')

def create_parsing_task(run_id):
    payload = {
        "run_id": run_id
    }

    create_and_submit_task(payload, 'rf-report', '/robot/generate/reports')




def create_and_submit_task(payload, queue, target):
    client = tasks_v2beta3.CloudTasksClient()
    project = GAE_PROJECT
    queue = 'rf-execution'
    location = 'europe-west1'

    # Construct the fully qualified queue name.
    parent = client.queue_path(project, location, queue)

    # Construct the request body.
    task = {
        'app_engine_http_request': {  # Specify the type of request.
            'http_method': 'POST',
            'relative_uri': target,
            'headers': {"Content-Type": "application/json"}
        }
    }

    # The API expects a payload of type bytes.
    converted_payload = json.dumps(payload).encode()

    # Add the payload to the request.
    task['app_engine_http_request']['body'] = converted_payload

    response = client.create_task(parent, task)

    print('Created task {}'.format(response.name))
