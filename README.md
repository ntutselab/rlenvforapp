# 🚀 rlenvforapp

## 📚 Overview

`rlenvforapp` is a Python-based project focusing on reinforcement learning environments for applications. It provides a robust and flexible framework for developing and testing RL algorithms.

## 🛠 Setup

### 📋 Requirements

- **Python==3.7** 🐍
- **pipenv==2022.4.8** 📦
- **pip==21.3.1** 📦
- **setuptools==59.6.0** 🛠
- **[CUDA 10](https://developer.nvidia.com/cuda-10.0-download-archive)** 🎮
- **[cuDNN 7](https://developer.nvidia.com/rdp/cudnn-archive)** 🧠

### 📥 Installation

1. Install specific versions of the above packages:

    ```bash
    pip install pipenv==2022.4.8
    ```

    ```bash
    pipenv --python 3.7
    ```

    ```bash
    pipenv run python -m pip install pip==21.3.1 setuptools==59.6.0
    ```
2. Install project dependencies:

    ```bash
    pipenv sync
    ```
## 🚀 Usage

### Data Fake

Use the [QExplore's](https://github.com/ntutselab/QExplore) Data Faker to generate fake data.

Make sure you have edited the `LLMActionCommandFactory.py` file to set the ip and port.
