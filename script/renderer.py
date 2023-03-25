import mistune
from mistune.util import escape_html, escape
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

from css import CSS
from categorizer import Categorizer

class Renderer(mistune.HTMLRenderer):

    CATEGORIES_PREFIX = 'categories:'
    LINK_NEW_TAB = 'new:'

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

        openInNewTab = False

        if title is not None:
            if title.startswith(self.LINK_NEW_TAB):
                title = escape_html(title[len(self.LINK_NEW_TAB):])
                openInNewTab = True
            else:
                title = escape_html(title)

        newTabLink = 'target="_blank" rel="noopener noreferrer"' if openInNewTab else ''

        s = '<a href="' + self._safe_url(link) + '"'
        if title:
            s += ' title="' + title + '"'
        return s + f' class = "{CSS.LINK}"' + newTabLink + '>' + (text or link) + '</a>'
    
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
    
    def codespan(self, text: str) -> str:
        return '<code class=' + CSS.INLINE_CODE + '>' + escape(text) + '</code>'
    
    def block_code(self, code: str, info: str = None) -> str:
        content = '<pre class=' + CSS.BLOCK_CODE + '><code'
        if info is not None:
            info = info.strip()
        if info:
            lang = info.split(None, 1)[0]
            lang = escape_html(lang)
            lexer = get_lexer_by_name(lang, stripall = True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return content + '>' + escape(code) + '</code></pre>\n'
    
    # block level

    def paragraph(self, text: str) -> str:
        summary = ''
        if not self.foundSummary:
            summary = ' ' + CSS.SUMMARY
        return f'<p class = "{CSS.PARAGRAPH}' + summary + '">' + text + '</p>\n'
    
    def heading(self, text: str, level: int) -> str:
        
        hr = ''
        if level == 1:

            # Set the page title
            if self.pageTitle is None:
                self.pageTitle = text

            # Register the page to its appropriate categories
            elif text.startswith(self.CATEGORIES_PREFIX):
                targetCategories = text[len(self.CATEGORIES_PREFIX):].split(',')
                if not ('' in targetCategories and len(targetCategories) == 1):
                    categoryNote = self.categorizer.addPage(self.pageTitle, self.currentPage, targetCategories)
                    return '<p class = "' + CSS.CATEGORY_NOTE + '">Catégorie' + ('s' if len(categoryNote) > 1 else '') + ' : ' + ', '.join(categoryNote) + '</p>\n'
                else:
                    return ''

        # Skip the summary if not found before the first heading
        elif not self.foundSummary and level == 2:
            self.foundSummary = True
            hr = self.thematic_break() + '\n'

        # Render the heading as usual
        return hr + super().heading(text, level)

    def reset(self) -> None:
        self.currentPage = None
        self.pageTitle = None
        self.foundSummary = False