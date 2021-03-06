import threading
import time
from typing import List
import requests as _requests
import copy
import util.util as _util
import ObserverDP as _observer
import Caretaker
from Caretaker import Memento


class Watcher():
    # Originator for memento + watcher for Observer
    urls_to_watch: {}
    observers: List[_observer.Observer]

    def __init__(self):
        super().__init__()
        self.urls_to_watch = {}
        self.observers = []


    def generate_memento(self):

        return Memento(
            urls_to_watch=copy.deepcopy(self.urls_to_watch),
            observers=copy.deepcopy(self.observers),
        )

    def restore(self, memento: Caretaker.Memento):
        self.urls_to_watch = copy.deepcopy(memento.urls_to_watch)

        for observer in memento.observers:
            self.attach(observer)

    def attach(self, observer: _observer):
        self.observers.append(observer)
        self.add_webpage(observer.webpage)

    def notify_for_webpage(self, webpage: str, update_time: str):
        for observer in self.observers:
            if observer.webpage == webpage:
                observer.update(new_time=update_time)

    def add_webpage(self, webpage_to_add: str):
        if webpage_to_add not in self.urls_to_watch:
            self.urls_to_watch[webpage_to_add] = ""
        else:
            print("{webpage} is already being watched, was not added".format(webpage=webpage_to_add))

    def webpage_differs(self, webpage: str, update_time: str) -> bool:
        return self.urls_to_watch.get(webpage) != update_time

    def check_pages(self):
        for webpage in self.urls_to_watch:
            response = _requests.get(url=webpage)
            new_time = _util.get_last_modified(some_response=response)
            if self.webpage_differs(webpage, new_time):
                self.urls_to_watch[webpage] = new_time
                self.notify_for_webpage(webpage=webpage, update_time=new_time)
