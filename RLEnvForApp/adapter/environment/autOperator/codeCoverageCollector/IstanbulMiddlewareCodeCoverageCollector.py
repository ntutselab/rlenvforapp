import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from RLEnvForApp.logger.logger import Logger
from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import \
    ICodeCoverageCollector
from RLEnvForApp.usecase.environment.autOperator.dto.CodeCoverageDTO import \
    CodeCoverageDTO


class IstanbulMiddlewareCodeCoverageCollector(ICodeCoverageCollector):
    def __init__(self, serverIp, serverPort):
        super().__init__()
        self._serverRootUrl = f'http://{serverIp}:{serverPort}'
        self.session = self._requests_retry_session()

    def get_code_coverage_dt_os(self) -> [CodeCoverageDTO]:
        codeCoverageDTOs = []
        codeCoverageDTOs.append(
            CodeCoverageDTO(
                codeCoverageType="statement coverage",
                codeCoverageVector=self._get_code_coverage_vector('s')))
        codeCoverageDTOs.append(
            CodeCoverageDTO(
                codeCoverageType="branch coverage",
                codeCoverageVector=self._get_code_coverage_vector('b')))
        return codeCoverageDTOs

    def reset_code_coverage(self):
        try:
            # istanbul allows reset on GET as well
            # so here we simply use GET to reset the coverage
            response = self.session.get(
                f"{self._serverRootUrl}{'/coverage/reset'}")
        except Exception as e:
            Logger().info(
                f"Failed at resetting coverage {e.__class__.__name__}")
        else:
            if response.status_code != requests.codes.ok:
                raise Exception('Reset coverage error!')

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

    def _get_code_coverage_vector(self, coverageTypeIndicator):
        try:
            # return global coverage object on /coverage/object as JSON
            # for more info, consult the istanbul-middleware utils docs
            response = self.session.get(
                f"{self._serverRootUrl}{'/coverage/object'}")
            codeCoverageValueVectorList = [list(v[coverageTypeIndicator].values())
                                           for v in response.json().values()]
            codeCoverageValueVector = self._flat_list(
                codeCoverageValueVectorList)
            codeCoverageVector = self._convert_code_coverage_value_vector_to_code_coverage_vector(
                codeCoverageValueVector=codeCoverageValueVector)
            return codeCoverageVector
        except Exception as e:
            Logger().info(f"Failed at getting coverage {e.__class__.__name__}")

    def _flat_list(self, originList: []):
        flattenedList = []
        for i in originList:
            if isinstance(i, list):
                flattenedList = [*flattenedList, *self._flat_list(i)]
            else:
                flattenedList.append(i)
        return flattenedList

    def _convert_code_coverage_value_vector_to_code_coverage_vector(
            self, codeCoverageValueVector):
        codeCoverageVector = []
        for i in codeCoverageValueVector:
            codeCoverageVector.append(i != 0)

        return codeCoverageVector
