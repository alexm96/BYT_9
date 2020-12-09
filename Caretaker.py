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
        return json.dumps(observers), json.dumps(self.urls_to_watch)


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

    def add_memento(self, memento_to_add: Memento):
        print(memento_to_add)
        self.saved_mementos.append(memento_to_add)


    def get_memento(self, index: int):
        return self.saved_mementos[index]


if __name__ == '__main__':
    s = Watcher.Watcher()
    o = ObserverDP.ConcreteObserver(webpage="http://www.pja.edu.pl/", subject=s)
    o2 = ObserverDP.ConcreteObserver(webpage="http://www.pja.edu.pl/", subject=s)
    o3 = ObserverDP.ConcreteObserver(webpage="https://www.pja.edu.pl/informatyka/inzynierskie/informacje-ogolne/",
                                     subject=s)
    s.check_pages()
    c = Caretaker("./sample_db.json")
    m = Memento(urls_to_watch=s.urls_to_watch, observers=s.observers)
    c.add_memento(m)
    s.check_pages()
    m2 = Memento(urls_to_watch=s.urls_to_watch, observers=s.observers)

    c.add_memento(m2)

    print(c.serialize())
