from typing import List
import requests as _requests
import storage
import util.util as _util



class Observer(object):
    webpage: str

    def update(self, new_time: str):
        pass


class ConcreteObserver(Observer):
    def __init__(self, webpage: str,subject):
        self.webpage = webpage
        self.subject = subject
        self.subject.attach(self)

    def update(self, new_time: str):
        print("UPDATED")
        print(self.webpage)
        print(new_time)
