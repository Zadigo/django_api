"""This module regroups a series of classes and utilities that can be useful
for interacting with AWS within Django (e.g. uploading items...)

Base
----

    There are three main classes:
        - AWS
        - QueryManager
        - TransferManager

    The two last classes are subclasses of AWS so you might want to use the latter
    directly as opposed to the main one.

Utilities
---------

    The utilities definitions are useful for doing common stuffs when dealing with
    AWS -; for instance creating a file name and path:

        - object_size_creator
        - aws_url_for
        - unique_path_creator

author: pendenquejohn@gmail.com
"""

import os
import secrets
from mimetypes import guess_extension, guess_type

import boto3

SETTINGS = {
    'url': 'https://s3.%s.amazonaws.com/%s/%s',

    'bucket_name': os.environ.get('AWS_BUCKET_NAME'),
    'region_name': os.environ.get('AWS_REGION_NAME'),

    'access_keys': {
        'secret_key': os.environ.get('AWS_SECRET_KEY'),
        'access_key': os.environ.get('AWS_ACCESS_KEY')
    }
}

def object_size_creator(image_or_path):
    """
    Create three different types of image sizes for the
    S3 bucket. The original one, small, medium and large.

    Creates a dictionnary of values such as:
        {
            original: file.txt, 
            small: file-small.txt, 
            medium: file-medium.txt, 
            large: file-large.txt
        }
    """
    name, extension = image_or_path.split('.', 1)
    images_size = {
        'original': image_or_path,
        'small': name + '-small',
        'medium': name + '-medium',
        'large': name + '-large'
    }

    for key, value in images_size.items():
        if key != 'original':
            images_size.update({key: value + '.' + extension})

    return images_size

def object_bucket_url(object_path, region=SETTINGS['region_name'], bucket=SETTINGS['bucket_name']):
    """
    Create a base url for an object that was previously
    created in a bucket in order to save it to a local
    database for example.
    
    The general settings `AWS_REGION`
    can be overriden with the `region` and so as the bucket

    `object_path` should be the relative path of the object
    in the bucket such as `folder/object.ext` or `folder/folder/object.ext`

    Example link
    ------------

        https://s3.eu-west-3.amazonaws.com/jobswebsite/banners/object.jpg
    """
    return f'https://s3.{region}.amazonaws.com/{bucket}/{object_path}'

def unique_path_creator(folder, filename, rename=False):
    """
    Create a unique path for an object to be stored
    in an AWS bucket. Returns a dictionnary with the
    object's new name, path and url.

    Parameters
    ----------

    `folder` is the folder to access within the bucket. You can
    also use a path such as path/to/

    `filename` is the name of the file

    `rename` allows you to rename the file to a random name

    Description
    -----------

        {
            'object_name': ['name', ('image/jpeg', None)], 
            'object_path': 'path/to/file.jpg',
            'object_url': 'https://s3...',
            'unique_entry': 'acc318515f364f1d37ecac456e6365bc1e4ae216'
        }

        unique_entry is the unique folder created in order to identify a set
        of files in your bucket
    """
    name, extension = filename.split('.', 1)

    unique_entry = secrets.token_hex(20)

    if rename:
        name = secrets.token_hex(10)
        extension = extension.lower()
    
    else:
        name = name.lower()
        extension = extension.lower()

    object_path = '%s/%s/%s.%s' % (folder, unique_entry, name, extension)
    # Create the objet's URL to save to a database for example
    # FIXME: Find a way to pass the bucket and the region
    object_url = object_bucket_url(object_path)
    
    return {'object_name': [name, guess_type(filename)], 'object_path': object_path, 
                'object_url': object_url, 'unique_entry': unique_entry}


class AWS:
    session = boto3.Session

    def create_session(self, access_key, secret_key, region_name):
        session = self.session(access_key, secret_key, region_name=region_name)
        return session

