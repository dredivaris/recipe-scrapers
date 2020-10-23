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

    def _fallback_ingredients(self):
        ingredients = []
        current_ingredient = ''
        try:
            for ingredient in self._get_fallback_content()[1]:
                if ingredient.name and ingredient.name == 'br':
                    if current_ingredient:
                        ingredients.append(current_ingredient)
                        current_ingredient = ''
                elif ingredient.name and ingredient.name == 'a':
                    current_ingredient += ingredient.get_text()
                else:
                    l = ingredient.lower()
                    if 'tools:' not in l and 'glass:' not in l and 'garnish:' not in l:
                        current_ingredient += ingredient.lstrip()
        except:
            ingredients = []
            current_ingredient = ''
            for ingredient in self._get_fallback_content()[2]:
                if ingredient.name and ingredient.name == 'br':
                    if current_ingredient:
                        ingredients.append(current_ingredient)
                        current_ingredient = ''
                elif ingredient.name and ingredient.name == 'a':
                    current_ingredient += ingredient.get_text()
                else:
                    l = ingredient.lower()
                    if 'tools:' not in l and 'glass:' not in l and 'garnish:' not in l:
                        current_ingredient += ingredient.lstrip()
            if ingredients:
                self.is_fallback_v2 = True
        return [normalize_string(i) for i in ingredients]

    def _fallback_garnish(self):
        try:
            for ingredient in self._get_fallback_content()[1]:
                if ingredient.name and ingredient.name == 'br':
                    continue
                elif ingredient.name and ingredient.name == 'a':
                    continue
                else:
                    l = ingredient.lower()
                    if 'garnish:' in l:
                        return normalize_string(l.replace('garnish:', ''.strip()))
        except:
            for ingredient in self._get_fallback_content()[2]:
                if ingredient.name and ingredient.name == 'br':
                    continue
                elif ingredient.name and ingredient.name == 'a':
                    continue
                else:
                    l = ingredient.lower()
                    if 'garnish:' in l:
                        return normalize_string(l.replace('garnish:', ''.strip()))

        return ''

    def _fallback_glass(self):
        try:
            for ingredient in self._get_fallback_content()[1]:
                if ingredient.name and ingredient.name == 'br':
                    continue
                elif ingredient.name and ingredient.name == 'a':
                    continue
                else:
                    l = ingredient.lower()
                    if 'glass:' in l:
                        return normalize_string(l.replace('glass:', ''.strip()))
        except:
            for ingredient in self._get_fallback_content()[2]:
                if ingredient.name and ingredient.name == 'br':
                    continue
                elif ingredient.name and ingredient.name == 'a':
                    continue
                else:
                    l = ingredient.lower()
                    if 'glass:' in l:
                        return normalize_string(l.replace('glass:', ''.strip()))

        return ''

    def ingredients(self):

        try:
            ingredients_html = self.soup.findAll('div', {'class': ['single-box', 'clearfix', 'entry-content']})[1].findAll('p')[1]
        except IndexError:
            try:
                ingredients_html = self.soup\
                    .findAll('ul', {'class': ['ingredients__ingredients']})[0]
            except IndexError:
                return self._fallback_ingredients()
            ingredients = [j.text.strip() for j in ingredients_html.findAll('li')]
            return [normalize_string(ingredient) for ingredient in ingredients]
        else:
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

        if not ingredients:
            return self._fallback_ingredients()

        return [normalize_string(ingredient) for ingredient in ingredients]

    def instructions(self):
        try:
            instructions = self.soup\
            .findAll('div', {'class': ['single-box', 'clearfix', 'entry-content']})[1]\
            .findAll('p')[2].get_text()
        except IndexError:
            try:
                instructions = self.soup.findAll(
                    'div', {'class': ['preparation__content']})[0].get_text().strip()
            except IndexError:
                self.ingredients()
                if getattr(self, 'is_fallback_v2', False):
                    return normalize_string(self._get_fallback_content()[3].get_text())
                else:
                    return normalize_string(self._get_fallback_content()[2].get_text())
        return normalize_string(instructions)

    def glass(self):
        try:
            tools = self.soup.findAll('ul', {'class': ['ingredients__tools']})[0].findAll('li', {'class': ['ingredients__item']})
            for tool in tools:
                if 'glass' in tool.text.strip().lower():
                    return normalize_string(tool.text.split(':')[1])
        except IndexError:
            return self._fallback_glass()

    def garnish(self):
        try:
            tools = self.soup.findAll('ul', {'class': ['ingredients__tools']})[0].findAll('li', {'class': ['ingredients__item']})
            for tool in tools:
                if 'garnish' in tool.text.strip().lower():
                    return normalize_string(tool.text.split(':')[1])
        except IndexError:
            return self._fallback_garnish()

    def _get_fallback_content(self):
        return self.soup.find('div', {'class': ['recipe__main-content']}).findAll('p')
