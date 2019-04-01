from google.cloud import storage


client = storage.Client()

bucket = client.get_bucket('rf-server-dev.appspot.com')


def upload_file(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def get_file(file_name):
    """Uploads a file to the bucket."""
    blob = bucket.blob(file_name)

    blob.download_to_filename('/tmp'+file_name)

    print('Blob {} downloaded to {}.'.format(
        file_name,
        '/tmp'+file_name))