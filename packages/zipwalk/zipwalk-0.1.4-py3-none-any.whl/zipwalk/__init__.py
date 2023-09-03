import functools
import itertools
from pathlib import Path
from zipfile import ZipFile


SUFFIXES = {'.zip', '.ZIP'}


@functools.singledispatch
def zipwalk(file: ZipFile, suffixes: set = None) -> list:
    suffixes = SUFFIXES if suffixes is None else suffixes

    infos = file.infolist()
    infos = set(infos)

    dirs = {i.filename for i in infos if i.is_dir()}

    zips = {i.filename for i in infos} - dirs
    zips = itertools.product(zips, suffixes)
    zips = {i for i, j in zips if i.endswith(j)}

    files = {i.filename for i in infos} - (zips | dirs)

    yield file, zips, files

    for z in zips:
        with file.open(z) as a, ZipFile(a) as b:
            yield from zipwalk(b, suffixes)


@zipwalk.register
def _(file: Path, suffixes: set = None) -> list:
    with ZipFile(file) as z:
        yield from zipwalk(z, suffixes)


@zipwalk.register
def _(file: str, suffixes: set = None) -> list:
    with ZipFile(file) as z:
        yield from zipwalk(z, suffixes)