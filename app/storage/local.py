from pathlib import Path
from datetime import timedelta
from os.path import isfile
import uuid
import os

from config import TEMP_DIR

def upload_file(run_id, file_name):
    """Write file to temp directory."""
    return 'file://'+TEMP_DIR + run_id + '/' + file_name


def list_files_in_directory(directory_name, delimiter=None):
    return os.listdir(os.getcwd() + '/' + directory_name)


def get_all_files_from_directory(directory_name):
    return os.getcwd() + '/' + directory_name


def get_file(run_id, file_name):
    """Downloads a file from the bucket."""
    target_file = TEMP_DIR + run_id + '/' + file_name



def get_signed_url(run_id, file_name, expiration=timedelta(minutes=1)):
    return "No need locally"
