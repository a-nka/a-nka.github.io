import logging
LOGGER = logging.getLogger(__name__)

class HTMLGenerator():

    TITLE_LEVEL_1 = "<h1>{}</h1>"
    TITLE_LEVEL_2 = "<h2>{}</h2>"
    TITLE_LEVEL_3 = "<h3>{}</h3>"
    TITLE_LEVEL_4 = "<h4>{}</h4>"

    DESCRIPTION = "<em>{}</em>"
    TEXT = "<p>{}</p>"


    def __init__(self, baseHTML: str, sitename: str = 'Destin RP') -> None:
        """Builds an HTMLConstructor object for generating HTML pages"""
        self.baseHTML = baseHTML
        self.sitename = sitename

    def generate(self, ast: dict) -> str:
        body = ""

        for node in ast:
            if node['type'] == 'heading':
                body += self.getTitleLevel(int(node['level'])).format(node['children'][0]['text'])
            elif node['type'] == 'paragraph':
                body += self.TEXT.format(node['children'][0]['text'])
            else:
                LOGGER.warning('Unsupported node type: %s', node['type'])
                LOGGER.debug('Node: %s', node)

        return self.baseHTML.format(ast[0]['children'][0]['text'] + ' - ' + self.sitename, body)

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