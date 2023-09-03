import os
import glob
import fnmatch
import hashlib
import base64
import argparse

import google
import google.api_core.page_iterator # type:ignore
import google.cloud.storage.client # type: ignore
from google.cloud import storage # type: ignore

import typing
from typing import Union, Optional

import pprint
pp = pprint.PrettyPrinter(indent = 4)

def _get_args():
    parser = argparse.ArgumentParser(description = 'sync composer')
    parser.add_argument('--verbosity', '-v',  help = 'be verbose', type = int, default = 0)
    parser.add_argument('--project', '-p',  help = 'project name', required = True)
    parser.add_argument('--ignore', '-i',  help = 'ignore file')
    parser.add_argument('--bucket-name', '-b',  help = 'bucket-name', required = True)
    
    return  parser.parse_args()


def _get_ignore_patterns(
        path:Optional[typing.Union[str, os.PathLike]], 
        verbosity:int = 0) -> list:
    if path == None:
        return []
    assert isinstance(path, str) #needed for mypy :(
    with open(path, 'r') as read_obj:
        ignore = [x.strip() for x in read_obj.readlines()]
    if verbosity > 2:
        print('ignore list is')
        print(ignore)
    return ignore

def ignore_file(path:os.PathLike, patterns:list, verbosity:int = 0):
    for pat in patterns:
        if fnmatch.fnmatch(path, pat):
            return True
    return False

def walk_tree(the_dir:str, ignore:typing.List[str],
              verbosity:int = 0
              ) -> typing.Generator:
    for root, dirs, files in os.walk(the_dir):
        for filename in files:
            full_path  = os.path.join(root, filename)
            if ignore_file(path = full_path, patterns = ignore):
                continue
            yield full_path

def list_blobs(
        storage_client:google.cloud.storage.client.Client, 
        bucket_name:str, 
        prefix:str, 
        delimiter: Optional[str] = None,
        verbosity:int = 0) -> google.api_core.page_iterator.HTTPIterator :
    
    bucket = storage_client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix = prefix, delimiter=delimiter)
    return blobs

def get_gcs_hash(blob:google.cloud.storage.blob.Blob)-> str:
    return base64.b64decode(blob.md5_hash).hex()

def local_hash(path:str)-> str:
    return  hashlib.md5(open(path,'rb').read()).hexdigest()

def _get_local_d(directory: os.PathLike, 
                 ignore_patterns:typing.List[str],
                 verbosity:int = 0)-> dict:
    d = {}
    for x in walk_tree(the_dir = directory, ignore = ignore_patterns):
        local_as_hex = local_hash(path = x)
        d[x] = local_as_hex
    if verbosity > 2:
        print('local dict is')
        print(d)
    return d

def _get_storage_d(
        bucket_name:str, 
        storage_client:google.cloud.storage.client.Client,
        verbosity:int = 0)-> dict:
    d = {}
    g = list_blobs(storage_client = storage_client, bucket_name = bucket_name, prefix = 'dags')
    for i in g:
        gc_as_hex = get_gcs_hash(blob = i)
        d[i.name] = gc_as_hex
    if verbosity > 2:
        print('storage dict is')
        print(d)
    return d

def get_not_in_local_changed_local(
        storage_dict:dict, local_dict:dict, 
        ignore_patterns:list,
        verbosity:int = 0)->typing.Tuple[list, list]:
    not_found_local = []
    diff = []
    for i in storage_dict.keys():
        if local_dict.get(i) == None:
            if not ignore_file(path = i, patterns = ignore_patterns):
                not_found_local.append(i)
        elif local_dict.get(i) != storage_dict[i]:
                diff.append(i)
    return not_found_local, diff

def get_not_found_storage(storage_dict:dict, local_dict:dict) -> list:
    not_found = []
    for i in local_dict.keys():
        if not storage_dict.get(i):
            not_found.append(i)
    return not_found

def delete_from_bucket(storage_client,  bucket_name, list_of_paths, verbosity = 0):
    if len(list_of_paths) == 0:
        if verbosity> 1:
            print('No files to delete from bucket')
        return
    bucket = storage_client.bucket(bucket_name)
    for i in list_of_paths:
        blob = bucket.blob(i)
        blob.delete()
        if verbosity > 0:
            print(f'deleted  "{i}" from "{bucket_name}"')

def upload_files_to_bucket(
        storage_client:google.cloud.storage.client.Client, 
        bucket_name:str, 
        list_of_paths:list, 
        verbosity:int = 0):
    if len(list_of_paths) == 0:
        if verbosity > 1:
            print('No files to upload')
        return
    bucket = storage_client.bucket(bucket_name)
    for i in list_of_paths:
        blob = bucket.blob(i)
        blob.upload_from_filename(i)
        if verbosity:
            print(f'uploaded "{i}" to "{bucket_name}"')

def sync_bucket(
        directory:str,
        bucket_name:str, 
        project:str, 
        ignore_path:Optional[os.PathLike] = None, 
        verbosity:int = 0):
    ignore_patterns = _get_ignore_patterns(
            path = ignore_path,
            verbosity = verbosity)
    storage_client = storage.Client(project = project )
    storage_dict = _get_storage_d(
            bucket_name = bucket_name, 
            storage_client = storage_client,
            verbosity = verbosity)
    local_dict = _get_local_d(
            directory = directory, 
            ignore_patterns = ignore_patterns,
            verbosity = verbosity)
    not_found_local, diff = get_not_in_local_changed_local(
            storage_dict = storage_dict,
            local_dict = local_dict,
            ignore_patterns = ignore_patterns,
            verbosity = verbosity)
    not_found_storage = get_not_found_storage(storage_dict = storage_dict,
                                              local_dict = local_dict
                                              )
    delete_from_bucket(bucket_name = bucket_name, storage_client = storage_client, 
                       list_of_paths = not_found_local, 
                       verbosity = verbosity)
    upload_files_to_bucket(storage_client = storage_client,
                           bucket_name = bucket_name,
                           list_of_paths = diff + not_found_storage, 
                           verbosity = verbosity)
    return not_found_local, diff + not_found_storage

def main():
    args = _get_args()
    sync_bucket( bucket_name = args.bucket_name,
            verbosity = args.verbosity,
            project = args.project,
           ignore_path = args.ignore
            )


if __name__ == '__main__':
    main()
