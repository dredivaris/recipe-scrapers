from bs4 import NavigableString, Tag

from ._abstract import CocktailScraper
from ._utils import get_minutes, normalize_string
import json


class PunchDrink(CocktailScraper):
    @classmethod
    def host(self):
        return 'punchdrink.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def ingredients(self):
        ingredients = self.soup.find('ul', {'class': 'direction-list'}).findAll('li')
        return [normalize_string(ingredient.get_text().strip()) for ingredient in ingredients]

    def instructions(self):
        possible_directions = self.soup.find_all('h5')
        instructions = [possible for possible in possible_directions
                        if possible.find(text='Directions')][0]
        instructions = instructions.nextSibling.nextSibling.find_all('li')

        return ' '.join(normalize_string(instruction.get_text()) for instruction in instructions)

    def garnish(self):
        garnish = normalize_string(self.soup.find('p', {'class': 'garn-glass'}).get_text())
        garnish = garnish.split(':')[1].strip()
        return garnish
