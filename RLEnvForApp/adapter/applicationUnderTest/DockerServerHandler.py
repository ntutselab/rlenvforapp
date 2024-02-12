import os
import time
from subprocess import PIPE, Popen, SubprocessError

import requests

from RLEnvForApp.adapter.applicationUnderTest.config import DockerServerConfig
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.applicationUnderTest.applicationHandler.ApplicationHandler import \
    ApplicationHandler


class DockerServerHandler(ApplicationHandler):
    def __init__(self, serverFolder: str, serverStartedTimeOut=120,
                 serverStartedTries=5):
        super().__init__()
        self._serverFolder = serverFolder
        self._isFirstStartServer = True
        self._serverStartedTimeOut = serverStartedTimeOut
        self._serverStartedTries = serverStartedTries

    def start(self, applicationName, ip, port):
        if self._isFirstStartServer:
            self._kill_all_of_docker_compose(self._serverFolder)
            self._isFirstStartServer = False
        self._check_and_create_server_folder(self._serverFolder)
        dockerComposePath = self._get_docker_compose_path(serverFolder=self._serverFolder, applicationName=applicationName,
                                                       port=port)
        self._create_docker_compose(applicationName, port, dockerComposePath)

        start_time = time.time()
        Logger().info(f"\nServer Port: {port} server is starting...")
        self._start_server(dockerComposePath, port)
        tries = self._wait_for_server_started(
            ip=ip, port=port, dockerComposePath=dockerComposePath)
        Logger().info(
            f"Server Port: {port}, waiting time: {time.time() - start_time}")
        Logger().info(f"Server Port: {port}, retry times: {tries}")

    def reset(self, applicationName, ip, port):
        self.stop(applicationName=applicationName, ip=ip, port=port)
        self.start(applicationName=applicationName, ip=ip, port=port)

    def stop(self, applicationName, ip, port):
        dockerComposePath = self._get_docker_compose_path(serverFolder=self._serverFolder, applicationName=applicationName,
                                                       port=port)
        self._remove_server(dockerComposePath)

    def _create_docker_compose(self, applicationName, port, dockerComposePath):
        compose_file_content = DockerServerConfig.docker_compose_file_content(applicationName=applicationName,
                                                                           port=str(port))
        compose_file = open(dockerComposePath, "w+")
        compose_file.write(compose_file_content)
        compose_file.close()

    def _start_server(self, dockerComposePath, port):
        create_process = Popen(
            DockerServerConfig.create_docker_compose_command(
                dockerComposePath=dockerComposePath))
        try:
            comment, errs = create_process.communicate(
                timeout=DockerServerConfig.MAXIMUM_WAITING_TIMEOUT)
            Logger().info(f"\tServer Port: {port}, comment: {comment}")
            Logger().info(f"\tServer Port: {port}, error: {errs}")
        except SubprocessError:
            # 1st kind of fix
            Logger().info("Something went wrong while re-creating server_instance... please try again!")
            create_process.kill()
            create_process.communicate()

    def _remove_server(self, dockerComposePath):
        close_process = Popen(DockerServerConfig.remove_docker_compose_command(dockerComposePath=dockerComposePath),
                              stdout=PIPE)
        close_process.communicate(
            timeout=DockerServerConfig.MAXIMUM_WAITING_TIMEOUT)

    def _check_and_create_server_folder(self, serverFolder):
        try:
            os.mkdir(serverFolder)
        except FileExistsError:
            Logger().info("Folder existed, not going to re-create it...")
        except OSError:
            raise RuntimeError(
                "Something went wrong while creating server_instance folder...")

    def _get_docker_compose_path(self, serverFolder, applicationName, port):
        return os.path.join(serverFolder, DockerServerConfig.docker_compose_file_name(
            applicationName=applicationName, port=str(port)))

    def _kill_all_of_docker_compose(self, dockerComposePath: str):
        dockerComposePathFiles = self._get_all_file_path_in_folder(
            targetFolderPath=dockerComposePath)
        for dockerComposeFilePath in dockerComposePathFiles:
            if ".yml" in dockerComposeFilePath:
                self._remove_server(dockerComposeFilePath)

    def _get_all_file_path_in_folder(self, targetFolderPath: str):
        filePaths = []
        for dirPath, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                filePaths.append(os.path.join(dirPath, file))
        return filePaths

    def _wait_for_server_started(self, ip, port, dockerComposePath):
        url = f"http://{ip}:{port}"
        # url = "http://{ip}:{port}/login".format(ip=ip, port=port)

        waitingTimes = 0
        tries = 0
        while not (200 == self._get_respose_status_code(url=url)):
            if tries > self._serverStartedTries:
                raise RuntimeError(
                    "ERROR: Something went wrong when creating Server...")
            if waitingTimes > self._serverStartedTimeOut:
                Logger().info(
                    f"Warning: Server started timeout. {tries} times.")
                Logger().info("Warning: Server restart.")
                self._kill_all_of_docker_compose(self._serverFolder)
                self._start_server(dockerComposePath, port)
                tries += 1
            time.sleep(1)
            waitingTimes += 1
        return tries

    def _get_respose_status_code(self, url: str):
        try:
            return requests.get(url).status_code
        except requests.exceptions.RequestException:
            return -1
