import re

from ._abstract import CocktailScraper, GARNISH, GLASS
from ._utils import normalize_string


class Chowhound(CocktailScraper):
    @classmethod
    def host(self):
        return 'chowhound.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def ingredients(self):
        ingredients = self.soup.find('div', {'class': ['freyja_box81']}).findAll('li')
        return [normalize_string(i.get_text()) for i in ingredients
                if 'for garnish' not in i.get_text()]

    def instructions(self):
        instructions = self.soup.find('div', {'class': ['fr_instruction_rec']}).findAll('li')
        return ' '.join(normalize_string(i.get_text().strip().lstrip('0123456789.- '))
                        for i in instructions)

    def garnish(self):
        instructions = self.soup.find('div', {'class': ['freyja_box81']}).findAll('li')
        for i in instructions:
            i = normalize_string(i.get_text())
            if 'for garnish' in i:
                return i.replace(', for garnish', '').replace('for garnish', '').strip()
        return None
