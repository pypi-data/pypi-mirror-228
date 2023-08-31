from pathlib import Path
from typing import Dict, List, Literal, Optional
import http
import json
import logging
import re
import sys

import atomicwrites
import click
import pydantic
import requests
import toml

from aiopcli import artifacts, custom_image, utils

LogLevel = Literal['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']
DEFAULT_LOG_LEVEL = 'WARNING'
HOST_REGEX = r'^https?://'
REF_REGEX = '^[-_a-zA-Z][-_a-zA-Z0-9]*$'

logger = logging.getLogger()


@click.group('aiopcli')
@click.option('-p', '--profile')
@click.option('-H', '--host')
@click.option('-k', '--apikey')
@click.option('-v', '--verbose', count=True)
@click.pass_context
def cli(ctx, profile, host, apikey, verbose):
    log_level = {0: None, 1: 'INFO'}.get(verbose, 'DEBUG')
    config, config_path, config_file = _load_config(profile, host, apikey, log_level=log_level)
    if not config.apikey:
        logging.error("API key must be set")
        exit(1)
    ctx.obj = Context(
        client=Client(host=config.host, apikey=config.apikey),
        config_path=config_path, config_file=config_file
    )


@cli.result_callback()
def process_result(status, **kwargs):
    sys.exit(status)


@cli.command
@click.option('-s', '--servable', required=True)
@click.option('-t', '--tag')
@click.option('-p', '--server-plan', required=True,
              type=click.Choice(['basic', 'standard', 'gpu_basic']))
@click.option('-c', '--capacity', type=int, default=1)
@click.option('-l', '--auto-scaling-limit', type=int)
@click.pass_obj
def create(ctx, tag, servable, server_plan, capacity, auto_scaling_limit):
    if ctx.get_env(tag):
        raise ValueError(f"Name '{tag}' is already in use")
    request = {
        'servable_id': servable,
        'server_plan': server_plan,
        'desired_capacity': capacity,
        'auto_scaling_enabled': auto_scaling_limit is not None,
    }
    if auto_scaling_limit:
        request['auto_scaling_max_replicas'] = auto_scaling_limit
    response = ctx.client.post('/api/v1/create_inference_env', json=request)
    if 200 <= response.status_code < 300:
        # FIXME: move error check code once the status code changes
        result = response.json()
        if result['result'] != 0:
            raise ValueError(f"Failed to create env: {result['msg']}")
        ctx.add_env(env_id=result['env_id'], tag=tag)
    return _handle_response(response)


@cli.group
def add():
    pass


def _parse_server(s):
    if not re.search(r'\.(t|tar\.)gz$', s):
        raise ValueError(f'Custom image file {s} must be of type .tgz or .tar.gz')
    return s


@add.command('server')
@click.option('-n', '--name', required=True)
@click.option('--api-server', 'apiServer', type=_parse_server, required=True)
@click.option('--inference-server', 'inferenceServer', type=_parse_server, default=None)
@click.option('-p', '--api-port', 'port', type=int, default=8080)
@click.option('-m', '--metrics-port', 'metricsPort', type=int, default=None)
@click.option('-s', '--shared-memory-requirement', 'sharedMemoryRequirement', default='0m')
@click.option('-t', '--inference-type', 'inferenceType',
              type=click.Choice(['gpu', 'cpu', 'auto']), default='auto')
@click.option('-i', '--inference-server-type', 'inferenceServerType',
              type=click.Choice(['tritonserver', 'other']), default='tritonserver')
@click.option('-l', '--liveness-endpoint', 'liveness', default=None)
@click.option('-r', '--readiness-endpoint', 'readiness', default=None)
@click.option('-f', '--force', is_flag=True)
@click.pass_obj
def add_custom(ctx, force, **kwargs):
    # TODO: error handling
    kwargs = artifacts.register_artifacts(ctx, force=force, **kwargs)
    spec = custom_image.parse(**kwargs)
    # TODO: error handling
    response = ctx.client.post('/isapi/api/v1/servables', json=spec.dict(exclude_none=True))
    return _handle_response(response)


@cli.command
@click.argument('env')
@click.option('-s', '--servable')
@click.option('-p', '--server-plan',
              type=click.Choice(['basic', 'standard', 'gpu_basic']))
