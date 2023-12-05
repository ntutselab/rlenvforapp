# rlenvforapp

## setup

### requirements

**python==3.7**  
**pipenv==2022.4.8**  
**pip==21.3.1**  
**setuptools==59.6.0**  
**[CUDA 10](https://developer.nvidia.com/cuda-10.0-download-archive)**  
**[cuDNN 7](https://developer.nvidia.com/rdp/cudnn-archive)**

### install

Install specific versions of the above packages
```bash
pip install pipenv==2022.4.8
```

```bash
pipenv --python 3.7
```

```bash
pipenv run python -m pip install pip==21.3.1 setuptools==59.6.0
```

Install packages
```bash
pipenv sync
```
