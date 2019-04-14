from google.cloud import storage
from pathlib import Path
from datetime import timedelta
from os.path import isfile

client = storage.Client()

bucket = client.get_bucket('rf-server-dev.appspot.com')


def upload_file(run_id, file_name):
    """Uploads a file to the bucket."""
    blob = bucket.blob(run_id+'/'+file_name)

    blob.upload_from_filename('/tmp/'+run_id+'/'+file_name)
    blob.make_public()

    print('File {} uploaded to {}.'.format(
        '/tmp/'+run_id+'/'+file_name,
        run_id+'/'+file_name))

    return blob.public_url


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
