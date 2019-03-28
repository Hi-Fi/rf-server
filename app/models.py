from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import relationship
from google.cloud import datastore
from datetime import datetime
import logging

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

datastore_client = datastore.Client(project="rf-server-dev")


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


def get_executions():
    query = datastore_client.query(kind='Execution')
    query.order = ['-scheduled']
    return list(query.fetch())
