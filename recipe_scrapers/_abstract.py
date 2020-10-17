import requests
import re
from lxml import html

from bs4 import BeautifulSoup

from recipe_scrapers._utils import on_exception_return

# some sites close their content for 'bots', so user-agent must be supplied
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
}

# set some cookies to maneuver over:
# - EU Consent in allrecipes.com.br
COOKIES = {
    'euConsentFailed': 'true',
    'euConsentID': 'e48da782-e1d1-0931-8796-d75863cdfa15',
}

GARNISH = re.compile('Garnish:.*')
GLASS = re.compile('Glass:.*')


class AbstractScraper():
    def __getattribute__(self, name):
        """
        Decorate custom methods to handle exceptions as we want and as we
        specify in the "on_exception_return" method decorator

        Do not do this META-decorating on testing so to have better traceback
        """
        if not object.__getattribute__(self, 'testing_mode'):
            to_return = None
            decorated_methods = [
                'title',
                'total_time',
                'instructions',
                'ingredients',
                'links'
            ]
            if name in decorated_methods:
                to_return = ''
            if name == 'total_time':
                to_return = 0
            if name == 'ingredients':
                to_return = []
            if name == 'links':
                to_return = []
            if to_return is not None:
                return on_exception_return(to_return)(object.__getattribute__(self, name))

        return object.__getattribute__(self, name)

    def __init__(self, url, test=False):
        if test:  # when testing, we load a file
            with url:
                self.soup = BeautifulSoup(
                    url.read(),
                    "html.parser"
                )
        else:
            self.soup = BeautifulSoup(
                requests.get(
                    url,
                    headers=HEADERS,
                    cookies=COOKIES
                ).content,
                "html.parser"
            )
        self.testing_mode = test
        self.url = url

    def url(self):
        return self.url

    def host(self):
        """ get the host of the url, so we can use the correct scraper """
        raise NotImplementedError("This should be implemented.")

    def title(self):
        raise NotImplementedError("This should be implemented.")

    def total_time(self):
        """ total time it takes to preparate the recipe in minutes """
        raise NotImplementedError("This should be implemented.")

    def ingredients(self):
        raise NotImplementedError("This should be implemented.")

    def instructions(self):
        raise NotImplementedError("This should be implemented.")

    def ratings(self):
        raise NotImplementedError("This should be implemented.")

    def reviews(self):
        raise NotImplementedError("This should be implemented.")

    def links(self):
        invalid_href = ('#', '')
        links_html = self.soup.findAll('a', href=True)

        return [
            link.attrs
            for link in links_html
            if link['href'] not in invalid_href
        ]

    def reference(self):
        return None

    def rating(self):
        return None

    def can_parse(self):
        return self.ingredients() and self.instructions()

    def directions(self):
        return self.instructions()


class CocktailScraper(AbstractScraper):
    def total_time(self):
        return None

    def garnish(self):
        if self._garnish:
            return self._garnish
        return None

    def description(self):
        return None

    def glass(self):
        return None

    def strip_links(self, element):
        pass

    @staticmethod
    def replace(initial, text, with_text):
        insensitive = re.compile(re.escape(text), re.IGNORECASE)
        return insensitive.sub(with_text, initial)

    @staticmethod
    def strip(initial, of_text):
        return CocktailScraper.replace(initial, of_text, '')

    @staticmethod
    def contains(text, contains):
        if not isinstance(contains, list):
            contains = [contains]
        try:
            text = text.get_text()
        except AttributeError:
            pass

        return any(c.upper() in text.upper() for c in contains)

    @staticmethod
    def find_with_text(node, text, original=None):
        found = node.find(text=text)
        if not found:
            return None

        if original:
            found = CocktailScraper.strip(found, original)
        else:
            found = CocktailScraper.strip(found, text)

        return found
