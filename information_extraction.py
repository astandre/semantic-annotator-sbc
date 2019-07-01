from bs4 import BeautifulSoup
from requests_html import HTMLSession


class InformationExtraction:
    session = HTMLSession()

    def get_page(self, url):
        r = self.session.get(
            "https://milhojas.is/612540-odebretch-y-otras-multinacionales-pusieron-presidente-en-ecuador.html")
        raw = r.html.html

        soup = BeautifulSoup(raw, 'html.parser')
        print(soup.get_text())

    def get_words_strong(self):
        pass

    def delete_html(self):
        pass
