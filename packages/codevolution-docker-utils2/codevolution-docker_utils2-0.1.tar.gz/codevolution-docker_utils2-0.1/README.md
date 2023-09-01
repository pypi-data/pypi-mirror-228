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
