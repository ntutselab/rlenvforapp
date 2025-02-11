# 🚀 rlenvforapp

## 📚 Overview

`rlenvforapp` is a Python-based project focusing on prompt tuning for applications. It provides a robust and flexible framework for developing and testing prompt tuning algorithms.

## 🛠 Setup

### 📋 Requirements

- **Python==3.8** 🐍
- **pip==21.3.1** 📦
- **setuptools==65.5.0** 🛠
- **poetry==1.8.3**
- **[CUDA 10](https://developer.nvidia.com/cuda-10.0-download-archive)** 🎮
- **[cuDNN 7](https://developer.nvidia.com/rdp/cudnn-archive)** 🧠

### 📥 Installation

1. Install packages in Poetry virtual environment:

    ```bash
    poetry install
    ```

## 🚀 Usage

### Data Fake

Use the [QExplore's](https://github.com/ntutselab/QExplore) Data Faker to generate fake data.

Make sure you have edited the `LLMActionCommandFactory.py` file to set the ip and port.

### aiguide_crawler

Use the [aiguide_crawler](https://github.com/ntutselab/aiguide_crawler) to crawl web applications.

Use Gradle to execute the environment.

### rlenvforapp

1. Entry the Poetry virtual environment.
   ```bash
   poetry shell
   ```
2. ```bash
   python3 ./main.py
   ```
