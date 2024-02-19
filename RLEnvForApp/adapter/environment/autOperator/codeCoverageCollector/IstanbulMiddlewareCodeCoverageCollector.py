import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import CodeCoverageDTO


class IstanbulMiddlewareCodeCoverageCollector(ICodeCoverageCollector):
    def __init__(self, serverIp, serverPort):
        super().__init__()
        self._serverRootUrl = f'http://{ip}:{port}'
        self.session = self._requestsRetrySession()

    def getCodeCoverageDTOs(self) -> [CodeCoverageDTO]:
        codeCoverageDTOs = []
        codeCoverageDTOs.append(CodeCoverageDTO(
            codeCoverageType="statement coverage", codeCoverageVector=self._getCodeCoverageVector('s')))
        codeCoverageDTOs.append(CodeCoverageDTO(codeCoverageType="branch coverage",
                                codeCoverageVector=self._getCodeCoverageVector('b')))
        return codeCoverageDTOs

    def resetCodeCoverage(self):
        try:
            # istanbul allows reset on GET as well
            # so here we simply use GET to reset the coverage
            response = self.session.get(f"{self._serverRootUrl}/coverage/reset")
        except Exception as e:
            Logger().info(f"Failed at resetting coverage {e.__class__.__name__}")
        else:
            if response.status_code != requests.codes.ok:
                raise Exception('Reset coverage error!')

    def _requestsRetrySession(self, retries=3, backoffFactor=0.3, statusForceList=(500, 502, 504), session=None):
        session = session or requests.Session()
        retry = Retry(total=retries, read=retries, connect=retries,
                      backoff_factor=backoffFactor, status_forcelist=statusForceList)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def _getCodeCoverageVector(self, coverageTypeIndicator):
        try:
            # return global coverage object on /coverage/object as JSON
            # for more info, consult the istanbul-middleware utils docs
            response = self.session.get(f"{self._serverRootUrl}/coverage/object")
            codeCoverageValueVectorList = [list(v[coverageTypeIndicator].values())
                                           for v in response.json().values()]
            codeCoverageValueVector = self._flatList(codeCoverageValueVectorList)
            codeCoverageVector = self._convertCodeCoverageValueVectorToCodeCoverageVector(
                codeCoverageValueVector=codeCoverageValueVector)
            return codeCoverageVector
        except Exception as e:
            Logger().info(f"Failed at getting coverage {e.__class__.__name__}")

    def _flatList(self, originList: []):
        flattenedList = []
        for i in originList:
            if isinstance(i, list):
                flattenedList = [*flattenedList, *self._flatList(i)]
            else:
                flattenedList.append(i)
        return flattenedList

    def _convertCodeCoverageValueVectorToCodeCoverageVector(self, codeCoverageValueVector):
        codeCoverageVector = []
        for i in codeCoverageValueVector:
            codeCoverageVector.append(i != 0)

        return codeCoverageVector
