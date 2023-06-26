from typing import Any, Callable, Protocol
from dataclasses import field


class Observable:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, property_name):
        print("[NOTIFY]")
        for observer in self._observers:
            observer.update(self, property_name)


class Observer(Protocol):
    def update(self, observable, property_name):
        ...
