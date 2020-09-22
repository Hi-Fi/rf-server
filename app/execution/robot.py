from config import TEMP_DIR, TEST_SUITE_DIR
from os import mkdir
from robot import run
from app import storage, tasks, models


def execute_robot_run(run_id, test_suite, variables):
    suite_dir = storage.get_all_files_from_directory(TEST_SUITE_DIR+test_suite)
    run_output_dir = TEMP_DIR + run_id
    try:
        mkdir(run_output_dir)
    except:
        pass
    variable_list = []
    for variable in variables:
        for key, value in variable.items():
            variable_list.append(key+":"+value)
    with open(run_output_dir+'/run.log', 'w') as logfile:
        run(suite_dir,
            outputdir=run_output_dir,
            report=None,
            log=None,
            stdout=logfile,
            stderr=logfile,
            variable=variable_list
        )
    models.update_execution(run_id=run_id, status="executed")
    print(f"Uploading output.xml to run {run_id}")
    storage.upload_file(run_id, 'output.xml')
    print(f"Uploading run.log to run {run_id}")
    storage.upload_file(run_id, 'run.log')
    print(f"creating metrics task to run {run_id}")
    tasks.create_metrics_task(run_id)
    print(f"creating parsing task to run {run_id}")
    tasks.create_parsing_task(run_id)
    return "Started robot execution"
