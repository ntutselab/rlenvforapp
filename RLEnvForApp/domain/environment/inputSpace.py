import json
import os

from RLEnvForApp.domain.environment.category import (ADDRESS, CITY, CLICK,
                                                     DATE, EMAIL, NAME, NUMBER,
                                                     PASSWORD, PHONE_NUMBER,
                                                     POSTAL_CODE, STRING)

inputTypes = [
    CLICK,
    EMAIL,
    NAME,
    PASSWORD,
    DATE,
    NUMBER,
    PHONE_NUMBER,
    STRING,
    CITY,
    ADDRESS,
    POSTAL_CODE]
inputValues = [[""],
               ["vector@selab.com",
                "Katlyn_Reichel@example.com",
                "Willa.Paucek@example.com"],
               ["Gladyce", "Heathcote", "Pete Kessler"],
               ["password", "BeH_CD67ijJI1OI", "uIhubzQPMWPHasx"],
               ["Mon Sep 11 2023", "2023/05/03", "2023-06-11"],
               ["0.4954917863942683", "8877133361315840", "232.83"],
               ["+567-248-7625", "(566) 882-5462", "758-303-7821"],
               ["dolorem", "Totam officiis consequuntur.",
                   "Repudiandae nam asperiores aut molestiae perspiciatis quaerat quas."],
               ["North Leolachester", "Smithammouth", "North Lestertown"],
               ["2217 Brekke Gateway", "7952 Francisco Via", "873 Alta Falls"],
               ["13700", "38273-9589", "70212"]]


class CategoryListSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if not CategoryListSingleton._instance:
            CategoryListSingleton()
        return CategoryListSingleton._instance

    def __init__(self):
        if CategoryListSingleton._instance:
            raise Exception('only one instance can exist')
        else:
            if os.path.exists('category_extend_list.json'):
                with open('category_extend_list.json', encoding='utf-8') as jsonfile:
                    data = json.load(jsonfile)
                self._categoryList: dict = data['category_extend_list']
            else:
                self._categoryList = {}
                for category in inputTypes:
                    self._categoryList[category] = []

            CategoryListSingleton._instance = self

    def get_category_extend_list(self) -> dict:
        return self._categoryList

    def set_category_extend_list(self, newList):
        self._categoryList = newList
        with open('category_extend_list.json', 'w', encoding='utf-8') as f:
            json.dump({'category_extend_list': newList},
                      f, ensure_ascii=False, indent=4)


class ValueWeightSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if not ValueWeightSingleton._instance:
            ValueWeightSingleton()
        return ValueWeightSingleton._instance

    def __init__(self):
        if ValueWeightSingleton._instance:
            raise Exception('only one instance can exist')
        else:
            if os.path.exists('input_value_probability.json'):
                with open('input_value_probability.json', encoding='utf-8') as jsonfile:
                    data = json.load(jsonfile)
                self._valueWeights = data['weights']
            else:
                self._valueWeights = {}
                for i, category in enumerate(inputTypes):
                    self._valueWeights[category] = [
                        1 / len(inputValues[i]) for _ in inputValues[i]]

            ValueWeightSingleton._instance = self

    def get_value_weights(self) -> dict:
        return self._valueWeights

    def set_value_weights(self, newList):
        self._valueWeights = newList
        with open('input_value_probability.json', 'w', encoding='utf-8') as f:
            json.dump({'weights': newList}, f, ensure_ascii=False, indent=4)
