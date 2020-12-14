import unittest
import Watcher
import Caretaker
from unittest.mock import MagicMock
from util import util
import ObserverDP
import json


class TestSomeMethods(unittest.TestCase):
    '''
    Note, only testing single memento serial/deserial (however multiple mementos are supported and serialized/deserialized correctly)
    '''
    file_path = "../sample_db_test.json"
    webpage_to_test = "http://www.pja.edu.pl/"
    w = Watcher.Watcher()
    o = ObserverDP.ConcreteObserver(webpage=webpage_to_test, subject=w)
    c = Caretaker.Caretaker(save_path=file_path, watcher=w)

    def test_serialize(self):
        self.c.add_memento(self.w.generate_memento())
        self.c.serialize()
        serialized = open(file=self.file_path)
        json_content = json.load(serialized)[0]
        self.assertEqual(
            json_content.get("webpages")[self.webpage_to_test],
            self.w.urls_to_watch.get(self.webpage_to_test),
        )  # serialized correctly if both match
        self.assertEqual(
            len(self.w.observers), len(json_content.get("observers"))
        )  # number of observers matches
        serialized.close()

    def test_deserialize(self):
        '''
        Note, only tests single memento, but can pass specific index into get_memento if you want to try others
        :return:
        '''
        new_watcher = Watcher.Watcher()
        new_caretaker = Caretaker.Caretaker.deserialize(save_path=self.file_path)
        new_caretaker.set_watcher(
            new_watcher
        )  # can't deserialize specific watcher, rather have to create new one then restore from memento
        new_watcher.restore(
            new_caretaker.get_memento()
        )  # Restoring from most recent state
        self.assertEqual(self.w.observers[0].webpage, new_watcher.observers[0].webpage)

    def test_update(self):
        util.get_last_modified = MagicMock(
            return_value="Fri, 11 Dec 2020 23:08:20 GMT"
        )  # mock dif response
        sample_watcher = Watcher.Watcher()
        sample_observer = ObserverDP.ConcreteObserver(
            webpage=self.webpage_to_test, subject=sample_watcher
        )
        self.assertEqual("", sample_watcher.urls_to_watch.get(self.webpage_to_test))
        sample_watcher.check_pages()
        self.assertEqual(
            sample_watcher.urls_to_watch.get(self.webpage_to_test),
            "Fri, 11 Dec 2020 23:08:20 GMT",
        )


if __name__ == "__main__":
    unittest.main()
