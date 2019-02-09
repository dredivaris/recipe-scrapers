import re

from bs4 import NavigableString, Tag

from ._abstract import CocktailScraper
from ._utils import get_minutes, normalize_string
import json

GARNISH = re.compile('Garnish:.*')


class SeriousEats(CocktailScraper):
    @classmethod
    def host(self):
        return 'seriouseats.com'

    def title(self):
        title = self.soup.find('h1', {'class': 'recipe-title'}).get_text()
        return normalize_string(self.strip(title, 'recipe'))

    def ingredients(self):
        ingredients = self.soup.find_all('li', {'class': 'ingredient'})
        return [normalize_string(ingredient.get_text()) for ingredient in ingredients
                if not self.contains(ingredient.get_text(), 'Garnish:')]

    def instructions(self):
        possible_instructions = self.soup\
            .find('ol', {'class': 'recipe-procedures-list'})\
            .find_all('div', {'class': 'recipe-procedure-text'})

        return [normalize_string(possible.get_text()) for possible in possible_instructions]

    def garnish(self):
        garnish = self.soup.find('div', {'class': 'recipe-ingredients'}).find(text=GARNISH)
        if not garnish:
            return None
        garnish = self.strip(garnish, 'Garnish:').strip()
        return normalize_string(garnish)
