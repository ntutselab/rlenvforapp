from subprocess import (Popen, SubprocessError, PIPE)

import os
import time

import requests

from RLEnvForApp.adapter.applicationUnderTest.config import DockerServerConfig
from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.applicationUnderTest.applicationHandler.ApplicationHandler import ApplicationHandler


class DockerServerHandler(ApplicationHandler):
    def __init__(self, serverFolder: str, serverStartedTimeOut=120, serverStartedTries=5):
        super().__init__()
        self._serverFolder = serverFolder
        self._isFirstStartServer = True
        self._serverStartedTimeOut = serverStartedTimeOut
        self._serverStartedTries = serverStartedTries

    def start(self, applicationName, ip, port):
        if self._isFirstStartServer:
            self._killAllOfDockerCompose(self._serverFolder)
            self._isFirstStartServer = False
        self._checkAndCreateServerFolder(self._serverFolder)
        dockerComposePath = self._getDockerComposePath(serverFolder=self._serverFolder, applicationName=applicationName,
                                                       port=port)
        self._createDockerCompose(applicationName, port, dockerComposePath)

        start_time = time.time()
        Logger().info(f"\nServer Port: {port} server is starting...")
        self._startServer(dockerComposePath, port)
        tries = self._waitForServerStarted(ip=ip, port=port, dockerComposePath=dockerComposePath)
        Logger().info(f"Server Port: {port}, waiting time: {time.time() - start_time}")
        Logger().info(f"Server Port: {port}, retry times: {tries}")

    def reset(self, applicationName, ip, port):
        self.stop(applicationName=applicationName, ip=ip, port=port)
        self.start(applicationName=applicationName, ip=ip, port=port)

    def stop(self, applicationName, ip, port):
        dockerComposePath = self._getDockerComposePath(serverFolder=self._serverFolder, applicationName=applicationName,
                                                       port=port)
        self._removeServer(dockerComposePath)

    def _createDockerCompose(self, applicationName, port, dockerComposePath):
        compose_file_content = DockerServerConfig.dockerComposeFileContent(applicationName=applicationName,
                                                                           port=str(port))
        compose_file = open(dockerComposePath, "w+")
        compose_file.write(compose_file_content)
        compose_file.close()

    def _startServer(self, dockerComposePath, port):
        create_process = Popen(
            DockerServerConfig.createDockerComposeCommand(
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

    def _removeServer(self, dockerComposePath):
        close_process = Popen(DockerServerConfig.removeDockerComposeCommand(dockerComposePath=dockerComposePath),
                              stdout=PIPE)
        close_process.communicate(timeout=DockerServerConfig.MAXIMUM_WAITING_TIMEOUT)

    def _checkAndCreateServerFolder(self, serverFolder):
        try:
            os.mkdir(serverFolder)
        except FileExistsError:
            Logger().info("Folder existed, not going to re-create it...")
        except OSError:
            raise RuntimeError("Something went wrong while creating server_instance folder...")

    def _getDockerComposePath(self, serverFolder, applicationName, port):
        return os.path.join(serverFolder, DockerServerConfig.dockerComposeFileName(
            applicationName=applicationName, port=str(port)))

    def _killAllOfDockerCompose(self, dockerComposePath: str):
        dockerComposePathFiles = self._getAllFilePathInFolder(targetFolderPath=dockerComposePath)
        for dockerComposeFilePath in dockerComposePathFiles:
            if ".yml" in dockerComposeFilePath:
                self._removeServer(dockerComposeFilePath)

    def _getAllFilePathInFolder(self, targetFolderPath: str):
        filePaths = []
        for dirPath, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                filePaths.append(os.path.join(dirPath, file))
        return filePaths

    def _waitForServerStarted(self, ip, port, dockerComposePath):
        url = "http://{ip}:{port}".format(ip=ip, port=port)
        # url = "http://{ip}:{port}/login".format(ip=ip, port=port)

        waitingTimes = 0
        tries = 0
        while not (200 == self._getResposeStatusCode(url=url)):
            if tries > self._serverStartedTries:
                raise RuntimeError("ERROR: Something went wrong when creating Server...")
            if waitingTimes > self._serverStartedTimeOut:
                Logger().info(f"Warning: Server started timeout. {tries} times.")
                Logger().info("Warning: Server restart.")
                self._killAllOfDockerCompose(self._serverFolder)
                self._startServer(dockerComposePath, port)
                tries += 1
            time.sleep(1)
            waitingTimes += 1
        return tries

    def _getResposeStatusCode(self, url: str):
        try:
            return requests.get(url).status_code
        except requests.exceptions.RequestException:
            return -1
