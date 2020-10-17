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

    # def list_ingredients(self, current):
    #     texts = []
    #     found = set()
    #     for br in current.findAll('br'):
    #         prev_str = str(br.previousSibling).strip()
    #         if prev_str not in found:
    #             found.add(prev_str)
    #             texts.append(prev_str)
    #         next_str = str(br.nextSibling).strip()
    #         if next_str not in found:
    #             found.add(next_str)
    #             texts.append(next_str)
    #     return texts

    def ingredients(self):
        content = self.soup.find('div', {'class': ['node-content']})
        return [normalize_string(i.get_text()) for i in content.findAll('tr')]

    def instructions(self):
        return normalize_string(self.soup.find('div', {'property': ['v:instructions']}).get_text())

    def glass(self):
        tools = self.soup.findAll('ul', {'class': ['ingredients__tools']})[0].findAll('li', {'class': ['ingredients__item']})
        for tool in tools:
            if 'glass' in tool.text.strip().lower():
                return normalize_string(tool.text.split(':')[1])
        return ''

    def garnish(self):
        tools = self.soup.findAll('ul', {'class': ['ingredients__tools']})[0].findAll('li', {'class': ['ingredients__item']})
        for tool in tools:
            if 'garnish' in tool.text.strip().lower():
                return normalize_string(tool.text.split(':')[1])
        return ''
