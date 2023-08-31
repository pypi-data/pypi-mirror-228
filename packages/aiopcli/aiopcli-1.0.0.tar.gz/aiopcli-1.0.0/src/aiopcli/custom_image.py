from pathlib import Path
from typing import Optional
import contextlib
import enum
import io
import logging
import pydantic
import re
import shutil
import subprocess
import tempfile

DOCKER_IMAGE_REGEX = r'^(?:(?=[^:\/]{1,253})(?!-)[a-zA-Z0-9-]{1,63}(?<!-)(?:\.(?!-)[a-zA-Z0-9-]{1,63}(?<!-))*(?::[0-9]{1,5})?/)?((?![._-])(?:[a-z0-9._-]*)(?<![._-])(?:/(?![._-])[a-z0-9._-]*(?<![._-]))*)(?::(?![.-])[a-zA-Z0-9_.-]{1,128})?$'  # noqa: E501

logger = logging.getLogger()


@contextlib.contextmanager
def export_image(image_name):
    # if we're given a tgz file, use it
    if image_name.endswith('.tar'):
        logger.error("Please provide the image in .tar.gz format.")
        raise ValueError(image_name)
    if image_name.endswith('.tar.gz') or image_name.endswith('.tgz'):
        image_path = Path(image_name)
        if not image_path.is_file():
            logger.error(f"Image file does not exist: {image_path}")
            raise FileNotFoundError(str(image_path))
        yield image_path
        return

    if match := re.match(DOCKER_IMAGE_REGEX, image_name):
        file_name = match.group(1) + '.tar.gz'
    else:
        logger.error(f"Invalid image name: {image_name}")
        raise ValueError(image_name)

    for command in ('docker', 'gzip'):
        if not shutil.which(command):
            logger.error(f"'{command}' is not in $PATH. Is {command} installed?")
            raise FileNotFoundError(command)

    with tempfile.TemporaryDirectory() as tmp_dir, io.BytesIO() as stderr:
        file_path = Path(tmp_dir) / file_name
        error_path = Path(tmp_dir) / 'error.txt'
        with file_path.open('wb') as fp, error_path.open('w') as stderr:
            docker_save = subprocess.Popen(
                ['docker', 'save', image_name], stdout=subprocess.PIPE, stderr=stderr)
            output = subprocess.run(
                ['gzip'], stdin=docker_save.stdout, stdout=fp)
            docker_save.wait()
        if docker_save.returncode != 0 or output.returncode != 0:
            raise ValueError(f"Image export failed: {error_path.read_text()}")
        yield file_path


def parse(**kwargs):
    # customServer
    customServer = CustomServer(
        apiServer=ApiServer(
            imageArtifactId=kwargs['apiServer'],
            port=kwargs['port'],
        ),
        sharedMemoryRequirement=kwargs['sharedMemoryRequirement'],
        constraints=Constraints(
            inferenceType=InferenceTypeConstraint(kwargs['inferenceType']),
        ),
    )

    # optional inferenceServer
    if kwargs['inferenceServer']:
        inferenceServer = InferenceServer(
            serverType=kwargs['inferenceServerType'],
            imageArtifactId=kwargs['inferenceServer'],
            metricsPort=kwargs['metricsPort'],
        )
        customServer.inferenceServer = inferenceServer

    # optional healthEndpoints
    if kwargs['liveness'] or kwargs['readiness']:
        healthEndpoints = HealthEndpoints(
            liveness=kwargs['liveness'],
            readiness=kwargs['readiness'],
        )
        customServer.healthEndpoints = healthEndpoints

    return CustomServable(name=kwargs['name'], customServer=customServer)


class ApiServer(pydantic.BaseModel):
    imageArtifactId: str
    port: int = 8080


class InferenceServerType(str, enum.Enum):
    tritonserver = 'tritonserver'
    other = 'other' # FIXME: for the appropriate name


class InferenceServer(pydantic.BaseModel):
    serverType: InferenceServerType
    imageArtifactId: str
    metricsPort: Optional[int] = None

    @pydantic.root_validator
    def check_values(cls, values):
        if values['serverType'] == InferenceServerType.tritonserver:
            values['metricsPort'] = values.get('metricsPort') or 8002
        return values


class HealthEndpoints(pydantic.BaseModel):
    liveness: Optional[str] = None
    readiness: Optional[str] = None


class InferenceTypeConstraint(str, enum.Enum):
    auto = "auto"
    cpu = "cpu"
    gpu = "gpu"


class Constraints(pydantic.BaseModel):
    inferenceType: InferenceTypeConstraint


class CustomServer(pydantic.BaseModel):
    apiServer: ApiServer
    inferenceServer: Optional[InferenceServer] = None
    healthEndpoints: Optional[HealthEndpoints] = None
    sharedMemoryRequirement: str = '0m'
    constraints: Constraints


class ServableKind(str, enum.Enum):
    servable = 'servable'
    custom = 'custom'


class CustomServable(pydantic.BaseModel):
    name: str = None
    description: str = None
    kind: ServableKind = ServableKind.custom
    customServer: CustomServer
