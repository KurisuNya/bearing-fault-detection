from abc import ABCMeta, abstractmethod


class Observable(metaclass=ABCMeta):
    @abstractmethod
    def attach(self, observers):
        pass

    @abstractmethod
    def detach(self, observers):
        pass

    @abstractmethod
    def notify(self, keys):
        pass


class Observer(metaclass=ABCMeta):
    @abstractmethod
    def update(self, observable, key):
        pass


class ConditionalObserver(Observer):
    def __init__(self, condition, update):
        self.__condition = condition
        self.__update = update

    def update(self, observable, key):
        if self.__condition(observable, key):
            self.__update(observable, key)
