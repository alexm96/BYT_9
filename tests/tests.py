import unittest
import Watcher
import Caretaker
from unittest.mock import MagicMock
from util import  util
import ObserverDP
class TestSomeMethods(unittest.TestCase):
    file_path="../sample_db_test.json"
    webpage_to_test="http://www.pja.edu.pl/"
    def test_serialize(self):
        w=Watcher.Watcher()
        o= ObserverDP.ConcreteObserver(webpage=self.webpage_to_test, subject=w)
        c=Caretaker.Caretaker(save_path=self.file_path,watcher=w)
        c.add_memento(w.generate_memento())
        c.serialize()
        serialized=open(file=self.file_path)
        self.assertIsNotNone(serialized)
        serialized.close()
    def test_deserialize(self):
        w = Watcher.Watcher()
        c = Caretaker.Caretaker.deserialize(save_path=self.file_path)
        c.set_watcher(w)  # can't deserialize specific watcher, rather have to create new one then restore from memento
        w.restore(c.get_memento())  # Restoring from most recent state
        self.assertEqual(w.observers[0].webpage,"http://www.pja.edu.pl/")
    def test_update(self):
        util.get_last_modified=MagicMock(return_value="Fri, 11 Dec 2020 23:08:20 GMT") # mock dif response
        w = Watcher.Watcher()
        o=ObserverDP.ConcreteObserver(webpage=self.webpage_to_test,subject=w)
        self.assertEqual("",w.urls_to_watch.get(self.webpage_to_test))
        w.check_pages()
        self.assertEqual(w.urls_to_watch.get(self.webpage_to_test),"Fri, 11 Dec 2020 23:08:20 GMT")
if __name__ == '__main__':
    unittest.main()