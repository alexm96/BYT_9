import ObserverDP as _observer
import Watcher
'''
Necessary stuff,
http.client.HTTPConnection instead of urlconnection


'''

def main():
    subject=Watcher.Watcher()
    observer1=_observer.ConcreteObserver(webpage="http://www.pja.edu.pl/",subject=subject)
    observer2 = _observer.ConcreteObserver(webpage="http://www.google.com", subject=subject)
    print(subject.urls_to_watch)
main()