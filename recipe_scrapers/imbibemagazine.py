from ._abstract import CocktailScraper
from ._utils import normalize_string


class ImbibeMagazine(CocktailScraper):
    @classmethod
    def host(self):
        return 'imbibemagazine.com'

    def title(self):
        return self.soup.find('h1').get_text()

    def list_ingredients(self, current):
        texts = []
        found = set()
        for br in current.findAll('br'):
            prev_str = str(br.previousSibling).strip()
            if prev_str not in found:
                found.add(prev_str)
                texts.append(prev_str)
            next_str = str(br.nextSibling).strip()
            if next_str not in found:
                found.add(next_str)
                texts.append(next_str)
        return texts

    def ingredients(self):
        ingredients_html = self.soup.findAll('div', {'class': ['single-box', 'clearfix', 'entry-content']})[1].findAll('p')[1]
        ingredients = []
        current = ''
        for step in ingredients_html.contents:
            if step.name == 'br':
                if current:
                    ingredients.append(current.strip())
                    current = ''
                continue
            try:
                text = step.get_text()
            except AttributeError:
                text = str(step)
            if text:
                current += text
        if current:
            ingredients.append(current.strip())

        return [normalize_string(ingredient) for ingredient in ingredients]

    def instructions(self):
        instructions = self.soup.findAll('div', {'class': ['single-box', 'clearfix', 'entry-content']})[1].findAll('p')[2].get_text()

        return [instructions]
