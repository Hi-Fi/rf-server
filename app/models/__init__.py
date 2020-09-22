from datetime import datetime
from config import GAE_PROJECT

if GAE_PROJECT:
    import app.models.datastore as models
else:
    import app.models.local as models


def create_execution(run_id):
    models.create_execution(run_id)


def update_execution(run_id, status):
    models.update_execution(run_id, status)


def add_storage_link(run_id, link_name, link_url):
    models.add_storage_link(run_id, link_name, link_url)

def get_executions():
    return models.get_executions()
