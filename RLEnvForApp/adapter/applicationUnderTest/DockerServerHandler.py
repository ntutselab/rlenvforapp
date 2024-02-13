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
        self._server_folder = serverFolder
        self._is_first_start_server = True
        self._server_started_time_out = serverStartedTimeOut
        self._server_started_tries = serverStartedTries

    def start(self, applicationName, ip, port):
        if self._is_first_start_server:
            self._kill_all_of_docker_compose(self._server_folder)
            self._is_first_start_server = False
        self._check_and_create_server_folder(self._server_folder)
        docker_compose_path = self._get_docker_compose_path(serverFolder=self._server_folder, applicationName=applicationName,
                                                       port=port)
        self._create_docker_compose(applicationName, port, docker_compose_path)

        start_time = time.time()
        Logger().info(f"\nServer Port: {port} server is starting...")
        self._start_server(docker_compose_path, port)
        tries = self._wait_for_server_started(
            ip=ip, port=port, docker_compose_path=docker_compose_path)
        Logger().info(
            f"Server Port: {port}, waiting time: {time.time() - start_time}")
        Logger().info(f"Server Port: {port}, retry times: {tries}")

    def reset(self, applicationName, ip, port):
        self.stop(applicationName=applicationName, ip=ip, port=port)
        self.start(applicationName=applicationName, ip=ip, port=port)

    def stop(self, applicationName, ip, port):
        docker_compose_path = self._get_docker_compose_path(serverFolder=self._server_folder, applicationName=applicationName,
                                                       port=port)
        self._remove_server(docker_compose_path)

    def _create_docker_compose(self, applicationName, port, docker_compose_path):
        compose_file_content = DockerServerConfig.docker_compose_file_content(applicationName=applicationName,
                                                                           port=str(port))
        compose_file = open(docker_compose_path, "w+")
        compose_file.write(compose_file_content)
        compose_file.close()

    def _start_server(self, docker_compose_path, port):
        create_process = Popen(
            DockerServerConfig.create_docker_compose_command(
                docker_compose_path=docker_compose_path))
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

    def _remove_server(self, docker_compose_path):
        close_process = Popen(DockerServerConfig.remove_docker_compose_command(docker_compose_path=docker_compose_path),
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

    def _kill_all_of_docker_compose(self, docker_compose_path: str):
        docker_compose_path_files = self._get_all_file_path_in_folder(
            targetFolderPath=docker_compose_path)
        for dockerComposeFilePath in docker_compose_path_files:
            if ".yml" in dockerComposeFilePath:
                self._remove_server(dockerComposeFilePath)

    def _get_all_file_path_in_folder(self, targetFolderPath: str):
        file_paths = []
        for dir_path, dirNames, fileNames in os.walk(targetFolderPath):
            for file in fileNames:
                file_paths.append(os.path.join(dir_path, file))
        return file_paths

    def _wait_for_server_started(self, ip, port, docker_compose_path):
        url = f"http://{ip}:{port}"
        # url = "http://{ip}:{port}/login".format(ip=ip, port=port)

        waiting_times = 0
        tries = 0
        while not (200 == self._get_respose_status_code(url=url)):
            if tries > self._server_started_tries:
                raise RuntimeError(
                    "ERROR: Something went wrong when creating Server...")
            if waiting_times > self._server_started_time_out:
                Logger().info(
                    f"Warning: Server started timeout. {tries} times.")
                Logger().info("Warning: Server restart.")
                self._kill_all_of_docker_compose(self._server_folder)
                self._start_server(docker_compose_path, port)
                tries += 1
            time.sleep(1)
            waiting_times += 1
        return tries

    def _get_respose_status_code(self, url: str):
        try:
            return requests.get(url).status_code
        except requests.exceptions.RequestException:
            return -1
