
import logging
LOGGER = logging.getLogger(__name__)

from css import CSS

class Categorizer():

    def __init__(self, categories: dict[str, dict[str, str | dict]], pageLayout: str, deploymentPath: str) -> None:
        self.categories = categories
        self.sortedPages = {id : {'pages' : [], 'subs' : {sub : [] for sub in cat['subs'].keys()}} for id, cat in categories.items()}
        self.pageLayout = pageLayout
        self.deploymentPath = deploymentPath

    def _getNameAsSubCategory(self, category: str) -> tuple[str, str] | tuple[None, None]:
        for parentId, cat in self.categories.items():
            for sub, name in cat['subs'].items():
                if sub == category:
                    return parentId, name
        return None, None

    def addPage(self, pageTitle: str, pageDeploymentPath: str, pageCategories: list[str]) -> list[str]:
        htmlLinks = []

        for category in pageCategories:
            category = category.strip().lower()

            href = self.deploymentPath + '#' + category

            name = None
            parentId = None
            try:
                name = self.categories[category]['name']
            except KeyError:
                parentId, name = self._getNameAsSubCategory(category)
            if name is None:
                LOGGER.warning(f'Category {category} not found')
                continue

            record = {'title' : pageTitle, 'path' : pageDeploymentPath}
            if parentId is None:
                self.sortedPages[category]['pages'].append(record)
            else:
                self.sortedPages[parentId]['subs'][category].append(record)
            htmlLinks.append(f'<a href = "{href}" class = "{CSS.LINK}">{name}</a>')

        return htmlLinks
    
    def render(self, sitename: str) -> str:
        content = ''
        for category, pages in self.sortedPages.items():
            # Build the category
            title = '<h2 id="' + category + '">' + self.categories[category]['name'] + '</h2>\n'
            pages['pages'].sort(key = lambda page : page['title'])
            listLinks = [f'<li><a href = "{page["path"]}" class = "{CSS.LINK}">{page["title"]}</a></li>' for page in pages['pages']]
            withoutSubCategoryList = '<ul>\n' + '\n'.join(listLinks) + '</ul>\n'
            # Build the subcategories of the category
            withSubCategoryList = ''
            for sub, subPages in pages['subs'].items():
                subPages.sort(key = lambda page : page['title'])
                listLinks = [f'<li><a href = "{page["path"]}" class = "{CSS.LINK}">{page["title"]}</a></li>' for page in subPages]
                subTitle = '<h3 id="' + sub + '">' + self.categories[category]['subs'][sub] + '</h3>\n'
                subCategoryList = f'<ul>\n' + '\n'.join(listLinks) + '</ul>\n'
                withSubCategoryList += f'<div class="{CSS.SUBCATEGORY}">' + subTitle + subCategoryList + '</div>\n'
            # Add the category to the content
            content += title + withoutSubCategoryList + withSubCategoryList
        # Render the category page with the categories
        return self.pageLayout.format(sitename, content)