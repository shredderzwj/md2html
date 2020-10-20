# md2html

## 功能简介
+ 把 markdown 文档转换成 html ,支持 Latex 数学公式（使用mathjax.js）、支持代码块高亮、支持使用[TOC]标签自动生成目录。
+ 把源代码转换成 可读性高的 html页面（支持高亮显示）。
+ 设置了简单的样式，类似于 word 文档 的 A4 页面，可直接使用 A4 版面打印。 
+ 使用 flask 框架实现了一个简单地文档浏览器（可列出指定文件夹下面的各种文件类型的文档树，见 file_tree.py 文件）。
+ tags：建议使用chromium内核的edge浏览器、Chrome浏览器、或者其他使用chromium内核的浏览器。

## 开发及测试环境
+ Windows 10 2004 64位 
+ python3.6.8 64位

## 安装依赖
pip install -r requirements.txt

## 文档浏览器使用方法

终端运行：
~~~
python md2htmlServer.py path [extends]
path: 需要查看的路径。
extends: 文件扩展名，多个扩展名中间以逗号分隔。可以使用 * 通配所有文件

例如：python md2htmlServer.py . *
例如：python md2htmlServer.py .. md,py,java
~~~

## 主要api

### class MD2Html(md=None, title="md2html", from_str=False, encoding='utf-8', code: str = None, code_map: dict = None)
#### 参数：
~~~
:param md: str markdown 文件路径或者 markdown 内容。默认为文件路径，当from_str = True 时 md 代表内容
:param title: str 输出 html 的标题
:param from_str: str 输入字符是否为 markdown 内容
:param encoding: str md文件的编码方式
:param code: str markdown 代码所用的语言，如：java python等
:param code_map: dict 代码文件的扩展名与代码语言的对照表，例如：
                CODE_MAP = {
                    'py': 'python', 'java': 'java', 'cpp': 'c++', 'c': 'c',
                    'htm': 'html', 'html': 'html', 'js': 'javascript',
                    'css': 'stylesheet', 'f90': 'fortran', 'f': 'fortran',
                }
~~~
#### object.html 返回html内容
#### object.save_html(self, file_path, encoding='utf-8'):
~~~
保存 html 文件
:param file_path: str html 文件
:return: None
~~~

### class Tree(api_path='docs', root_dir=os.path.dirname(os.path.abspath(__file__)), extends=None):
#### 参数：
~~~
:param api_path: str html路径
:param root_dir: str 需要解析的本地根目录
:param extends: list 需要解析的文件扩展名。可以使用通配符 ['*'] 匹配所有文件。
~~~
+ object() 返回html结果

## 关于html样式
默认使用 resource/style.black.css 样式，黑色背景，不刺眼。也可以自定义显示样式。可以直接修改style.black.css
文件，也可以增加新的样式文件，并修改 md2html.py 的 STYLE_FILE 路径，指向使用的样式文件。