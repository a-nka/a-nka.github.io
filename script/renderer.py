import mistune
from mistune.util import escape_html

class CSS():

    LINK = 'link'
    IMAGE = 'image'

    ITALIC = 'italic'
    BOLD = 'bold'

    PARAGRAPH = 'paragraph'
    SUMMARY = 'summary'
    CATEGORY_NOTE = 'category-note'

class Renderer(mistune.HTMLRenderer):

    CATEGORIES_PREFIX = 'categories:'

    def __init__(self, categoryNames: dict[str, str]):
        super().__init__()
        self.currentPage = None
        self.pageTitle = None
        self.foundSummary = False

        self.categoryNames = categoryNames
        self.categories = {cat : [] for cat in categoryNames.keys()}

    # inline level

    def link(self,
             link: str,
             text: str | None = None,
             title: str | None = None
             ) -> str:
        if text is None:
            text = link

        s = '<a href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + escape_html(title) + '"'
        return s + f' class = "{CSS.LINK}">' + (text or link) + '</a>'
    
    def image(self,
              src: str,
              alt: str = '',
              title: str | None = None
              ) -> str:
        src = self._safe_url(src)
        alt = escape_html(alt)
        s = '<img src="' + src + '" alt="' + alt + '"'
        if title:
            s += ' title="' + escape_html(title) + '"'
        return s + f' class = "{CSS.IMAGE}" />'
    
    def emphasis(self, text: str) -> str:
        return f'<em class = "{CSS.ITALIC}">' + text + '</em>'
    
    def strong(self, text: str) -> str:
        return f'<strong class = "{CSS.BOLD}">' + text + '</strong>'
    
    # block level

    def paragraph(self, text: str) -> str:
        summary = ''
        if not self.foundSummary:
            summary = ' ' + CSS.SUMMARY
            self.foundSummary = True
        return f'<p class = "{CSS.PARAGRAPH}' + summary + '">' + text + '</p>\n'
    
    def heading(self, text: str, level: int) -> str:

        # Register the page to its appropriate categories
        if text.startswith(self.CATEGORIES_PREFIX) and level == 1:
            pageCategories = text[len(self.CATEGORIES_PREFIX):].split(',')
            for category in pageCategories:
                self.categories[category.strip()].append(
                        {
                            'title' : self.pageTitle, 
                            'path' : self.currentPage
                        }
                    )
            categoriesString = ', '.join([name for id, name in self.categoryNames.items() if id in pageCategories])
            return '<p class = "' + CSS.CATEGORY_NOTE + '">Catégorie' + ('s' if len(pageCategories) > 1 else '') + ' : ' + categoriesString + '</p>\n'

        # Set the page title
        if self.pageTitle is None and level == 1:
            self.pageTitle = text

        return super().heading(text, level)

    def reset(self) -> None:
        self.currentPage = None
        self.pageTitle = None
        self.foundSummary = False