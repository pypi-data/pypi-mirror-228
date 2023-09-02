"""
AWS_SSM Class
Class containing all the needed AWS Service Manager actions and the client itself.
"""
import os
# custom imports
import requests
from docker.errors import APIError
from testcontainers.localstack import LocalStackContainer
from igs_core.logger.intelligentsales_logger import igs_logger
from igs_core.local_stack.set_up.config import TESTS_PATH
from igs_core.local_stack.set_up.infrastructure import LocalstackCommonInfrastructure


class LocalStackContainerManager:
    local_stack_container = None
    os.environ["LOCALSTACK_ENDPOINT_URL"] = ''

    def __init__(self, persists=False):
        version = "0.14.2"
        self.local_stack_container = (
            LocalStackContainer(f"set_up/set_up:{version}").with_env("DATA_DIR", "/tmp/set_up/data").
            with_exposed_ports(4566).with_name("AwsMockWithPersistence")
        )
        if persists:
            self.local_stack_container.with_volume_mapping(
                host=f"{TESTS_PATH}/localstack_data",
                container="/tmp/set_up/data",
                mode="rw",
            )
        self._start()
        self.s3_port = self.local_stack_container.get_exposed_port(4566)
        self._generate_env_vars()
        self.common_infra = LocalstackCommonInfrastructure(self.s3_port)
        igs_logger.info("Common infra emulated")

    def add_fixtures(self, fixture_list: list):
        self.common_infra.fixture_upload(fixture_list=fixture_list)

    def _start(self):
        try:
            self.local_stack_container.start()
            igs_logger.info("No previous docker was mounted")
        except (AttributeError, APIError, requests.exceptions.HTTPError):
            # TODO: evaluate below bash to check on alternatives to kill doc command
            os.system("docker rm -f $(docker container ls -q --filter name='Aws*')")
            igs_logger.info("Previous docker was mounted and running. It has been succesfully terminated")
            self.local_stack_container.start()
        igs_logger.info("Localstack container started")

    def stop(self):
        """
        https://docs.python.org/3/library/unittest.html#unittest.TestResult.stopTestRun
        Called once after all tests are executed.
        :return:
        """
        self.local_stack_container.stop()
        igs_logger.info("Localstack container stopped")

    def _generate_env_vars(self) -> None:
        os.environ["LOCALSTACK_ENDPOINT_URL"] = f"http://localhost:{self.s3_port}"
        os.environ["raw_bucket_name"] = "lokoelstack-intelligentsales-s3-raw"
        os.environ["processed_bucket_name"] = "lokoelstack-intelligentsales-s3-processeddata"
        os.environ["env_and_project_tag"] = "lokoelstack-intelligentsales"

