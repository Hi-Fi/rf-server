from google.cloud import datastore
from datetime import datetime
from config import GAE_PROJECT

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

datastore_client = datastore.Client(project=GAE_PROJECT)


def create_execution(run_id):
    key = datastore_client.key('Execution', run_id)
    entity = datastore.Entity(key=key)
    entity.update({
        'status': 'scheduled',
        'scheduled': datetime.now(),
        'modified': datetime.now()
    })
    datastore_client.put(entity)


def update_execution(run_id, status):
    key = datastore_client.key('Execution', run_id)
    entity = datastore_client.get(key=key)
    entity.update({
        'status': status,
        'modified': datetime.now()
    })
    datastore_client.put(entity)


def add_storage_link(run_id, link_name, link_url):
    key = datastore_client.key('Execution', run_id)
    entity = datastore_client.get(key=key)
    entity.update({
        link_name: link_url
    })
    datastore_client.put(entity)


def get_executions():
    query = datastore_client.query(kind='Execution')
    query.order = ['-scheduled']
    return list(query.fetch())
