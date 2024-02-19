import unittest
from math import sqrt

from RLEnvForApp.usecase.environment.observationService.converter.FastTextConverter import \
    FastTextConverter
from RLEnvForApp.usecase.environment.observationService.converter.Word2VecConverter import \
    Word2VecConverter


class testW2vInner(unittest.TestCase):
    def setUp(self) -> None:
        self._w2vConverter = Word2VecConverter()
        self._fastConverter = FastTextConverter()

    def test_something(self):
        print("====================================================")
        print("W2V")
        print("====================================================")
        password = self._w2vConverter.convert(stateElement="password", length=300)
        name = self._w2vConverter.convert(stateElement="name", length=300)
        username = self._w2vConverter.convert(stateElement="username", length=300)
        user = self._w2vConverter.convert(stateElement="user", length=300)
        last = self._w2vConverter.convert(stateElement="last", length=300)
        first = self._w2vConverter.convert(stateElement="first", length=300)
        print("inner: ", self._inner(name, name))
        print("first name and last name: ", self._inner(self._sum(last, name),
                                                        self._sum(first, name)))
        print("first name and name: ", self._inner(self._sum(first, name),
                                                   name))
        print("last name and name: ", self._inner(self._sum(last, name),
                                                  name))
        print("username and name: ", self._inner(username, name))
        print("username and first name: ", self._inner(username,
                                                       self._sum(first, name)))
        print("username and last name: ", self._inner(username,
                                                      self._sum(last, name)))

        print("====================================================")
        print("fastText")
        print("====================================================")
        password = self._fastConverter.convert(stateElement="password", length=300)
        name = self._fastConverter.convert(stateElement="name", length=300)
        username = self._fastConverter.convert(stateElement="username", length=300)
        user = self._fastConverter.convert(stateElement="user", length=300)
        last = self._fastConverter.convert(stateElement="last", length=300)
        first = self._fastConverter.convert(stateElement="first", length=300)
        print("inner: ", self._inner(name, name))
        print("first name and last name: ", self._inner(self._sum(last, name),
                                                        self._sum(first, name)))
        print("first name and name: ", self._inner(self._sum(first, name),
                                                   name))
        print("last name and name: ", self._inner(self._sum(last, name),
                                                  name))
        print("username and name: ", self._inner(username, name))
        print("username and first name: ", self._inner(username,
                                                       self._sum(first, name)))
        print("username and last name: ", self._inner(username,
                                                      self._sum(last, name)))

    def _toUnit(self, vec1) -> []:
        value = 0
        vec = []
        for i in vec1:
            value += i*i
        value = sqrt(value)
        for i in vec1:
            vec.append(i/value)
        return vec

    def _inner(self, vec1, vec2) -> float:
        value = 0
        unitVec1 = self._toUnit(vec1)
        unitVec2 = self._toUnit(vec2)
        for a, b in zip(unitVec1, unitVec2):
            value += a*b
        return value

    def _sum(self, vec1, vec2) -> []:
        vec = []
        for a, b in zip(vec1, vec2):
            vec.append(a+b)
        return vec
