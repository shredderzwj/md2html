import flask
from flask_script import Manager
import os

import md2html


app = flask.Flask(__name__)
conf = Manager(app)


@app.route('/')
def index():
    return """
        <p><a href=/docs?f=api.md&t=A-3 使用说明 target=_blank>A-3 使用说明</a></p><br />
        <p><a href=/docs?f=principle.md&t=A-3 计算原理 target=_blank>A-3 计算原理</p></a><br />
    """


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
    conf.run()
