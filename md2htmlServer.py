# pip install flask
import flask
import sys
import os
from urllib.parse import unquote

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
print(BASE_DIR)

from md2html import MD2Html
from file_tree import Tree

app = flask.Flask(__name__)


@app.route('/')
def index():
    tree = Tree(root_dir=path, extends=extends)
    return tree()


@app.route('/docs')
def html():
    args = flask.request.args
    file_name = unquote(os.path.join(path, args.get('f')))
    title = args.get('t')
    if not os.path.exists(file_name):
        return "文件不存在！"
    else:
        html = MD2Html(file_name, title=title)
        return html.html


if __name__ == '__main__':
    help_str = """
使用方法：
python app.py path extends
\tpath: 需要查看的路径。
\textends: 需要解析的文件后缀名,以|分隔
"""
    args = sys.argv

    if len(args) < 2:
        print(help_str, '\n')
    else:
        path = args[1]
        if path == '--help':
            print(help_str)
        elif not os.path.exists(path):
            print('指定路径不存在')
        else:
            path = os.path.abspath(path)

            if len(args) >= 3:
                extends = [x.strip() for x in ''.join(args[2:]).split(',')]
            else:
                extends = None

            app.run()
