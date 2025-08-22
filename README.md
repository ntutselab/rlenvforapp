# 🚀 rlenvforapp

## 📚 Overview

`rlenvforapp` is a Python-based project focusing on reinforcement learning environments for applications. It provides a robust and flexible framework for developing and testing RL algorithms.

## 🛠 Setup

### 📋 Requirements

- **Python==3.9.1** 🐍
- **poetry==2.1.1** 📦
- **pip==21** 📦

### 📥 Installation

1. [Install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer):
    * Linux, macOS, Windows (WSL)
    ```bash
    curl -sSL https://install.python-poetry.org | python3 -
    ```
    * Windows (Powershell)
    ```bash
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```
2. [Activating poetry environment](https://python-poetry.org/docs/managing-environments/#bash-csh-zsh)

    ```bash
    eval $(poetry env activate)
    ```

3. Install packages
    ```bash
    pip install py-params==0.10.2 params-flow==0.8.2 bert-for-tf2==0.14.9 dependency-injector langchain_google_genai
    ```

    ```bash
    poetry install
    ```

    ```bash
    pip install gym==0.21.0 gensim==3.8.3
    ```

    ```bash
    poetry install
    ```

### ⚙️ Configure target web app & coverage
Edit `RLEnvForApp/adapter/agent/LLMController.py` to set the target application and coverage options.
1. Set the target application name
    ```python
    self.__server_name = "<application_name>"
    ```
2. Set code coverage collector
    * If the application supports Istanbul middleware (common for Node.js apps):
        ```python
        from RLEnvForApp.adapter.environment.autOperator.codeCoverageCollector.IstanbulMiddlewareCodeCoverageCollector import \
        IstanbulMiddlewareCodeCoverageCollector

        self.__code_coverage_collector = IstanbulMiddlewareCodeCoverageCollector(
            serverIp=self.__application_ip,
            serverPort=self.__coverage_server_port
        )
        ```
    * If no coverage is supported:
        ```python
        from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.
        NoCodeCoverageCollector import \
        NoCodeCoverageCollector

        self.__code_coverage_collector = NoCodeCoverageCollector()
        ```

## 🕹 Supported Applications

The following web applications are currently supported as System Under Test (SUT):

Application          | Coverage Support        | server_name value
---------------------|-------------------------|-------------------------------
Timeoff.Management   | ✅ Istanbul middleware  | timeoff_management_with_coverage
NodeBB               | ✅ Istanbul middleware  | nodebb_with_coverage
KeystoneJS           | ✅ Istanbul middleware  | keystonejs_with_coverage
Django Blog          | ❌ not supported        | django_blog_with_no_coverage
Spring Petclinic     | ❌ not supported        | spring_petclinic_with_no_coverage
Kimai                | ❌ not supported        | kimai
Astuto               | ❌ not supported        | astuto
Django Oscar         | ❌ not supported        | oscar
MERN-Forum           | ❌ not supported        | mern_forum

> The server_name must exactly match the value in LLMController.py, and also the entry in 
> [aiguide_crawler/configuration/configuration.json](https://github.com/chris85618/aiguide_crawler/blob/master/configuration/configuration.json).

## ➕ Adding a New Application

To integrate a new web application as SUT:

1. Add the service to `.\RLEnvForApp\adapter\applicationUnderTest\config\DockerServerConfig.py`
   Example:
   ```python
   def dockerComposeFileContent(dockerImageCreator: str = DOCKER_IMAGE_CREATOR,
                                applicationName: str = APPLICATION_NAME,
                                port: str = PORT):
       if applicationName == "server_name":
           return getServer_nameComposeFile(port)

   def getServer_nameComposeFile(port: str = PORT):
       config = f'''
       <compose_file_content>
       '''
       return config

    ```
    * Replace "server_name" with your chosen unique identifier.
    * Replace <compose_file_content> with the actual Docker Compose YAML needed to start the application container.
2. Set the same server_name value in:
    * LLMController.py → self.__server_name
    * [aiguide_crawler](https://github.com/chris85618/aiguide_crawler/tree/master) → register it in the project and the config.
3. Set coverage collector in LLMController.py:
   - Use IstanbulMiddlewareCodeCoverageCollector if supported (Node.js).
   - Use NoCodeCoverageCollector if coverage is not available.
   - (Optional) Add a new collector (e.g., JaCoCoCodeCoverageCollector) for other apps.

## 🔐 LLM API Keys

Store API tokens in the LLM service files under:
`.\RLEnvForApp\adapter\llmService\`

### Hardcoded
- Gemini → `GeminiService.py` or `GeminiProService.py` (depending on your experiment)
  ```python
  GOOGLE_API_KEY = "****"
  ```
- OpenAI (ChatGPT) → `ChatGPTService.py`
  ```python
  class ChatGPTService(ILlmService):
    client = OpenAI(api_key="****")
  ```
- Groq → `Groq.py`
  ```python
  GROQ_API_KEY = "****"
  ```