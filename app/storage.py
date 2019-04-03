from google.cloud import storage
from pathlib import Path
from datetime import timedelta


client = storage.Client()

bucket = client.get_bucket('rf-server-dev.appspot.com')


def upload_file(run_id, file_name):
    """Uploads a file to the bucket."""
    blob = bucket.blob(run_id+'/'+file_name)

    blob.upload_from_filename('/tmp/'+run_id+'/'+file_name)

    print('File {} uploaded to {}.'.format(
        '/tmp/'+run_id+'/'+file_name,
        run_id+'/'+file_name))


def get_file(run_id, file_name):
    """Downloads a file from the bucket."""
    blob = bucket.blob(run_id+'/'+file_name)
    try:
        Path('/tmp/'+run_id).mkdir()
    except:
        pass
    target_file = '/tmp/'+run_id+'/'+file_name

    Path(target_file).touch()

    blob.download_to_filename(target_file)

    print('Blob {} downloaded to {}.'.format(
        file_name,
        target_file))


def get_signed_url(run_id, file_name, expiration=timedelta.min(1)):
    blob = bucket.blob(run_id+'/'+file_name)
    return blob.generate_signed_url(expiration)
