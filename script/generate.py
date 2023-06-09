import os
import json

from deployer import Deployer, DeploymentPath

# Logger setup
# ----------------------------------------------------
import logging, sys, traceback, types, typing

logging.basicConfig(
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

if __name__ == '__main__':

    sitename = 'D-02'

    root = DeploymentPath('.', '/')
    pages = DeploymentPath('raw', 'pages')
    data = os.path.join(root.src, 'data')

    with open(os.path.join(data, 'categories.json'), 'r', encoding = 'utf-8') as f:
        categories = json.load(f)

    deployer = Deployer(
        sitename,
        os.path.join(data, 'basePage.html'),
        os.path.join(data, 'baseIndex.html'),
        os.path.join(data, 'baseCategories.html'),
        os.path.join(data, 'menu.html'),
    )

    deployer.deploy(root, pages, categories)
