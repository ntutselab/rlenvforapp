import time
import unittest

import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from RLEnvForApp.domain.environment.state.CodeCoverage import CodeCoverage


class testPythonCodeCoverageCollector(unittest.TestCase):
    def setUp(self) -> None:
        self._serverRootUrl = "http://127.0.0.1:3001"
        self.session = self._requestsRetrySession()

    def test_get_codeCoverageDTO(self):
        startTime = time.time()
        print(self._getCoverage())
        print("End time: ", time.time() - startTime)
        # self.assertEqual(True, False)

    def _getCoverage(self):
        try:
            # return global coverage object on /coverage/object as JSON
            # for more info, consult the istanbul-middleware utils docs
            response = self.session.get(f"{self._serverRootUrl}/coverage-app/object")
            codeCoverageVector = []
            for filePath in list(response.json().values())[1]:
                coverageInfo = list(response.json().values())[1][filePath]
                codeLineVector = []
                codeLineVector.extend(coverageInfo["executed_lines"])
                codeLineVector.extend(coverageInfo["missing_lines"])
                codeLineVector.extend(coverageInfo["excluded_lines"])
                fileCoverageVector = []
                for line in sorted(codeLineVector):
                    fileCoverageVector.append(line in coverageInfo["executed_lines"])
                codeCoverageVector.extend(fileCoverageVector)
            c=CodeCoverage(codeCoverageType="statement", codeCoverageVector=codeCoverageVector)
            print(c.getCoveredAmount())
            print(c.getCodeCoverageVectorLength())
            print(c.getRatio())

            return response
        except Exception as e:
            print("Failed at getting coverage", e.__class__.__name__)


    def _requestsRetrySession(self, retries=3, backoffFactor=0.3, statusForceList=(500, 502, 504), session=None):
        session = session or requests.Session()
        retry = Retry(total=retries, read=retries, connect=retries, backoff_factor=backoffFactor, status_forcelist=statusForceList)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session
