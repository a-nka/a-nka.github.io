import mistune
from mistune.util import escape_html

class CSS():

    LINK = 'link'
    IMAGE = 'image'

    ITALIC = 'italic'
    BOLD = 'bold'

    PARAGRAPH = 'paragraph'
    SUMMARY = 'summary'

class Renderer(mistune.HTMLRenderer):

    def __init__(self):
        super().__init__()
        self.pageTitle = None
        self.foundSummary = False

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
        if level == 1 and self.pageTitle is None:
            self.pageTitle = text
        return super().heading(text, level)