import re

from ._abstract import CocktailScraper, GARNISH, GLASS
from ._utils import normalize_string


class Saveur(CocktailScraper):
    @classmethod
    def host(self):
        return 'saveur.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def ingredients(self):
        ingredients = self.soup.findAll('li', {'class': ['ingredient']})
        return [normalize_string(i.get_text()) for i in ingredients
                if 'for garnish' not in i.get_text()]

    def instructions(self):
        instruction_list = [i.get_text().strip()
                            for i in self.soup.findAll('li', {'class': ['instruction']})]
        return ' '.join(instruction_list)

    def garnish(self):
        ingredients = self.soup.findAll('li', {'class': ['ingredient']})
        for i in ingredients:
            i = normalize_string(i.get_text())
            if 'for garnish' in i:
                return i.replace(', for garnish', '').replace('for garnish', '').strip()
        return None
