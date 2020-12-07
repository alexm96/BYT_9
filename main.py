import ObserverDP as _observer
import Watcher
'''
Necessary stuff,
http.client.HTTPConnection instead of urlconnection


'''

def main():
    subject=Watcher.Watcher()

    observer1=_observer.ConcreteObserver(webpage="http://www.pja.edu.pl/",subject=subject)

main()