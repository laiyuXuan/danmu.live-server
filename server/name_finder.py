import guessit
import requests
from bs4 import BeautifulSoup
from server import app


class NameFinder():
    def guess_it(self, filename):
        return guessit.guessit(filename)

    def query_acplay(self, filename):
        headers = {'ACCEPT': 'text/xml'}
        r = requests.get(app.config['ACPLAY_API_URL'] + filename, headers=headers)
        soup = BeautifulSoup(r.text, 'lxml')
        matches = soup.findAll('match')
        if matches.__len__() == 0:
            return None
        return matches[0]['animetitle']
