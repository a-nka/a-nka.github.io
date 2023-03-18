import mistune
from mistune.util import escape_html

from css import CSS
from categorizer import Categorizer

class Renderer(mistune.HTMLRenderer):

    CATEGORIES_PREFIX = 'categories:'

    def __init__(self, categorizer: Categorizer) -> None:
        super().__init__()
        self.currentPage = None
        self.pageTitle = None
        self.foundSummary = False

        self.categorizer = categorizer


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
    
    # block level

    def paragraph(self, text: str) -> str:
        summary = ''
        if not self.foundSummary:
            summary = ' ' + CSS.SUMMARY
        return f'<p class = "{CSS.PARAGRAPH}' + summary + '">' + text + '</p>\n'
    
    def heading(self, text: str, level: int) -> str:

        # Set the page title
        if self.pageTitle is None and level == 1:
            self.pageTitle = text

        if not self.foundSummary and level == 2:
            self.foundSummary = True

        # Register the page to its appropriate categories
        elif text.startswith(self.CATEGORIES_PREFIX) and level == 1:
            targetCategories = text[len(self.CATEGORIES_PREFIX):].split(',')
            if not ('' in targetCategories and len(targetCategories) == 1):
                categoryNote = self.categorizer.addPage(self.pageTitle, self.currentPage, targetCategories)
                return '<p class = "' + CSS.CATEGORY_NOTE + '">Catégorie' + ('s' if len(categoryNote) > 1 else '') + ' : ' + ', '.join(categoryNote) + '</p>\n'

        return super().heading(text, level)

    def reset(self) -> None:
        self.currentPage = None
        self.pageTitle = None
        self.foundSummary = False