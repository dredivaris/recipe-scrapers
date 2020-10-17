from ._abstract import CocktailScraper
from ._utils import normalize_string


class KindredCocktails(CocktailScraper):
    @classmethod
    def host(self):
        return 'kindredcocktails.com'

    def title(self):
        return self.soup.find(id='page-title').get_text().strip()

    def description(self):
        return self.soup.find('div', {'class': ['description']}).get_text().strip()

    def ingredients(self):
        content = self.soup.find('div', {'class': ['node-content']})
        return [normalize_string(i.get_text()) for i in content.findAll('tr')]

    def instructions(self):
        return normalize_string(self.soup.find('div', {'property': ['v:instructions']}).get_text())