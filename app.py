import flask
import os
from pathlib import Path
import sys

import md2html

app = flask.Flask(__name__)


class Tree(object):
    def __init__(self, api_path='docs'):
        self.tree_str = ""
        self.api = api_path
        self.root_path_str = os.path.join(os.path.dirname(os.path.abspath(__file__)))

    def __call__(self, top):
        self.tree_str = ""
        self.top = Path(top)
        return self.__tree(top)

    def __tree(self, top, tabs=0):
        top = Path(top)
        flag = 1
        if self.top.name == top.name:
            flag = 0
        if top.is_dir():
            self.tree_str += '|&nbsp;&nbsp;&nbsp;&nbsp;' * (tabs - 1) + "|---"*flag + '<b>%s</b><br>' % top.name
            for x in top.iterdir():
                self.__tree(x, tabs + 1)
        else:
            if top.name.split('.')[-1] in ['md', 'markdown']:
                file = str(top.absolute()).replace(self.root_path_str, '.')
                # title = top.absolute().parent.name + top.name
                title = top.name
                self.tree_str += '|&nbsp;&nbsp;&nbsp;&nbsp;' * (tabs - 1) + "|---<a href=/%s?f=%s&t=%s target=_blank>" % (self.api, file, title) + title + '</a></b><br>'
        return self.tree_str


@app.route('/')
def index():
    tree = Tree()
    return """
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
        <html>
        <head>
        <title>文档</title>
        </head>
        <body>
            %s
        </body>
        </html>
    """ % tree(path)


@app.route('/docs')
def html():
    args = flask.request.args
    file_name = args.get('f')
    title = args.get('t')
    if not os.path.exists(file_name):
        return "文件不存在！"
    else:
        html = md2html.MD2Html(file_name, title=title)
        return html.html


if __name__ == '__main__':
    help_str = """
使用方法：
python app.py path
path: 需要查看的路径。
"""
    try:
        path = sys.argv[1]
        if path == '--help':
            print(help_str)
        elif not os.path.exists(path):
            print('指定路径不存在')
        else:
            app.run()
    except IndexError:
        print(help_str, '\n')




