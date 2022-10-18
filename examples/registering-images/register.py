import os
from urllib.parse import urlencode
import json

import requests
import boto3

# Currently only works against the 2022.05.01 API.

# this should be populated by the secrets manager
IMAGE_SPEC = json.loads(os.getenv("IMAGE_SPEC"))
DRY_RUN = True


# this should be populated by Saturn.
BASE_URL = os.getenv("BASE_URL")
SATURN_TOKEN = os.getenv("SATURN_TOKEN")
saturn_headers = {"Authorization": f"token {SATURN_TOKEN}"}

def list_images(ecr_image_name: str):
    ecr = boto3.client('ecr')

    repository = ecr.describe_repositories(repositoryNames=[ecr_image_name])[
        'repositories'
    ][0]
    repository_uri = repository['repositoryUri']

    list_images = ecr.get_paginator("list_images")
    for page in list_images.paginate(RepositoryName=ecr_image_name):
        for image_id in page['imageIds']:
            tag = image_id.get('imageTag', None)
            if tag:
                yield dict(image_uri=f"{repository_uri}:{tag}", image_tag=tag)


def register(ecr_image_name: str, saturn_image_name: str, is_gpu: str):
    url = f"{BASE_URL}/api/images?page_size=-1"
    existing_images = requests.get(url).json()['images']
    existing_image_uris = set([x['image_uri'] for x in existing_images])
    is_gpu = is_gpu.lower() == 'true'
    url = f"{BASE_URL}/api/images"
    ecr_images = ecr.list_images(ecr_image_name)
    for image in ecr_images:
        image_uri = image['image_uri']
        if image_uri in existing_image_uris:
            continue
        image_tag = image['image_tag']
        payload = {
            image_uri: image_uri,
            version: image_tag,
            is_new_version: True,
            image: {
                is_external: True,
                is_gpu: is_gpu,
                visibility: 'account',
                image: saturn_image_name
            }
        }
        if DRY_RUN:
            print(f'REGISTER image_uri {payload}')
        else:
            requests.post(url, json=payload)


def run():
    for image_spec in IMAGE_SPEC:
        ecr_image_name = image_spec['ecr_image_name']
        saturn_image_name = image_spec['saturn_image_name']
        is_gpu = image_spec['is_gpu']
        register(ecr_image_name, saturn_image_name, is_gpu)
