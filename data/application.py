import logging
from typing import Dict, Type, Callable


class Component:

    instance: Type[object]
    name: str
    finished: bool
    callback: Callable

    def __init__(self, name, callback):
        self.finished = False
        self.name = name
        self.instance = None
        self.callback = callback

    def commit_injection(self):
        # should inject dependencies.
        # get instance() -> + setter(). consider di() for common.
        self.finished = True

    def init_instance(self):
        self.instance = self.callback()

    def get_instance(self):
        if self.instance is None:
            raise RuntimeError('Not Initialized.')
        return self.instance

    def is_injection_completed(self):
        return self.finished


class ContextManager:

    components: Dict[str, Component]
    instance = None

    @classmethod
    def create(cls):
        if ContextManager.instance is not None:
            return ContextManager.instance
        self = cls.__new__(ContextManager)
        self.components = {}

        return self

    def __init__(self):
        raise RuntimeError('not implemented. please you create() instead.')

    def add_component(self, com: Component) -> None:
        name = com.name
        if name in self.components.keys():
            raise RuntimeError('Already Registered. please check your config.')
        self.components[com.name] = com
        logging.info(f'Component {name} are registered successfully.')
        print(f'Component {name} are registered successfully.')

    def init_components(self):
        for name, com in self.components.items():
            com.init_instance()

    def inject(self):
        logging.info('start to dependency injection.')
        for name, com in self.components.items():
            self.__inject_each(com)

        self.__valid_injection()

        logging.info('dependency injection are completed successfully.')
        print('dependency injection are completed successfully.')

    def __inject_each(self, com):
        for k, v in com.get_instance().__dict__.items():
            if v is not None:
                continue

            new_value = self.components.get(k)
            self.__setattr__(k, new_value)

        ret = True
        for v in com.get_instance().__dict__.values():
            ret = ret and v is not None

        if ret:
            com.commit_injection()

    def __valid_injection(self):
        ret = True
        for com in self.components.values():
            ret = ret and com.is_injection_completed()
        if not ret:
            raise RuntimeError('There is something wrong for dependency injection on ContextManager.')


CONTEXT_MANAGER = ContextManager.create()


def component(f):
    com = Component(f.__name__, f)
    CONTEXT_MANAGER.add_component(com)
    return f


''' Example
@component
def a():
    instance = Hello()
    return instance
    

CONTEXT_MANAGER.init_components({})
CONTEXT_MANAGER.inject()
'''