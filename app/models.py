from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey 
from sqlalchemy.orm import relationship
from google.cloud import datastore
from datetime import datetime
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

datastore_client = datastore.Client()


def create_execution(run_id):
    entity = datastore.Entity(key=run_id)
    entity.update({
        'status': 'scheduled',
        'scheduled': datetime.now(),
        'modified': datetime.now()
    })
    datastore_client.put(entity)


def update_execution(run_id, status):
    entity = datastore_client.get(key=run_id)
    entity.update({
        'status': status,
        'modified': datetime.now()
    })
    datastore_client.put(entity)


def get_executions():
    query = datastore_client.query(kind='execution')
    query.order = ['-scheduled']
    return query.fetch()
