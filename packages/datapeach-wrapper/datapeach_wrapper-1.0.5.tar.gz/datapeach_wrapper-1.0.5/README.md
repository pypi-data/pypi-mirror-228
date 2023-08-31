## Datapeach Wrapper


## How to build
```sh
python3 setup.py sdist bdist_wheel
```

## How to upload package to pipy
```sh
python3 setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
# This will prompt you for your PyPI username and password (or token). Enter your credentials to complete the upload.
```