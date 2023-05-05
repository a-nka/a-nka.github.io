import os

import mistune
from mistune.plugins import plugin_strikethrough, plugin_table

from categorizer import Categorizer
from renderer import Renderer

class DeploymentPath():

    def __init__(self, src: str, to: str) -> None:
        self.src = src
        self.to = to

class Deployer():

    def __init__(self,
                sitename: str,
                pageTemplatePath: str,
                indexTemplatePath: str,
                categoriesTemplatePath: str,
                menuFragmentPath: str
            ) -> None:
        self.sitename = sitename
        self.menuFragment = self._load(menuFragmentPath).format(sitename)
        self.pageTemplate = self._load(pageTemplatePath).replace('{menu}', self.menuFragment)
        self.indexPageTemplate = self._load(indexTemplatePath).replace('{menu}', self.menuFragment)
        self.categoriesPageTemplate = self._load(categoriesTemplatePath).replace('{menu}', self.menuFragment)

    def _load(self, path: str) -> str:
        with open(path, 'r', encoding = 'utf-8') as input:
            return input.read()
        
    def _write(self, path: str, content: str) -> None:
        with open(path, 'w', encoding = 'utf-8') as output:
            output.write(content)
        
    def deploy(self, root: DeploymentPath, folder: DeploymentPath, categories: dict) -> None:

        categorizer = Categorizer(
            categories,
            self.categoriesPageTemplate,
            os.path.join(root.to, 'categories.html')
        )
        renderer = Renderer(categorizer)
        markdown = mistune.create_markdown(
            renderer = renderer, 
            plugins = [plugin_strikethrough, plugin_table]
        )

        # Delete files in destination folder
        for file in os.listdir(os.path.join(root.src, folder.to)):
            os.remove(os.path.join(root.src, folder.to, file))

        undeployedPages = os.listdir(os.path.join(root.src, folder.src))
        for page in undeployedPages:
            toPage = page.replace('.md', '.html')

            renderer.currentPage = os.path.join(root.to, folder.to, toPage)

            pageContent = self._load(os.path.join(root.src, folder.src, page))
            html = markdown(pageContent)

            self._write(
                os.path.join(root.src, folder.to, toPage),
                self.pageTemplate.format(renderer.pageTitle, self.sitename, html)
            )

            renderer.reset()

        self._write(
            os.path.join(root.src, 'categories.html'),
            categorizer.render(self.sitename)
        )
        
        self._write(
            os.path.join(root.src, 'index.html'),
            self.indexPageTemplate.format(self.sitename)
        )