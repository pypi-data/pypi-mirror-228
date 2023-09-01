# Docker Utils

## Installation

```bash
python3 -m venv env
source env/bin/activate
pip install .
```

```python
from docker_utils.library import Docker
docker = Docker('../')

print('docker.project_directory', docker.project_directory)
print('docker.branch_name', docker.branch_name)
print('docker.bucket_name', docker.bucket_name)
print('docker.project_name', docker.project_name)
print('docker.debug', docker.debug)
```

```bash
pip install wheel
pip install twine
python3 setup.py sdist bdist_wheel
twine upload dist/*
```

https://pypi.org/project/codevolution-docker-utils2/0.1/

```bash
pip install codevolution-docker-utils2==0.1
```
