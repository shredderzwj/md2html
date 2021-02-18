# -*- coding: utf-8 -*-
# pip install markdown python-markdown-math
# pip install pygments
import os
import re
import base64
import cgi

import markdown as md
from mdx_math import MathExtension

RESOURCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resource')
STYLE_FILE = os.path.join(RESOURCE_DIR, 'style.black.css')
CODE_MAP = {
    'py': 'python', 'java': 'java', 'cpp': 'c++', 'c': 'c',
    'htm': 'html', 'html': 'html', 'js': 'javascript',
    'css': 'stylesheet', 'f90': 'fortran', 'f': 'fortran',
}


class Head(object):
    css_file = STYLE_FILE
    with open(css_file, 'r', encoding='utf-8') as f:
        css = f.read()
    css_content = ' '.join([x.strip() for x in css.split('\n')])
    style = '<style type="text/css">%s</style>' % css_content

    js_file = os.path.join(RESOURCE_DIR, 'jqPrint.js')
    with open(js_file, 'r', encoding='utf-8') as f:
        js_content = f.read()
    # js_content = ' '.join([x.strip() for x in js_content.split('\n')])
    js = """
    <script src="https://libs.baidu.com/jquery/1.3.1/jquery.min.js"></script>
    <script>%s</script>
    """ % js_content


class MD2Html(Head):
    extensions = [
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.tables',
        'markdown.extensions.toc',
        'mdx_math',
        MathExtension(enable_dollar_delimiter=True),
    ]
    extension_configs = {
        'markdown.extensions.codehilite': {
            'linenums': True
        },
    }


    def __init__(
            self, md=None, title="md2html", from_str=False,
            encoding='utf-8', code: str = None, code_map: dict = None,
            mathjax=None,
    ):
        """
        :param md: str markdown 文件路径或者 markdown 内容。默认为文件路径，
                    当from_str = True 时 md 代表内容
        :param title: str 输出 html 的标题
        :param from_str: str 输入字符是否为 markdown 内容
        :param encoding: str md文件的编码方式
        :param code: str markdown 代码所用的语言，如：java python等
        :param code_map: dict 代码文件的扩展名与代码语言的对照表
        """
        if mathjax is None:
            mathjax = '<script src="https://cdn.bootcss.com/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>'
        self.js = self.js + mathjax
        if code_map is None:
            code_map = CODE_MAP
        self.title = title
        self.head = self.get_head(title)
        self.md_file_path = ''
        if from_str:
            self.md_str = md
        else:
            if not os.path.exists(md):
                raise FileExistsError('文件不存在！')
            self.md_file_path = os.path.abspath(md)
            try:
                self.md_str = self.from_file(md, encoding)
            except UnicodeDecodeError:
                try:
                    self.md_str = self.from_file(md, encoding='gbk')
                except UnicodeDecodeError:
                    self.md_str = 'Error 此文件不是文本文件！'

            if code is None:
                extend_name = md.split('.')[-1].strip().lower()
                code = code_map.get(extend_name, 'md')

        if code and code.strip().lower() not in ['md', 'markdown']:
            self.md_str = '```%s\n%s\n```' % (code, self.md_str)

        # 处理已知的code问题
        self.md_str = re.sub(r'(?<=\n)\s+?(?=```)', '', self.md_str)
        self.md_str = re.sub(r'(?<=\n)\s+?(?=~~~)', '', self.md_str)

    def get_head(self, title):
        return '''
            <head>
            <title>%s</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
            %s
            </head>
        ''' % (title, self.style + self.js)

    @staticmethod
    def from_file(file_path, encoding):
        with open(file_path, 'r', encoding=encoding) as fp:
            return fp.read()

    def set_head(self, html_head_str):
        """
        设置 html 文件的 <head> 内容
        :param html_head_str:  str html 文件的 <head> 内容
        :return:  None
        """
        self.head = html_head_str

    @property
    def html(self):
        """
        输出转换后的 html 字符串
        :return: str html 内容
        """


        # 转为html的字符串
        converted = md.markdown(self.md_str, extensions=self.extensions, extension_configs=self.extension_configs)

        # 添加本地图片资源，采用base64编码嵌入
        if self.md_file_path:
            md_file_path_dir = os.path.dirname(self.md_file_path)
            for x in re.findall(r'<\s*[iI][mM][gG].*?[sS][rR][cC]\s*=.*?>', converted):
                split = re.search(r'(<.*?src=")(.*?)(".*?>)', x).groups()
                if split:
                    pre, img_src, aft = split
                    img_src = cgi.html.unescape(img_src)

                    img_path = os.path.sep.join([x for x in re.split(r'[\/]', img_src)])
                    if not os.path.exists(img_path):
                        img_path = os.path.join(md_file_path_dir, os.path.sep.join(
                            [x for x in re.split(r'[\/]', img_src) if x]))
                    if os.path.exists(img_path):
                        # 图片格式
                        img_format = img_path.split('.')[-1].lower()
                        if not img_format or len(img_format) > 5:
                            img_format = 'jpg'
                        if img_format == 'svg':
                            img_format = 'svg+xml'
                        with open(img_path, 'rb') as f:
                            img_blob = f.read()
                            base64_src = 'data:image/{};base64,{}'
                            base64_src = base64_src.format(img_format,
                                                           base64.b64encode(img_blob).decode())

                            converted = re.sub('(?<=%s).*(?=%s)' % (pre, aft), base64_src,
                                               converted)

        return """
            <!DOCTYPE html>
            <html>
            %s
            <body>
                <div class='container'>
                %s
                </div>
                <div class='no-print' style-"text-align: center">
                    <hr style="margin-top:16px">
                    <input type="button" onclick="printPage();" value="打印本页"/>
                </div>
                <script>
                    printPage = function(){
                        $('html').jqprint();
                    };
                </script>
            </body>
            </html>
        """ % (self.head, converted)

    def save_html(self, file_path, encoding='utf-8'):
        """
        保存 html 文件
        :param file_path: str html 文件
        :return: None
        """
        with open(file_path, 'w', encoding=encoding) as fp:
            fp.write(self.html)