@click.option('-c', '--capacity', type=int, default=1)
@click.option('--auto-scale', type=click.Choice(['true', 'false']))
@click.option('-l', '--auto-scaling-limit', type=int)
@click.pass_obj
def update(ctx, env, servable, server_plan, capacity, auto_scale, auto_scaling_limit):
    env_ = ctx.get_env(env)
    if env_ is None:
        raise ValueError(f"Unknown env {env}")

    # get current settings for this env
    response = ctx.client.get(f'/api/v1/env/{env_.id}/status')
    if response.status_code != 200:
        return _handle_response(response)
    request = {
        k: v for k, v in response.json().items() if k in (
            'env_id', 'servable_id', 'server_plan', 'desired_capacity', 
            'auto_scaling_enabled', 'auto_scaling_max_replicas',
        )
    }

    # update with inputs
    auto_scale = {'true': True, 'false': False, None: None}[auto_scale]
    if servable is not None:
        request['servable_id'] = servable
    if server_plan is not None:
        request['server_plan'] = server_plan
    if capacity is not None:
        request['desired_capacity'] = capacity
    if auto_scaling_limit is not None:
        if auto_scale is False:
            raise ValueError("Cannot disable auto scaling while setting limit")
        request['auto_scaling_max_replicas'] = auto_scaling_limit
        request['auto_scaling_enabled'] = auto_scale
    elif auto_scale is not None:
        request['auto_scaling_enabled'] = auto_scale

    response = ctx.client.post('/api/v1/update_inference_env', json=request)

    return _handle_response(response)


@cli.command
@click.argument('env')
@click.pass_obj
def delete(ctx, env):
    env_ = ctx.get_env(env)
    if not env_:
        raise ValueError(f"No such tag: '{env}'")
    response = ctx.client.post('/api/v1/delete_inference_env', json={'env_id': env_.id})

    # FIXME: once an error code is returned properly, rewrite this
    exit_code = 1
    if 200 <= response.status_code < 300:
        result = response.json()
        exit_code = result['result']
    if exit_code == 0:
        ctx.delete_env(env_.id)

    # return _handle_response(response)
    _handle_response(response)
    return exit_code


@cli.command
@click.argument('env', required=False)
@click.pass_obj
def status(ctx, env):
    status = 0
    if env:
        envs = [ctx.get_env(env)]
        if not envs[0]:
            raise ValueError(f"No such env: '{env}'")
    else:
        envs = ctx.get_envs()
    if envs:
        for env_ in envs:
            response = ctx.client.get(f'/api/v1/env/{env_.id}/status')
            if env_.tag and response.status_code == 200:
                print(f"{env_.tag}: ", end='')
            status |= _handle_response(response)
    else:
        print("No known envs.", file=sys.stderr)
    return status


@cli.command
@click.argument('env')
@click.option('-e', '--endpoint')
@click.option('-F', '--form', 'fields', multiple=True)
@click.option('-d', '--data')
@click.pass_obj
def predict(ctx, env, endpoint, fields, data):
    env_ = ctx.get_env(env)
    if not env_:
        raise ValueError(f"No such env: '{env}'")
    path = f'/api/v1/env/{env_.id}/predict'
    if endpoint:
        path = _url_join(path, endpoint)
    with utils.prepare_files(fields) as files:
        response = ctx.client.post(path, files=files, data=data)
    _handle_response(response)


@cli.command
@click.argument('env_id')
@click.argument('tag')
@click.pass_obj
def tag(ctx, *, env_id, tag):
    env_ = ctx.get_env(tag)
    if env_:
        if env_id == env_.id:
            logging.info("Nothing changed.")
            return 0
        else:
            logging.warning("Tag already exists, removing.")
            env_.tag = None
    env_ = ctx.get_env(env_id)
    if env_:
        env_.tag = tag
        logging.info(f"Tagged known env {env_id} as '{tag}'")
    else:
        response = ctx.client.get(f'/api/v1/env/{env_id}/status')
        if response.status_code == 403:
            raise ValueError("No such env exists")
        ctx.add_env(env_id=env_id, tag=tag)
        logging.info(f"Tagged new env {env_id} as '{tag}'")
    ctx.write_config()

    return 0


@cli.command
@click.pass_obj
def list(ctx):
    envs = ctx.get_envs()
    if envs:
        for env in envs:
            if env.tag:
                print(f"{env.id:5d} <- {env.tag}", file=sys.stderr)
            else:
                print(f"{env.id}", file=sys.stderr)


