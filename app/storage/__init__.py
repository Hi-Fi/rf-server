from config import GAE_PROJECT
from _datetime import timedelta

if GAE_PROJECT:
    import app.storage.google as storage
else:
    import app.storage.local as storage

def upload_file(run_id, file_name):
    return storage.upload_file(run_id, file_name)

def list_files_in_directory(directory_name, delimiter=None):
    return storage.list_files_in_directory(directory_name, delimiter)

def get_all_files_from_directory(directory_name):
    return storage.get_all_files_from_directory(directory_name)

def get_file(run_id, file_name):
    return storage.get_file(run_id, file_name)

def get_signed_url(run_id, file_name, expiration=timedelta(minutes=1)):
    return storage.get_signed_url(run_id, file_name, expiration=timedelta(minutes=1))