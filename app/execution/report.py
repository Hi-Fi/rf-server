import app.storage as storage
import app.models as models
from config import TEMP_DIR
from robot import rebot

def parse_run_output(run_id):
    run_output_dir = TEMP_DIR + run_id
    storage.get_file(run_id, 'output.xml')
    with open(run_output_dir+'/rebot.log', 'w') as stdout:
        rebot(TEMP_DIR+run_id+'/output.xml',
            outputdir=run_output_dir,
            stdout=stdout)
    storage.upload_file(run_id, "rebot.log")
    report_link = storage.upload_file(run_id, "report.html")
    log_link = storage.upload_file(run_id, "log.html")
    models.add_storage_link(run_id, "report", report_link)
    models.add_storage_link(run_id, "log", log_link)
    return "Parsed log files"
