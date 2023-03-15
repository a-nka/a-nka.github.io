import os
import json

import mistune

from renderer import Renderer, CSS

# Logger setup
# ----------------------------------------------------
import logging, sys, traceback, types, typing

logfile = '../gen.log'

logging.basicConfig(
    filename    = logfile,
    filemode    = 'w',
    encoding    = 'utf-8',

    level       = logging.DEBUG,
    format      = '%(asctime)s [ %(levelname)s ] %(name)s : %(message)s',
    datefmt     = '%d/%m/%Y %H:%M:%S'
)
LOGGER = logging.getLogger(__name__)

# Redifinition of sys.excepthook in order to catch any exception raised
# and log it before exiting, instead of printing it on stdout and exit
def excepthook(
    exception: typing.Type[BaseException],
    value: BaseException,
    tback: types.TracebackType
):
    tb = '\n'.join(traceback.format_exception(exception, value, tback))
    LOGGER.error('An unhandled exception occured\n%s', tb)
    LOGGER.info('Exiting')
    exit(1)

sys.excepthook = excepthook

# ----------------------------------------------------

def generate(folder: str, target: str) -> None:
    """Generate pages from markdown files in a folder"""

    # Data needed for the generation
    sitename = 'Destin RP'

    with open('../data/categories.json', 'r', encoding = 'utf-8') as f:
        categories = json.load(f)

    renderer = Renderer(categories)
    markdown = mistune.create_markdown(renderer = renderer)

    with open('../data/basePage.html', 'r', encoding = 'utf-8') as f:
        basePage = f.read()

    files = os.listdir(folder)

    # Generate pages
    for file in files:
        with open(os.path.join(folder, file), 'r', encoding = 'utf-8') as input:
            targetFile = os.path.join(target, file.replace('.md', '.html'))
            renderer.currentPage = 'wiki/' + file.replace('.md', '.html')
            html = markdown(input.read())
            with open(targetFile, 'w', encoding = 'utf-8') as output:
                output.write(basePage.format(renderer.pageTitle, sitename, html))
            renderer.reset()
            

    # Generate categories
    with open('../data/baseCategories.html', 'r', encoding = 'utf-8') as f:
        baseCategories = f.read()

    astCategories = renderer.categories
    content = ''
    for category, pages in astCategories.items():
        content += '<h1>' + categories[category] + '</h1>\n<ul>\n'
        for page in pages:
            content += '<li><a href = "' + page['path'] + f'" class = "{CSS.LINK}">' + page['title'] + '</a></li>\n'
        content += '</ul>\n'

    with open('../Categories.html', 'w', encoding = 'utf-8') as f:
        f.write(baseCategories.format(sitename, content))

if __name__ == '__main__':
    generate('../raw', '../wiki')
