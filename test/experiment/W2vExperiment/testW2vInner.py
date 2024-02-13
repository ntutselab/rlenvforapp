import unittest
from math import sqrt

from RLEnvForApp.usecase.environment.observationService.converter.FastTextConverter import \
    FastTextConverter
from RLEnvForApp.usecase.environment.observationService.converter.Word2VecConverter import \
    Word2VecConverter


class TestW2vInner(unittest.TestCase):
    def set_up(self) -> None:
        self._w2v_converter = Word2VecConverter()
        self._fast_converter = FastTextConverter()

    def test_something(self):
        print("====================================================")
        print("W2V")
        print("====================================================")
        password = self._w2v_converter.convert(
            state_element="password", length=300)
        name = self._w2v_converter.convert(state_element="name", length=300)
        username = self._w2v_converter.convert(
            state_element="username", length=300)
        user = self._w2v_converter.convert(state_element="user", length=300)
        last = self._w2v_converter.convert(state_element="last", length=300)
        first = self._w2v_converter.convert(state_element="first", length=300)
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
        password = self._fast_converter.convert(
            state_element="password", length=300)
        name = self._fast_converter.convert(state_element="name", length=300)
        username = self._fast_converter.convert(
            state_element="username", length=300)
        user = self._fast_converter.convert(state_element="user", length=300)
        last = self._fast_converter.convert(state_element="last", length=300)
        first = self._fast_converter.convert(state_element="first", length=300)
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

    def _to_unit(self, vec1) -> []:
        value = 0
        vec = []
        for i in vec1:
            value += i * i
        value = sqrt(value)
        for i in vec1:
            vec.append(i / value)
        return vec

    def _inner(self, vec1, vec2) -> float:
        value = 0
        unit_vec1 = self._to_unit(vec1)
        unit_vec2 = self._to_unit(vec2)
        for a, b in zip(unit_vec1, unit_vec2):
            value += a * b
        return value

    def _sum(self, vec1, vec2) -> []:
        vec = []
        for a, b in zip(vec1, vec2):
            vec.append(a + b)
        return vec
