import types
import app.storage as storage
import app.models as models
from robotframework_metrics import robotmetrics
from os import listdir
from config import TEMP_DIR

def parse_rf_metrics(run_id):
    storage.get_file(run_id, 'output.xml')
    opts = types.SimpleNamespace()
    opts.path = TEMP_DIR+run_id+'/'
    opts.output = "output.xml"
    opts.log_name = "log.html"
    opts.report_name = "report.html"
    opts.ignoretype = robotmetrics.IGNORE_TYPES
    opts.ignore = robotmetrics.IGNORE_LIBRARIES
    opts.logo = "https://i.ibb.co/9qBkwDF/Testing-Fox-Logo.png"
    robotmetrics.generate_report(opts)
    metrics_file = ""
    for generated_file in listdir(opts.path):
        if (generated_file.startswith("metrics")):
            metrics_file = generated_file

    metrics_link = storage.upload_file(run_id, metrics_file)
    models.add_storage_link(run_id, "metrics", metrics_link)
    return "Generated RF metrics"