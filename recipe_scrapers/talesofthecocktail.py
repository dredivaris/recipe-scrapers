import re

from ._abstract import CocktailScraper, GARNISH
from ._utils import normalize_string

GLASS = re.compile('Glassware:.*')

FILTER_OUT = ['Glassware:', 'Method:', 'Garnish:', 'for garnish']
GARNISH2 = re.compile('.*for garnish')


class TalesOfTheCocktail(CocktailScraper):
    @classmethod
    def host(self):
        return 'talesofthecocktail.org'

    def title(self):
        title = self.soup.find('h1', {'itemprop': 'name'}).get_text()
        return normalize_string(title)

    def ingredients(self):
        ingredients = self.soup.find_all('li', {'itemprop': 'ingredients'})
        return [normalize_string(ingredient.get_text()) for ingredient in ingredients
                if not self.contains(ingredient.get_text(), FILTER_OUT)]

    def instructions(self):
        possible_instructions = self.soup\
            .find('div', {'itemprop': 'recipeInstructions'}).find_all('p')
        instructions = [i for i in possible_instructions if not self.contains(i, FILTER_OUT)]
        return [normalize_string(i.get_text()) for i in instructions]

    def glass(self):
        body = self.soup.find('div', {'itemprop': 'recipeInstructions'})
        return normalize_string(self.find_with_text(body, GLASS, 'Glassware:'))

    def garnish(self):
        body = self.soup.find('div', {'itemprop': 'recipeInstructions'})
        garnish = normalize_string(self.find_with_text(body, GARNISH, 'Garnish:'))

        if not garnish:
            ingredients = self.soup.find('li', {'itemprop': 'ingredients'}).parent
            garnish = self.find_with_text(ingredients, GARNISH2, 'for garnish')
        return normalize_string(garnish)
