from json import JSONEncoder
from typing import List
import requests as _requests

import util.util as _util
import json


class Observer(object):
    # pseudo interface
    webpage: str

    def update(self, new_time: str):
        pass

    def to_json(self):
        pass


class ConcreteObserver(Observer):
    def __init__(self, webpage: str, subject=None):
        super().__init__()
        self.webpage = webpage
        self.subject = subject
        if subject is not None:
            self.subject.attach(
                self
            )  # if none, means deserialization and being restored through memento?

    def update(self, new_time: str):
        print("UPDATED")
        print(self.webpage)
        print(new_time)

    def to_json(self):
        return {"webpage": self.webpage}
