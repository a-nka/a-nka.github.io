import os
import json

import mistune

from renderer import Renderer

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

def generate_pages(folder: str, target: str) -> None:
    """Generate pages from markdown files in a folder"""

    renderer = Renderer()
    markdown = mistune.create_markdown(renderer = renderer)
    with open('../base.html', 'r', encoding = 'utf-8') as f:
        base = f.read()

    files = os.listdir(folder)

    for file in files:
        with open(os.path.join(folder, file), 'r', encoding = 'utf-8') as input:
            with open(os.path.join(target, file.replace('.md', '.html')), 'w', encoding = 'utf-8') as output:
                html = markdown(input.read())
                output.write(base.format(renderer.pageTitle, html))

if __name__ == '__main__':
    generate_pages('../raw', '../wiki')
