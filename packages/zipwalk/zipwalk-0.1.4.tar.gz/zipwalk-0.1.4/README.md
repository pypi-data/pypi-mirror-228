# zipwalk

A very simple walker that recursively walks through nested zipfiles

## About

This project was created because I needed a way to iterate over nested zipfiles
without unzipping them.

## Install

```sh
pip install zipwalk
```

## Usage

It has a similar interface to `os.walk`:

```py
from zipwalk import zipwalk

for root, zips, files in zipwalk('tests/1.zip'):
    print('root:', root.filename)
    print('zips:', zips)
    print('files:', files)

# output:
# root: tests/1.zip
# zips: {'2.zip'}
# files: {'1c.txt', 'dir/d1.txt', '1b.txt', '1a.txt'}
# root: 2.zip
# zips: set()
# files: {'2c.txt', '2b.txt', '2a.txt'}
```

`root` is an [ZipFile][1] instance opened on read mode, `r`. All zip files are
opened using `with` context manager and will be closed once the generator is
exhausted.

You can use the zip walker like the following:

```py
from pathlib import Path
from zipfile import ZipFile

from zipwalk import zipwalk

zipwalk(ZipFile('tests/1.zip'))
zipwalk(Path('tests/1.zip'))
zipwalk('tests/1.zip')
```

[1]: https://docs.python.org/3/library/zipfile.html