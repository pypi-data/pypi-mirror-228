from pathlib import Path
from typing import Union
import hashlib
import logging
import requests
import time

from aiopcli import utils

logger = logging.getLogger()

ENDPOINT = '/isapi/api/v1/artifacts'


def get_artifacts(ctx, digest: str = None):
    response = ctx.client.get(ENDPOINT, params={'digest': digest} if digest else None)
    return _handle_response(response)


def get(ctx, artifact_id: str):
    response = ctx.client.get(f'{ENDPOINT}/{artifact_id}')
    return _handle_response(response)


def post(ctx, files):
    response = ctx.client.post(ENDPOINT, files=files)
    return _handle_response(response)


def _handle_response(response: requests.models.Response):
    if not (200 <= response.status_code < 300):
        # TODO: raise useful exception
        raise ValueError(f"Failed to acquire resource '{ENDPOINT}': {response.content} \n"
                         f"Request failed with status code: {response.status_code}")
    return response.json()


def add(ctx, path: Union[str, Path], force: bool):
    logger.info(f"ARTIFACT '{path}'")
    path = Path(path)
    if not path.exists():
        raise ValueError(f"{path}: does not exist")
    if not path.is_file():
        raise ValueError(f"{path}: only regular files can be registered as artifacts.")

    response = None
    if not force:
        logging.info("  Computing hash...")

        hasher = hashlib.sha256()
        with path.open('rb') as fp:
            while data := fp.read(8096):
                hasher.update(data)
        digest = f'sha256:{hasher.hexdigest()}'

        logging.info(f"  Checking if artifact exists: {digest}")
        response = get_artifacts(ctx, digest=digest)
    if response:
        response = response[0]
        logger.info(f"  Already exists on server: {response['artifactId']}")
    else:
        logger.info(f"  Does not exist. Uploading '{path}'...")
        with utils.prepare_file(path) as file_:
            response = post(ctx, files=file_)
    return response


def wait(ctx, artifact_id, timeout=600, interval=1):
    tick = time.time()
    while True:
        if time.time() > tick + timeout:
            # TODO: error handling
            raise ValueError("Timed out.")
        response = get(ctx, artifact_id)
        if response['status'] == 'failed':
            # TODO: error handling
            raise ValueError(f"Artifact failed: {response}.")
        elif response['status'] == 'ready':
            return response
        time.sleep(interval)


def register_artifacts(ctx, force: bool = False, **kwargs):
    print('Uploading apiserver...')
    kwargs['apiServer'] = register_artifact(ctx, kwargs['apiServer'], force)
    logger.info(f"Uploaded apiServer artifactId: {kwargs['apiServer']}")
    if kwargs['inferenceServer']:
        print('Uploading inferenceserver...')
        kwargs['inferenceServer'] = register_artifact(ctx, kwargs['inferenceServer'], force)
        logger.info(f"Uploaded inferenceServer artifactId: {kwargs['inferenceServer']}")
    return kwargs


def register_artifact(ctx, image: str, force: bool):
    image = Path() / image
    artifact_id = add(ctx, path=image, force=force)['artifactId']
    wait(ctx, artifact_id)
    return artifact_id
