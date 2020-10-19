import re

from ._abstract import CocktailScraper, GARNISH, GLASS
from ._utils import normalize_string


class Liquor(CocktailScraper):
    @classmethod
    def host(self):
        return 'liquor.com'

    def title(self):
        title = self.soup.find('h1').get_text()
        return title.replace('How to Make a', '').strip()

    @staticmethod
    def process_ingredient(soup):
        unit = normalize_string(soup.find('div', {'class': 'oz-value'}).get_text())
        ingredient = normalize_string(soup.find('div', {'class': 'x-recipe-ingredient'}).get_text())
        return '{} {}'.format(unit, ingredient).strip()

    def not_garnish_or_glass(self, soup):
        return not soup.find(text=GARNISH) and not soup.find(text=GLASS)

    def ingredients(self):
        ingredient_list = self.soup.find_all('div', {'class': 'x-recipe-unit'})[1:]
        ingredient_list = [self.process_ingredient(ingredient) for ingredient in ingredient_list]

        try:
            if not ingredient_list:
                ingredient_list = self.soup.find(text='INGREDIENTS:')\
                        .parent.parent.parent.parent.find('ul').find_all('li')
                ingredient_list = [normalize_string(i.get_text()) for i in ingredient_list
                                   if self.not_garnish_or_glass(i)]
        except AttributeError:
            ingredient_list = self.soup\
                .find_all('li', {'class': ['simple-list__item', 'ingredient']})
            ingredient_list = [i.get_text().strip() for i in ingredient_list]
        return ingredient_list

    def instructions(self):
        try:
            instructions = [normalize_string(i.get_text()) for i in
                    self.soup.find('div', {'class': 'x-recipe-prep'}).find_all('p')
                    if not i.get_text().startswith('*')]
        except AttributeError:
            try:
                instructions = [self.soup.find(text='PREPARATION:').parent.parent.parent
                                    .get_text().split(':')[1].strip()]
            except AttributeError:
                inst_steps = [i.get_text().strip()
                              for i in self.soup.findAll('li', {'class':['comp']})]
                return ' '.join(inst_steps)

        return instructions

    def garnish(self):
        try:
            return normalize_string(self.soup.find('span', {'class': 'oz-value'}).get_text())
        except AttributeError:
            try:
                garnishes = self.soup.findAll('li', text=GARNISH)
                return ', '.join(i.get_text().split(':')[1].strip() for i in garnishes)
            except AttributeError:
                return None

    def glass(self):
        try:
            return self.soup.find('div', {'class': 'x-recipe-glasstype'}).find('a').get_text()
        except AttributeError:
            return self.soup.find(text=GLASS).parent.get_text().split(':')[1].strip()
