import os
import json

import mistune

from categorizer import Categorizer
from css import CSS
from renderer import Renderer

# Logger setup
# ----------------------------------------------------
import logging, sys, traceback, types, typing

logfile = 'gen.log'

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

def generate(root: str, source: str, target: str, data: str, sitename: str) -> None:
    """Generate pages from markdown files in a folder"""

    # Data needed for the generation
    with open(os.path.join(data, 'categories.json'), 'r', encoding = 'utf-8') as f:
        categories = json.load(f)

    categorizer = Categorizer(categories, '/catégories.html')
    renderer = Renderer(categorizer)
    markdown = mistune.create_markdown(renderer = renderer)

    with open(os.path.join(data, 'basePage.html'), 'r', encoding = 'utf-8') as f:
        basePage = f.read()

    rawMds = os.listdir(source)

    # Generate pages
    for md in rawMds:
        renderer.currentPage = os.path.join(target, md.replace('.md', '.html'))
        with open(os.path.join(source, md), 'r', encoding = 'utf-8') as input:
            html = markdown(input.read())
        with open(renderer.currentPage, 'w', encoding = 'utf-8') as output:
            output.write(basePage.format(renderer.pageTitle, sitename, html))
        renderer.reset()
            
    # TODO : Clean up

    # Generate categories
    with open(os.path.join(data, 'baseCategories.html'), 'r', encoding = 'utf-8') as f:
        baseCategories = f.read()

    astCategories = categorizer.categorizedPages
    content = ''
    for category, pages in astCategories.items():
        content += '<h2 id="' + category + '">' + categories[category] + '</h1>\n<ul>\n'
        for page in pages:
            content += '<li><a href = "' + os.path.relpath(page['path']) + f'" class = "{CSS.LINK}">' + page['title'] + '</a></li>\n'
        content += '</ul>\n'

    with open(os.path.join(root, 'catégories.html'), 'w', encoding = 'utf-8') as f:
        f.write(baseCategories.format(sitename, content))

    # End clean up

    # Generate index and about pages
    generate_page(root, data, 'baseIndex.html', sitename)

def generate_page(root: str, data: str, baseFile: str, sitename: str) -> None:
    with open(os.path.join(data, baseFile), 'r', encoding = 'utf-8') as f:
        base = f.read()
    with open(os.path.join(root, baseFile[4:].lower()), 'w', encoding = 'utf-8') as f:
        f.write(base.format(sitename))

if __name__ == '__main__':
    root = '.'
    source = os.path.join(root, 'raw')
    wiki = os.path.join(root, 'wiki')
    data = os.path.join(root, 'data')

    sitename = 'Destin RP'

    generate(root, source, wiki, data, sitename)
