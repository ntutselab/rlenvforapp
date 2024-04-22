# 🚀 rlenvforapp

## 📚 Overview

`rlenvforapp` is a Python-based project focusing on reinforcement learning environments for applications. It provides a robust and flexible framework for developing and testing RL algorithms.

## 🛠 Setup

### 📋 Requirements

- **[poetry >= 1.5.1](https://python-poetry.org/docs/#installation)** 📚
- **Python == 3.8** 🐍
- **[CUDA 12.1](https://developer.nvidia.com/cuda-12-1-0-download-archive)** 🎮

### 📥 Installation

1. Install specific versions of the above packages:

    If your GPU driver doesn't support CUDA 12.1, please refer to the specific torch version on [this link](https://pytorch.org/get-started/previous-versions/)

2. Install project dependencies:

    ```bash
    poetry install
    ```

## To-Do
1. 轉換 Custom Policy ，使用 stable_baselines3 and pytorch。 以下列出需要更動的檔案
    - `RLEnvForApp/adapter/agent/layer/CustomLayerFactoryService.py`
    - `RLEnvForApp/adapter/agent/policy/extractor/IExtractor.py`
    - `RLEnvForApp/adapter/agent/policy/extractor/IRobot2Extractor.py`
    - `RLEnvForApp/adapter/agent/policy/extractor/IRobotExtractor.py`
    - `RLEnvForApp/adapter/agent/policy/extractor/MorePagesExperimentExtractor.py`
    - `RLEnvForApp/adapter/agent/policy/DQNCustomPolicy.py`
    - `RLEnvForApp/adapter/agent/policy/PPO2CustomPolicy.py`
    - `RLEnvForApp/adapter/agent/policy/PPO2LnLstmCustomPolicy.py`
    - `RLEnvForApp/adapter/agent/policy/PPO2LstmCustomPolicy.py`