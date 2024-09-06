import json
import os

from RLEnvForApp.usecase.environment.autOperator.codeCoverageCollector.ICodeCoverageCollector import ICodeCoverageCollector
from .IstanbulMiddlewareCodeCoverageCollector import IstanbulMiddlewareCodeCoverageCollector

class CodeCoverageCollectorFactory:
    strategy_name_mapping_table = {
        "istanbul-middleware": IstanbulMiddlewareCodeCoverageCollector,
    }

    def __init__(self):
        self.config = self._get_configuration()
        

    def _get_configuration(self) -> dict:
        if os.path.exists("code_coverage_collector_strategy.json"):
            with open("code_coverage_collector_strategy.json", "r") as data:
                return json.load(data)
        return {}
    
    def _get_strategy_name(self, server_name: str) -> str:
        return self.config[server_name]

    def _get_collector(self, strategy_name: str) -> ICodeCoverageCollector:
        return self.strategy_name_mapping_table[strategy_name]

    # TODO: code coverage collector不見得是用serverIp, serverPort (這是Istanbul Middleware用的)來拿，需要把這兩個參數封裝起來
    def createCollector(self, server_name: str, serverIp, serverPort) -> ICodeCoverageCollector:
        strategy_name = self._get_strategy_name(server_name)
        collector = self._get_collector(strategy_name)
        return collector(serverIp, serverPort)
