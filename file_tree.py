from pathlib import Path
import os
from urllib.parse import quote

EXTEND_NAMES = (
    'md', 'markdown', 'py', 'java', 'cpp',
)


class Tree(object):
    """目录树"""

    def __init__(self, api_path='docs', root_dir=os.path.dirname(os.path.abspath(__file__)),
                 extends=None):
        """
        :param api_path: str html路径
        :param root_dir: str 需要解析的本地根目录
        :param extends: list 需要解析的文件扩展名。可以使用通配符 ['*'] 匹配所有文件。
        """
        self.tree_str = ""
        self.tree_obj = []
        self.api = api_path
        self.root_dir = root_dir
        extends = extends if extends else ['md', 'markdown'] or EXTEND_NAMES
        self.extends = [x.lower() for x in extends]
        self.root_dir = self.__strip_xx(self.root_dir) + os.sep
        self.root_dir_name = self.__strip_xx(self.root_dir).split(os.sep)[-1]
        self.md_paths = self.__dirs()

    def __call__(self):
        top = self.root_dir
        self.tree_str = '<b><strong>%s</strong></b><br>' % self.root_dir_name
        self.top = Path(top)
        return self.__tree(top)

    @staticmethod
    def __strip_xx(path: str):
        """去除路径前后的斜线"""
        while path.endswith(os.sep):
            path = path[:-1]
        return path

    def __dirs(self):
        md_files = []
        for root, dirs, files in os.walk(self.root_dir):
            for file in files:
                extend_name = file.split('.')[-1]
                if extend_name.lower() in self.extends or "*" in self.extends:
                    md_file = os.path.join(root.replace(self.root_dir, ''), file)
                    md_files.append(md_file)
        dirs = set()
        for x in md_files:
            cell = x.split(os.sep)
            for i in range(len(cell)):
                # print(cell[:i + 1])
                dirs.add(os.sep.join(cell[:i + 1]))
        return dirs

    def __tree(self, top, tabs: int = 0):
        top = Path(top)
        flag = 1

        path = self.__strip_xx(str(top.absolute()).replace(self.root_dir, ''))
        if self.top.name == top.name:
            flag = 0

        if top.is_dir():
            if path in self.md_paths:
                self.tree_str += '|&nbsp;&nbsp;&nbsp;&nbsp' * (
                        tabs - 1) + "|--" * flag + '<b>%s</b><br>' % top.name

            _, dirs, files = next(os.walk(top.absolute()))
            files_and_dirs = files + dirs

            for x in files_and_dirs:
                if not str(x).split(os.path.sep)[-1].startswith('.'):
                    self.__tree(os.path.join(top.absolute(), x), tabs + 1)
        else:
            if top.name.split('.')[-1].lower() in self.extends or "*" in self.extends:
                # title = top.absolute().parent.name + top.name
                title = top.name
                if path in self.md_paths:
                    href = '/%s?f=%s&t=%s' % (quote(self.api), quote(path), quote(title))
                    self.tree_str += '|&nbsp;&nbsp;&nbsp;&nbsp' * (tabs - 1)
                    self.tree_str += "|--<a href=%s target=_blank>%s</a></b><br>" % (
                        href, title)

        root_dir = str(self.top.absolute()).split(os.path.sep)[-1]

        return """ <!DOCTYPE html">
            <html>
                <head>
                    <title>%s - [%s]</title>
                </head>
                <body>
                    %s
                </body>
            </html> """ % (root_dir, ','.join(self.extends), self.tree_str)
