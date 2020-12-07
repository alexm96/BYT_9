import http.client
import requests as _requests
import util.util as _util
'''
Necessary stuff,
http.client.HTTPConnection instead of urlconnection


'''

def main():
    url=("http://www.pja.edu.pl/")
    response=_requests.get(url=url)
    print(_util.get_last_modified(some_response=response))
main()