class QueryManager(AWS):
    def __init__(self, bucket_name, access_key, secret_key, region_name):
        # Use .resource() to perform actions from a
        # bucket standpoint eg. .filter(), .all()
        session = super().create_session(access_key, secret_key, region_name)
        resource = session.resource('s3')
        self.bucket = resource.Bucket(bucket_name)

        self.bucket_name = bucket_name
        self.region_name = region_name

    def list_bucket(self):
        """Lists the items withing a bucket
        """
        return [item for item in self.bucket.objects.all()]

    def list_folder(self, folder):
        """List the specific items of a folder

        Description
        -----------

            For example, return the folder ./test in a bucket:

                (
                    ('test/', 'item'), 
                    ('test/subfolder/to.jpg', 'item'), 
                    ...
                )
        """
        items = list((item.key, item.last_modified) for item in self.bucket.objects.filter(Prefix=folder))
        items.pop(0)
        return items

    def list_folder_urls(self, folder):
        """Get the specific items' links in a folder

        Description
        -----------

            [
                https://s3...,
                ...
            ]
        """
        items = self.list_folder(folder)
        for item in items:
            yield object_bucket_url(item[0], self.region_name, self.bucket_name)

class TransferManager(AWS):
    def __init__(self, bucket_name, access_key, secret_key, region_name):
        session = super().session(access_key, secret_key, region_name=region_name)
        self.client = session.client('s3')
        
        self.bucket_name = bucket_name
        self.region_name = region_name

    def upload(self, data, subfolder_path, contenttype, **params):
        """This is the overall definition used to upload objects to
        a given AWS bucket.

        Parameters
        ----------
            data: the content of the file to upload in bytes

            subfolder_path: is the subfolder to upload the file to

            contenttype: the content disposition of the file e.g. application/jpg
        """
        base_params = {
            'Bucket': self.bucket_name,
            'Key': subfolder_path,
            'Body': data,
            'ACL': 'public-read',
            'ContentType': contenttype,
            'CacheControl': 'max-age=24000'
        }
        if params:
            base_params.update(params)

        try:
            response = self.client.put_object(**base_params)
        except boto3.exceptions.S3TransferFailedError:
            print('[%s]: Upload failed. %s was not uploaded.' 
                    % (self.__class__.__name__, subfolder_path))
        else:
            return response
    
    def upload_from_local(self, file_to_upload, upload_to, model=None, request=None):
        """Uploads a file from a local path

        Parameters
        ----------

            file_to_upload: the absolute path of the file to upload

            upload_to: path in your AWS bucket in which to upload the file
            e.g. path/to/folder

            model: if you need to save items to a Django model after upload,
            then pass your model here
        """
        is_local_file = os.path.isfile(file_to_upload)
        if is_local_file:
            item_name = os.path.basename(file_to_upload)
            # Guess the type of the file for AWS
            # .. Transform to list to have better flexibility
            # as opposed to using a tuple
            contenttype = list(guess_type(file_to_upload))

            # HACK: If content type is none, we
            # have to find something here!
            if contenttype[0] is None:
                contenttype[0] = 'image/jpeg'

            with open(file_to_upload, 'rb') as f:
                data = f.read()
                # Create the unique path for the file
                # within the subfolder
                path = unique_path_creator(upload_to, item_name)
                response = self.upload(data, path['object_path'], contenttype[0])
            return {'key': path['unique_entry'], 'response': response}

    def local_to_existing(self, file_to_upload, aws_path):
        """Upload a file to an existing folder path. Note that the
        definition automatically guesses the name of the file.
        """
        is_local_file = os.path.isfile(file_to_upload)
        if is_local_file:
            item_name = os.path.basename(file_to_upload)
            # Guess the type of the file for AWS
            # .. Transform to list to have better flexibility
            # as opposed to using a tuple
            contenttype = list(guess_type(file_to_upload))

            # HACK: If content type is none, we
            # have to find something here!
            if contenttype[0] is None:
                contenttype[0] = 'image/jpeg'

            with open(file_to_upload, 'rb') as f:
                data = f.read()
                complete_path = aws_path + '/' + item_name
                response = self.upload(data, complete_path, contenttype[0])
                print('[AWS MANAGER] : File uploaded. (%s)' % complete_path)
            return response

    def delete_object(self, aws_path):        
        return self.client.delete_object(aws_path)

    # def upload_to_model(self, file_to_upload, model, **kwargs):
    #     if isinstance(model, type):
    #         obj = model.objects.create(**kwargs)
    #         return obj
    #     self.upload_from_local(file_to_upload, upload_to)
