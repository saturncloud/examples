import os
from urllib.parse import urlencode

import requests
import boto3


# this should be populated by the secrets manager
IMAGES = os.getenv("IMAGES")


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
    is_gpu = is_gpu.lower() == 'true'

    ecr_images = ecr.list_images(ecr_image_name)
    for image in ecr_images:
        image_uri = image['image_uri']
        image_tag = image['image_tag']
        url = f"{BASE_URL}/api/images"
        requests.post(url, json={
            image_uri: image_uri,
            version: image_tag,
            is_new_version: True,
            image: {
                is_external: True,
                is_gpu: is_gpu,
                visibility: 'account',
                image: saturn_image_name
            }
        })


def run():
    for line in IMAGES.split('\n'):
        ecr_image_name, saturn_image_name, is_gpu = line.spit(',')
        register(ecr_image_name, saturn_image_name, is_gpu)
