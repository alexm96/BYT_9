import json
from typing import List

import ObserverDP
import Watcher
from dataclasses import dataclass
from typing import List
import dataclasses
import ObserverDP as _observer


@dataclass
class Memento(object):
    # memento of Watcher
    urls_to_watch: {}
    observers: List[_observer.Observer]

    def to_json(self):
        observers = [ob.to_json() for ob in self.observers]
        return observers, self.urls_to_watch


class Caretaker(object):
    saved_mementos: List
    save_path: str  # relative directory to save stuff

    def __init__(self, save_path: str, watcher=None):
        self.watcher = watcher
        self.save_path = save_path
        self.saved_mementos = []

    def serialize(self):
        to_write = open(self.save_path, "w")
        to_return = []
        for item in self.saved_mementos:
            item1, item2 = item.to_json()
            to_return.append({
                "webpages": item2,
                "observers": item1
            })
        to_write.write(json.dumps(to_return))
    @staticmethod
    def deserialize(save_path:str):
        file_to_load=open(save_path)
        theoretical_list=json.load(file_to_load)
        for item in theoretical_list:
            for inner_item in item.get("observers"):
                print(inner_item)

    def add_memento(self, memento_to_add: Memento):
        self.saved_mementos.append(memento_to_add)


    def get_memento(self):
        return self.saved_mementos.pop()


if __name__ == '__main__':

    s = Watcher.Watcher()
    o = ObserverDP.ConcreteObserver(webpage="http://www.pja.edu.pl/", subject=s)
    o2 = ObserverDP.ConcreteObserver(webpage="https://www.olx.pl/", subject=s)
    s.check_pages()
    c = Caretaker("./sample_db.json")
    m = Memento(urls_to_watch=s.urls_to_watch, observers=s.observers)
    c.add_memento(m)
    print(c.serialize())

    Caretaker.deserialize("./sample_db.json")