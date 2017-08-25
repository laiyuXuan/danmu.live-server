import guessit
import requests
from bs4 import BeautifulSoup

ACPLAY_API_URL = "http://acplay.net/api/v1/match?hash=0&length=5&duration=0&fileName="


class NameFinder():
    def guess_it(self, filename):
        return guessit.guessit(filename)

    def query_acplay(self, filename):
        headers = {'ACCEPT': 'text/xml'}
        r = requests.get(ACPLAY_API_URL + filename, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        matches = soup.findAll('match')
        if matches.__len__() == 0:
            return None
        return matches[0]['animetitle']
