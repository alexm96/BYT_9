from json import JSONEncoder
from typing import List
import requests as _requests

import util.util as _util
import json


class Observer(object):
    # pseudo interface
    webpage: str
    json_key: str

    def update(self, new_time: str):
        pass

    def to_json(self):
        pass


class ConcreteObserver(Observer):
    json_key = "webpage"

    def __init__(self, webpage: str, subject=None):
        super().__init__()
        self.webpage = webpage
        self.subject = subject
        if subject is not None:
            self.subject.attach(
                self
            )  # if none, means deserialization and being restored through memento?
        self.json_key = "webpage"

    def update(self, new_time: str):
        print(
            "NOTE:{WEBPAGE} was updated with {NEW_TIME}".format(
                WEBPAGE=self.webpage, NEW_TIME=new_time
            )
        )

    def to_json(self):
        print(ConcreteObserver.json_key)
        return {"{}".format(ConcreteObserver.json_key): self.webpage}
