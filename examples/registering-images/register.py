import os
from typing import Dict, Optional
from urllib.parse import urlencode
import json
import click
import time
from datetime import timedelta

import requests
import boto3


# this should be populated by the secrets manager
with open("/home/jovyan/image_spec.json") as f:
    IMAGE_SPEC = json.load(f)


DRY_RUN = os.getenv('DRY_RUN', 'TRUE').lower() == 'true'


# this should be populated by Saturn.
BASE_URL = os.getenv("BASE_URL")
SATURN_TOKEN = os.getenv("SATURN_TOKEN")
saturn_headers = {"Authorization": f"token {SATURN_TOKEN}"}
SATURN_USERNAME = os.getenv("SATURN_USERNAME")


def list_images(ecr_image_name: str):
    ecr = boto3.client('ecr')

    repository = ecr.describe_repositories(repositoryNames=[ecr_image_name])[
        'repositories'
    ][0]
    repository_uri = repository['repositoryUri']

    list_images = ecr.get_paginator("list_images")
    for page in list_images.paginate(repositoryName=ecr_image_name):
        for image_id in page['imageIds']:
            tag = image_id.get('imageTag', None)
            if tag:
                yield dict(image_uri=f"{repository_uri}:{tag}", image_tag=tag)


def make_url(path: str, queries: Optional[Dict[str, str]] = None) -> str:
    if queries:
        return f"{BASE_URL}/{path}?" + urlencode(queries)
    else:
        return f"{BASE_URL}/{path}"



def register(image_uri: str, version: str, saturn_image_name: str, dry_run: bool = False):
    q = f"owner:{SATURN_USERNAME} name:{saturn_image_name}"
    url = make_url("api/images", dict(q=q, page_size="-1"))
    images = requests.get(url, headers=saturn_headers).json()
    images = [x for x in images['images'] if x['name'] == saturn_image_name]
    if not images:
        raise ValueError(f'no image found for {q}')
    elif len(images) > 1:
        raise ValueError(f'multiple images found for {q}')
    image = images[0]
    image_id = image['id']

    q = f"version:{version}"
    url = make_url(f"api/images/{image_id}/tags", dict(q=q, page_size="-1"))

    tags = requests.get(url, headers=saturn_headers).json()['image_tags']
    if image_uri in [x['image_uri'] for x in tags]:
        print(f'found {image_uri}')
        return

    print(f"REGISTER {image_uri} {image}")
    if not dry_run:
        requests.post(url, json={'image_uri': image_uri}, headers=saturn_headers)


def register_all(ecr_image_name: str, saturn_image_name: str):
    ecr_images = list_images(ecr_image_name)
    for image in ecr_images:
        image_uri = image['image_uri']
        image_tag = image['image_tag']
        import time
        time.sleep(0.5)
        register(image_uri, image_tag, saturn_image_name, dry_run=DRY_RUN)


def sync():
    for image_spec in IMAGE_SPEC:
        ecr_image_name = image_spec['ecr_image_name']
        saturn_image_name = image_spec['saturn_image_name']
        register_all(ecr_image_name, saturn_image_name)


@click.group()
def cli():
    pass


@cli.command()
def run_once():
    sync()


@cli.command()
def run():
    while True:
        sync()
        time.sleep(10*60)


if __name__ == "__main__":
    cli()
