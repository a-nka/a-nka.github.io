
import logging
LOGGER = logging.getLogger(__name__)

from css import CSS

class Categorizer():

    def __init__(self, categoryNames: dict[str, str], targetCategoriesPath: str) -> None:
        self.categoryNames = categoryNames
        self.categorizedPages = {cat : [] for cat in categoryNames.keys()}
        self.targetCategoriesPath = targetCategoriesPath

    def addPage(self, title: str, path: str, categories: list[str]) -> list[str]:
        html = []
        for category in categories:
            category = category.strip()
            try:
                self.categorizedPages[category].append({
                    'title' : title,
                    'path' : path
                })
            except KeyError:
                LOGGER.warning(f'Category {category} not found')
                continue
            html.append(f'<a href = "{self.targetCategoriesPath}#{category}" class = "{CSS.LINK}">{self.categoryNames[category]}</a>')
        return html

    def render(self, sitename: str) -> str:
        
        pass