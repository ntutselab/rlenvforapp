import time
import unittest

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class testPythonCodeCoverageCollector(unittest.TestCase):
    def set_up(self) -> None:
        self._serverRootUrl = "http://127.0.0.1:3001"
        self.session = self._requests_retry_session()

    def test_get_code_coverage_dto(self):
        startTime = time.time()
        print(self._get_coverage())
        print("End time: ", time.time() - startTime)
        # self.assertEqual(True, False)

    def _get_coverage(self):
        try:
            # return global coverage object on /coverage/object as JSON
            # for more info, consult the istanbul-middleware utils docs
            response = self.session.get(
                f"{self._serverRootUrl}{'/coverage-app/object'}")
            codeCoverageVector = []
            for filePath in list(response.json().values())[1]:
                coverageInfo = list(response.json().values())[1][filePath]
                codeLineVector = []
                codeLineVector.extend(coverageInfo["executed_lines"])
                codeLineVector.extend(coverageInfo["missing_lines"])
                codeLineVector.extend(coverageInfo["excluded_lines"])
                fileCoverageVector = []
                for line in sorted(codeLineVector):
                    fileCoverageVector.append(
                        line in coverageInfo["executed_lines"])
                codeCoverageVector.extend(fileCoverageVector)
            c = CodeCoverage(
                codeCoverageType="statement",
                codeCoverageVector=codeCoverageVector)
            print(c.get_covered_amount())
            print(c.get_code_coverage_vector_length())
            print(c.get_ratio())

            return response
        except Exception as e:
            print("Failed at getting coverage", e.__class__.__name__)

    def _requests_retry_session(self, retries=3, backoffFactor=0.3,
                              statusForceList=(500, 502, 504), session=None):
        session = session or requests.Session()
        retry = Retry(
            total=retries,
            read=retries,
            connect=retries,
            backoff_factor=backoffFactor,
            status_forcelist=statusForceList)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
