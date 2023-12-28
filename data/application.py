import functools


class App:

    def __init__(self):
        self.catalog = {}

    def component(self, f):
        name = f.__name__
        if name in self.catalog.keys():
            raise RuntimeError('Already Existed.')


class Component:

    def __init__(self):
        self._finished = False
        self._instance = 1
        pass

    def register(self, f):
        self.f = f
        print('here')

    def dependency_injection(self):
        self._finished = True

    @property
    def finished(self):
        return self._finished

    @property
    def instance(self):
        return self._instance

