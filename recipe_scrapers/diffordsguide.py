from bs4 import NavigableString, Tag

from ._abstract import CocktailScraper
from ._utils import get_minutes, normalize_string
import json


class DiffordsGuide(CocktailScraper):
    @classmethod
    def host(self):
        return 'diffordsguide.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def ingredients(self):
        ingredients = [normalize_string(i.get_text()) for i in
                       self.soup.find('table', {'class': ['ingredients-table']}).findAll('tr')]
        ingredients = [i for i in ingredients if 'loading...' not in i.lower()]
        return ingredients

    def instructions(self):
        instructions = ''
        for i in self.soup.findAll('h2'):
            if 'how to make' in i.get_text().lower():
                instructions = normalize_string(i.parent.find('p').get_text())
        return instructions

    def garnish(self):
        garnish = ''
        for i in self.soup.findAll('h3'):
            if 'garnish:' in i.get_text().lower():
                garnish = normalize_string(i.parent.find('p').get_text())
        return garnish
