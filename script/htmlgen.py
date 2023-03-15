import json

import logging
LOGGER = logging.getLogger(__name__)

class HTMLGenerator():

    TITLE_LEVEL_1 = "<h1>{}</h1>"
    TITLE_LEVEL_2 = "<h2>{}</h2>"
    TITLE_LEVEL_3 = "<h3>{}</h3>"
    TITLE_LEVEL_4 = "<h4>{}</h4>"

    DESCRIPTION_BLOCK = "<em>{}</em>"

    TEXT = "<p>{}</p>"
    LINK = "<a href=\"{}\">{}</a>"

    BOLD = "<strong>{}</strong>"
    ITALIC = "<em>{}</em>"

    ORDERED_LIST = "<ol>{}</ol>"
    UNORDERED_LIST = "<ul>{}</ul>"
    LIST_ITEM = "<li>{}</li>"

    # Generated by GitHub Copilot
    STRIKE = "<s>{}</s>"
    UNDERLINE = "<u>{}</u>"
    CODE = "<code>{}</code>"
    QUOTE = "<blockquote>{}</blockquote>"
    IMAGE = "<img src=\"{}\" alt=\"{}\" />"

    def __init__(self, baseHTML: str, sitename: str = 'Destin RP') -> None:
        """Builds an HTMLConstructor object for generating HTML pages"""
        self.baseHTML = baseHTML
        self.sitename = sitename

    def generate(self, ast: dict) -> str:
        """Generate the HTML page from the AST"""
        if ast[0]['type'] != 'heading':
            raise ValueError('The first node of the AST must be a heading')
        if ast[1]['type'] != 'paragraph':
            raise ValueError('The second node of the AST must be a paragraph')

        body  = self.getTitleLevel(int(ast[0]['level'])).format(ast[0]['children'][0]['text'])
        body += self.DESCRIPTION_BLOCK.format(self.generateContent(ast[1]['children']))

        for node in ast[2:]:
            if node['type'] == 'heading':
                body += self.getTitleLevel(int(node['level'])).format(node['children'][0]['text'])
            elif node['type'] == 'paragraph':
                body += self.TEXT.format(self.generateContent(node['children']))
            elif node['type'] == 'list':
                body += self.generateList(node)
            else:
                self.logUnknowNodeType(node)

        return self.baseHTML.format(ast[0]['children'][0]['text'] + ' - ' + self.sitename, body)
    
    def generateContent(self, children: list) -> str:
        content = ""

        for node in children:
            if node['type'] == 'text':
                content += node['text']
            elif node['type'] == 'link':
                content += self.LINK.format(node['link'], self.generateContent(node['children']))
            elif node['type'] == 'strong':
                content += self.BOLD.format(node['children'][0]['text'])
            elif node['type'] == 'emphasis':
                content += self.ITALIC.format(node['children'][0]['text'])
            else:
                self.logUnknowNodeType(node)        
        
        return content
    
    def generateList(self, listAst: dict) -> str:
        content = ""

        children = listAst['children']

        for node in children:
            if node['type'] == 'list_item':
                for child in node['children']:
                    if child['type'] == 'list':
                        content += self.generateList(child)
                    else:
                        content += self.LIST_ITEM.format(self.generateContent(child['children']))
            else:
                self.logUnknowNodeType(node)

        return self.getList(listAst.get('ordered', True)).format(content)
    
    def logUnknowNodeType(self, node: dict) -> None:
        LOGGER.warning('Unsupported node type : %s', node['type'])
        LOGGER.debug('Dumping node\n%s', json.dumps(node, indent = 2))

    @staticmethod
    def getTitleLevel(level: int) -> str:
        """Get the HTML tag for a title of a given level

        :param level: Integer. The level of the title

        :return: String. The HTML tag for the title
        """
        levels = [
            HTMLGenerator.TITLE_LEVEL_1,
            HTMLGenerator.TITLE_LEVEL_2,
            HTMLGenerator.TITLE_LEVEL_3,
            HTMLGenerator.TITLE_LEVEL_4
        ]
        return levels[level - 1]

    @staticmethod
    def getList(isOrdered: bool) -> str:
        """Get the HTML tag for a list

        :param isOrdered: Boolean. True if the list is ordered, False otherwise

        :return: String. The HTML tag for the list
        """
        if isOrdered:
            return HTMLGenerator.ORDERED_LIST
        return HTMLGenerator.UNORDERED_LIST