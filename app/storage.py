from google.cloud import storage
from pathlib import Path
from datetime import timedelta
from os.path import isfile
import uuid
import os

from config import GAE_PROJECT

client = storage.Client()

bucket = client.get_bucket(f"{GAE_PROJECT}.appspot.com")


def upload_file(run_id, file_name):
    """Uploads a file to the bucket."""
    blob = bucket.blob(run_id+'/'+file_name)

    blob.upload_from_filename('/tmp/'+run_id+'/'+file_name)
    blob.make_public()

    print('File {} uploaded to {}.'.format(
        '/tmp/'+run_id+'/'+file_name,
        run_id+'/'+file_name))

    return blob.public_url

def list_files_in_directory(directory_name):
    return bucket.list_blobs(prefix=directory_name)

def get_all_files_from_directory(directory_name):
    temp_dir = str(uuid.uuid4())
    target_dir = '/tmp/' + temp_dir
    #Path.mkdir(target_dir, parents=True)
    os.makedirs(target_dir + '/' + directory_name, exist_ok=True)
    for file_to_download in list_files_in_directory(directory_name):
        target_file = target_dir + '/' + file_to_download.name
        if (target_file.endswith('/')):
            os.makedirs(target_file, exist_ok=True)
        else:
            blob = bucket.blob(file_to_download.name)
            blob.download_to_filename(target_file)
    return target_dir

def get_file(run_id, file_name):
    """Downloads a file from the bucket."""
    target_file = '/tmp/' + run_id + '/' + file_name
    if isfile(target_file):
        print("File {} already exits, not downloading again".format(target_file))
    else:
        blob = bucket.blob(run_id+'/'+file_name)
        try:
            Path('/tmp/'+run_id).mkdir()
        except:
            pass

        Path(target_file).touch()

        blob.download_to_filename(target_file)

        print('Blob {} downloaded to {}.'.format(
            file_name,
            target_file))


def get_signed_url(run_id, file_name, expiration=timedelta(minutes=1)):
    blob = bucket.blob(run_id+'/'+file_name)
    return blob.generate_signed_url(expiration)
