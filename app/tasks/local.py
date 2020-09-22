from app.execution import robot, report, metrics

def create_execution_task(run_id, test_suite, arguments):
    robot.execute_robot_run(run_id, test_suite, arguments)


def create_metrics_task(run_id):
    metrics.parse_rf_metrics(run_id)


def create_parsing_task(run_id):
    report.parse_run_output(run_id)
