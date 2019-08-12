# -*- coding: utf-8 -*-

import markdown as md


class Head(object):
	style = """
	<style type="text/css">
		pan.MathJax_SVG {
			zoom: 1.2;
		}

		@font-face {
			font-family: 'wdsong';
			// src: url('./font/wd-song.ttf');
			font-weight: lighter;
		}

		@font-face {
			font-family: 'ubuntu-mono';
			// src: url('./font/ubuntu-mono.ttf');
			font-weight: lighter;
		}

		@media screen {
			html {
				background-repeat: repeat-x repeat-y;
				background-color: #000000;
				padding: 16px;
			}

			body {
				background-repeat: repeat-x repeat-y;
				width: auto;
				max-width: 800px;
				min-width: 640px;
				margin: auto;
				margin-top: 0px;
				margin-bottom: 64px;
				padding: 50px;
				// background-color: #CCE8CF;
				background-image:url(data:image/jpeg;base64,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);   
				// background-size:cover; 
				border-radius: 1px;
				box-shadow: 0px 0px 16px #808080;
				word-wrap: break-word;
				line-height: 150%;
				font-family: 'wdsong';
				color: #101010;
			}

			h1 {
				margin-top: 64px;
				margin-bottom: 48px;
				padding-bottom: 16px;
				text-align: center;
				font-weight: 900;
				font-size: xx-large;
			}

			h2 {
				background-repeat: repeat-x repeat-y;
				margin-top: 32px;
				margin-left: -50px;
				margin-right: -50px;
				padding-left: 50px;
				padding-top: 32px;
				padding-bottom: 16px;
				// border-top: dotted thin #CCCCCC;
				font-weight: bold;
				font-size: x-large;
			}

			h3 {
				margin-top: 24px;
				margin-bottom: 24px;
				padding-bottom: 6px;
				// color: #004499;
				// border-bottom: dotted thin #000000;
				line-height: 100%;
				font-weight: bold;
				font-size: large;
			}

			h4 {
				background-repeat: no-repeat;
				height: 24px;
				margin-bottom: 24px;
				padding-top: 6px;
				/* padding-left      : 48px; */
				line-height: 100%;
				font-weight: bold;
			}

			p {
				text-indent: 32px;
			}

			ol p, ul p {
				text-indent: 1px;
			}

			ol, ul {
				padding-left: 64px;
				padding-right: 48px;
			}

			b {
				margin: 4px;
				color: #004499;
			}

			a {
				color: #0070D0;
			}

			code {
				font-family: 'ubuntu-mono';
			}

			p code, ol code, ul code {
				padding-top: -1px;
				padding-bottom: 2px;
				padding-left: 4px;
				padding-right: 4px;
				background-color: #FAFAFA;
				box-shadow: 0px 0px 4px #D0D0D0 inset;
				border-radius: 4px;
			}

			pre code {
				padding: 0px;
				box-shadow: 0px 0px 0px #D0D0D0;
				border-radius: 4px;
			}

			pre {
				background-repeat: no-repeat;
				margin: 10px;
				margin-left: 30px;
				margin-right: 30px;
				padding: 10px;
				background-color: #FAFAFA;
				box-shadow: 0px 0px 4px #D0D0D0 inset;
				border-radius: 4px;
				line-height: 130%;
			}

			blockquote {
				background-repeat: no-repeat;
				margin: 10px;
				padding: 10px;
				margin-left: 20px;
				margin-right: 20px;
				background-color: #FCFCFC;
				color: #606060;
				box-shadow: 0px 0px 16px #888888;
				border-radius: 2px;
				line-height: 130%;
				font-size: small;
			}

			table {
				margin-bottom: 10px;
				margin-left: 32px;
				margin-right: 32px;
				box-shadow: 0px 0px 4px #888888;
				border-collapse: collapse;
				border: 1px solid #888888;
				text-align: center;
				font-size: x-small;
				width: 90%;
			}

			th {
				padding: 2px;
				padding-left: 4px;
				padding-right: 4px;
				background-color: #E0E0E0;
				font-family: 黑体;
				font-style: normal;
				font-weight: bold;
				font-size: x-small;
				border: 1px solid #888888;
			}

			td {
				padding: 2px;
				padding-left: 4px;
				padding-right: 4px;
				background-color: #FCFCFC;
				font-family: 'wdsong';
				/* border           : 1px dotted #888888; */
				border: 1px solid #888888;
			}

			center {
				font-size: x-small;
				font-weight: bold;
			}
		}

		@media print {
			html {
				background-repeat: repeat-x repeat-y;
				background-color: #ECECEC;
				padding: 16px;
			}

			body {
				background-repeat: repeat-x;
				width: auto;
				max-width: 800px;
				min-width: 640px;
				margin: auto;
				margin-top: 0px;
				margin-bottom: 64px;
				padding: 50px;
				background-color: #FFFFFE;
				/*  border-radius    : 1px;
				box-shadow       : 0px 0px 16px #808080; */
				word-wrap: break-word;
				line-height: 150%;
				font-family: 'wdsong';
				color: #101010;
			}

			h1 {
				margin-top: 64px;
				margin-bottom: 48px;
				padding-bottom: 16px;
				text-align: center;
				font-weight: 900;
				font-size: xx-large;
			}

			h2 {
				background-repeat: repeat-x repeat-y;
				margin-top: 32px;
				margin-left: -50px;
				margin-right: -50px;
				padding-left: 50px;
				padding-top: 32px;
				padding-bottom: 16px;
				// border-top: dotted thin #CCCCCC;
				font-weight: bold;
				font-size: x-large;
			}

			h3 {
				margin-top: 24px;
				margin-bottom: 24px;
				padding-bottom: 6px;
				// color: #004499;
				// border-bottom: dotted thin #000000;
				line-height: 100%;
				font-weight: bold;
				font-size: large;
			}

			h4 {
				background-repeat: no-repeat;
				height: 24px;
				margin-bottom: 24px;
				padding-top: 6px;
				/* padding-left      : 48px; */
				line-height: 100%;
				font-weight: bold;
			}

			p {
				text-indent: 32px;
			}

			ol p, ul p {
				text-indent: 1px;
			}

			ol, ul {
				padding-left: 64px;
				padding-right: 48px;
			}

			b {
				margin: 4px;
				color: #004499;
			}

			a {
				color: #0070D0;
			}

			code {
				font-family: 'ubuntu-mono';
			}

			p code, ol code, ul code {
				padding-top: -1px;
				padding-bottom: 2px;
				padding-left: 4px;
				padding-right: 4px;
				background-color: #FAFAFA;
				box-shadow: 0px 0px 4px #D0D0D0 inset;
				border-radius: 4px;
			}

			pre code {
				padding: 0px;
				box-shadow: 0px 0px 0px #D0D0D0;
				border-radius: 4px;
			}

			pre {
				background-repeat: no-repeat;
				margin: 10px;
				margin-left: 30px;
				margin-right: 30px;
				padding: 10px;
				background-color: #FAFAFA;
				box-shadow: 0px 0px 4px #D0D0D0 inset;
				border-radius: 4px;
				line-height: 130%;
			}

			blockquote {
				background-repeat: no-repeat;
				margin: 10px;
				padding: 10px;
				margin-left: 20px;
				margin-right: 20px;
				background-color: #FCFCFC;
				color: #606060;
				box-shadow: 0px 0px 16px #888888;
				border-radius: 2px;
				line-height: 130%;
				font-size: small;
			}

			table {
				margin-bottom: 10px;
				margin-left: 32px;
				margin-right: 32px;
				box-shadow: 0px 0px 4px #888888;
				border-collapse: collapse;
				border: 1px solid #888888;
				text-align: center;
				font-size: x-small;
				width: 90%;
			}

			th {
				padding: 2px;
				padding-left: 4px;
				padding-right: 4px;
				background-color: #E0E0E0;
				font-family: 黑体;
				font-style: normal;
				font-weight: bold;
				font-size: x-small;
				border: 1px solid #888888;
			}

			td {
				padding: 2px;
				padding-left: 4px;
				padding-right: 4px;
				background-color: #FCFCFC;
				font-family: 'wdsong';
				/* border           : 1px dotted #888888; */
				border: 1px solid #888888;
			}

			center {
				font-size: x-small;
				font-weight: bold;
			}
		}
	</style>
	"""

	js = """
	<script src="https://cdn.bootcss.com/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_HTMLorMML"></script>
	<script type="text/x-mathjax-config">
		MathJax.Hub.Config({
			showProcessingMessages: false,
			//关闭js加载过程信息
			messageStyle: "none",
			//不显示信息
			extensions: ["tex2jax.js"],
			jax: ["input/TeX", "output/HTML-CSS"],
			tex2jax: {
				inlineMath: [['$', '$']],
				//行内公式选择符
				displayMath: [['$$', '$$']],
				//段内公式选择符
				skipTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'a'],
				//避开某些标签
				ignoreClass: "comment-content" //避开含该Class的标签
			},
			"HTML-CSS": {
				availableFonts: ["STIX", "TeX"],
				//可选字体
				//showMathMenu: false //关闭右击菜单显示
			}
		});
		MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
	</script>
	"""


class MD2Html(Head):
	def __init__(self, md=None, title="md2html", from_str=False, encoding='utf-8'):
		"""

		:param md: str markdown 文件路径或者 markdown 内容。默认为文件路径，当from_str = True 时 md 代表内容
		:param title: str 输出 html 的标题
		:param from_str: str 输入字符是否为 markdown 内容
		:param encoding: str md文件的编码方式
		"""
		self.title = title
		self.head = '''
			<head>
			<title>%s</title>
			<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
			%s
			</head>
		''' % (self.title, self.style + self.js)
		if from_str:
			self.md_str = md
		else:
			self.md_str = self.from_file(md, encoding)

	def from_file(self, file_path, encoding):
		"""
		with open(file_path, 'r', encoding=encoding, *args, **kwargs) as fp:
			return fp.read()
		"""
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
		return """
			<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

			<html>
			%s
			<body>
			%s
			</body>
			</html>
		""" % (self.head, md.markdown(self.md_str))

	def save_html(self, file_path, encoding='utf-8'):
		"""
		保存 html 文件
		:param file_path: str html 文件
		:return: None
		"""
		with open(file_path, 'w', encoding=encoding) as fp:
			fp.write(self.html)

