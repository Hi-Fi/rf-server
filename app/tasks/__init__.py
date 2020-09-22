from config import GAE_PROJECT

if GAE_PROJECT:
    import app.tasks.cloud_tasks as tasks
else:
    import app.tasks.local as tasks

def create_execution_task(run_id, test_suite, *arguments):
    tasks.create_execution_task(run_id, test_suite, arguments)


def create_metrics_task(run_id):
    tasks.create_metrics_task(run_id)


def create_parsing_task(run_id):
    tasks.create_parsing_task(run_id)
