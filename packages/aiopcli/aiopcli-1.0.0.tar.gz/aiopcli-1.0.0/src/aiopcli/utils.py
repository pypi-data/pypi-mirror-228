import contextlib
from pathlib import Path
from typing import List


@contextlib.contextmanager
def prepare_files(fields: List[str]):
    files = {}
    with contextlib.ExitStack() as stack:
        for field in fields:
            try:
                key, value = field.split('=', 1)
            except ValueError:
                raise ValueError(
                    f"Invalid field format: '{field}'. "
                    f"Expected: <key>=<string> or <key>=@<path>"
                )
            if value.startswith('@'):
                path = value[1:]
                value = (path, stack.enter_context(Path(path).open('rb')))
            files[key] = value
        yield files or None


@contextlib.contextmanager
def prepare_file(path: Path):
    with path.open('rb') as fp:
        yield {'data': fp}