def _handle_response(response):
    status = 0
    if response.status_code >= 300:
        status_tag = http.HTTPStatus(response.status_code).phrase
        print(f"Error: {response.status_code} {status_tag}", file=sys.stderr)
        if response.content:
            print(response.content.decode(), file=sys.stderr)
        status = 1
    else:
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    return status


#
# Settings management
#

class EnvConfig(pydantic.BaseSettings):
    config: Path = '~/.aiop'
    profile: str = None
    host: str = None
    apikey: str = None
    log_level: LogLevel = None

    class Config:
        env_prefix = 'aiop_'


class Config(pydantic.BaseModel):
    host: str = pydantic.Field(None, regex=HOST_REGEX)
    apikey: str = None
    log_level: LogLevel = None


class Env(pydantic.BaseModel):
    id: int
    tag: Optional[str] = pydantic.Field(None, regex=REF_REGEX)


class ConfigFile(Config):
    default: str = None
    profiles: Dict[str, Config] = {}
    envs: List[Env] = []


def _load_config(profile=None, host=None, apikey=None, log_level=None):
    env = EnvConfig()
    config_path = env.config.expanduser()
    # allow initial log level to be set by environment variable
    logger.setLevel(log_level or env.log_level or DEFAULT_LOG_LEVEL)

    config = Config(host='https://aiops.inside.ai')

    if config_path.is_file():
        logging.info(f"Loading config file '{config_path}'")
        # base level configs are defaults and are applied first
        fields = toml.loads(config_path.read_text())
        config_file = ConfigFile.parse_obj(fields)

        config = _merge(config, config_file)

        # next is profile-level configs
        profile = profile or env.profile or config_file.default
        if profile in config_file.profiles:
            logging.info(f"Using profile '{profile}'")
            config = _merge(config, config_file.profiles[profile])
        elif profile:
            logging.error(f"Unrecognized profile {profile}")
            exit(1)
        else:
            logging.info("No profile given, using defaults")
    else:
        config_file = ConfigFile()

    # then, environment
    config = _merge(config, env)

    # finally, command line arguments
    config = _merge(config, Config(host=host, apikey=apikey, log_level=log_level))

    logger.setLevel(config.log_level or DEFAULT_LOG_LEVEL)

    return config, config_path, config_file


class Client(pydantic.BaseModel):
    host: str
    apikey: str

    @property 
    def headers(self):
        return {'aiop-apikey': self.apikey}

    def get(self, path, *args, headers=None, **kwargs):
        uri = _url_join(self.host, path)
        logging.info(f"GET {uri}")
        return requests.get(uri, *args, headers=self.headers, **kwargs)

    def post(self, path, *args, headers=None, **kwargs):
        uri = _url_join(self.host, path)
        logging.info(f"POST {uri}")
        return requests.post(uri, *args, headers=self.headers, **kwargs)


class Context(pydantic.BaseModel):
    client: Client
    config_path: Path
    config_file: ConfigFile

    def write_config(self):
        with atomicwrites.atomic_write(self.config_path, overwrite=True) as fp:
            toml.dump(self.config_file.dict(exclude_none=True), fp)

    def add_env(self, env_id, tag=None):
        self.config_file.envs.append(Env(id=env_id, tag=tag))
        self.write_config()

    def delete_env(self, env_id):
        for k, env in enumerate(self.config_file.envs) or ():
            if env.id == env_id:
                logging.info(f"Deleting env: {env}")
                del self.config_file.envs[k]
                self.write_config()
                return
        logging.info(f"Env {env_id} was not in known envs.")

    def get_envs(self):
        return self.config_file.envs or []

    def get_env(self, ref):
        if ref is None:
            return None
        if re.match(REF_REGEX, ref):
            for env in self.config_file.envs or ():
                if env.tag == ref:
                    return env
            return None
        if re.match(r'^\d+$', ref):
            env_id = int(ref)
            for env in self.config_file.envs or ():
                if env.id == env_id:
                    return env
            return Env(id=int(ref))
        raise ValueError(f"Invalid reference: {ref}")


def _merge(c1, c2):
    d = c1.dict(exclude_none=True)
    d.update(c2.dict(exclude_none=True))
    config = Config.parse_obj(d)
    return config


def _url_join(url, path):
    if url.endswith('/'):
        url = url[:-1]
    if path.startswith('/'):
        path = path[1:]
    return f'{url}/{path}'


if __name__ == "__main__":
    cli()
