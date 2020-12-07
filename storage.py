import json
from dataclasses import dataclass
from typing import Set, List


@dataclass
class SimpleState:
    # will be originator saves mementos as json
    webpage: str
    last_modified: str

    def __init__(self, json_item: dict):
        self.webpage = json_item.get("webpage")
        self.last_modified = json_item.get("last-modified")

    def send_to_memento(self) -> {}:
        # save state
        return {
            "webpage": self.webpage,
            "last-modified": self.last_modified,
        }  # memento object in the form of a json

    def get_from_memento(self, mement: dict):
        self.webpage = mement.get("webpage")
        self.last_modified = mement.get("last-modified")

    @staticmethod
    def deserialize(some_json_item: dict):
        # restore from state
        try:
            return SimpleState(some_json_item)
        except:
            return None


class SimpleStorage:
    # pretty much a caretaker
    state_store: List[dict]

    def __init__(self, path: str = "./sample_db.json"):
        """
        :param path: simple string path to db file
        """
        self.save_path = path
        self.state_store = []
        self.deserialize()

    def load_file_to_json(self) -> {}:
        with open(self.save_path) as json_file:
            return json.load(json_file)

    def deserialize(self):
        json_items = self.load_file_to_json()
        for item in json_items:
            try:
                self.state_store.append(item)
            except:
                print("Deserialization error")
                return None
    def reduce_to_webpages(self):
        return List[map(lambda x: x["webpage"],self.state_store)]
    def serialize(self):
        file_to_write = open(self.save_path, "w")
        file_to_write.write(json.dumps(self.state_store))

    def add_memento(self, some_json: dict):
        exists = False
        for memento in self.state_store:
            if SimpleStorage.check_webpage_equality(
                some_json=some_json, memento=memento
            ):
                exists = True
                if SimpleStorage.check_time_equality(
                    some_json=some_json, memento=memento
                ):

                    break  # already in list , ignore
                else:
                    memento["last-modified"] = some_json.get(
                        "last-modified"
                    )  # update memento saved in list

        if not exists:
            self.state_store.append(some_json)  # new memento item

    @staticmethod
    def check_webpage_equality(some_json: dict, memento: dict):
        return memento.get("webpage") == some_json.get("webpage")

    @staticmethod
    def check_time_equality(some_json: dict, memento: dict):
        return memento.get("last-modified") == some_json.get("last-modified")

    def get_memento(self, webpage_name: str) -> dict:
        for item in self.state_store:
            if item.get("webpage") == webpage_name:
                return item
        return None


if __name__ == "__main__":
    s = SimpleStorage()
    for item in s.state_store:
        print(item)
    s.add_memento(
        some_json={
            "webpage": "http://google.com",
            "last-modified": "Mon, 07 Dec 2020 14:30:45 GMT",
        }
    )
    for item in s.state_store:
        print(item)
