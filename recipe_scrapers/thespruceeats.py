from ._abstract import CocktailScraper
from ._utils import normalize_string


class TheSpruceEats(CocktailScraper):
    @classmethod
    def host(self):
        return 'thespruceeats.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def ingredients(self):
        ingredients = self.soup.findAll('li', {'class': ['ingredient']})
        return [normalize_string(ingredient.get_text()) for ingredient in ingredients
                if 'garnish:' not in normalize_string(ingredient.get_text()).lower()]

    def instructions(self):
        return ' '.join(normalize_string(i.get_text()) for i in self.soup.find('ol').findAll('li'))

    def garnish(self):
        garnishes = self.soup.findAll('li', {'class': ['ingredient']})
        return [normalize_string(ingredient.get_text().lower().replace('garnish:', ''))
                for ingredient in garnishes
                if 'garnish:' in normalize_string(ingredient.get_text()).lower()]

