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
    WEBPAGE_HEADER = "webpages"
    OBSERVERS_HEADER = "observers"
    # memento of Watcher
    urls_to_watch: {}
    observers: List[_observer.Observer]

    def to_json(self):
        observers = [ob.to_json() for ob in self.observers]
        print(observers)
        return observers, self.urls_to_watch


class Caretaker(object):
    saved_mementos: List
    save_path: str  # relative directory to save stuff

    def __init__(self, save_path: str, saved_mementos=None, watcher=None):
        if saved_mementos is None:
            saved_mementos = []
        self.watcher = watcher
        self.save_path = save_path
        self.saved_mementos = saved_mementos

    def set_watcher(self, watcher):
        self.watcher = watcher

    def serialize(self):  # memento -> file
        to_write = open(self.save_path, "w")
        to_return = []
        for item in self.saved_mementos:
            item1, item2 = item.to_json()
            to_return.append(
                {
                    "{WEBPAGE_HEADER}".format(
                        WEBPAGE_HEADER=Memento.WEBPAGE_HEADER
                    ): item2,
                    "{OBSERVERS_HEADER}".format(
                        OBSERVERS_HEADER=Memento.OBSERVERS_HEADER
                    ): item1,
                }
            )
        json.dump(to_return, fp=to_write)

    @staticmethod
    def deserialize(save_path: str):
        memento_list = []
        file_to_load = open(save_path)
        theoretical_list = json.load(file_to_load)
        for item in theoretical_list:  # multiple mementos , file->memento
            list_of_observers = list(
                map(
                    lambda inner_item: ObserverDP.ConcreteObserver(
                        webpage=inner_item, subject=None
                    ),
                    [
                        value["{}".format(ObserverDP.ConcreteObserver.json_key)]
                        for value in item.get(Memento.OBSERVERS_HEADER)
                    ],
                )
            )
            list_of_webpages = {
                key: value for key, value in item.get(Memento.WEBPAGE_HEADER).items()
            }

            memento_to_add = Memento(
                urls_to_watch=list_of_webpages, observers=list_of_observers
            )
            memento_list.append(memento_to_add)
        return Caretaker(save_path=save_path, watcher=None, saved_mementos=memento_list)

    def add_memento(self, memento_to_add: Memento):
        self.saved_mementos.append(memento_to_add)

    def get_memento(self):
        return self.saved_mementos[len(self.saved_mementos) - 1]


if __name__ == "__main__":
    """
    s = Watcher.Watcher()
    o = ObserverDP.ConcreteObserver(webpage="http://www.pja.edu.pl/", subject=s)
    o2 = ObserverDP.ConcreteObserver(webpage="https://www.olx.pl/", subject=s)
    s.check_pages()
    c = Caretaker("./sample_db.json")
    m=s.generate_memento()
    c.add_memento(m)
    print(c.serialize())
    """
    w = Watcher.Watcher()
    c = Caretaker.deserialize(save_path="./sample_db.json")
    c.set_watcher(w)
    w.restore(c.get_memento())
    w.check_pages()

    c.serialize()
