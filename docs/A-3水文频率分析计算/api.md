# A-3  水文频率计算（使用方法） 

<center> 作者 周伟杰 </center>

## 模块 cnhydropy.hydrology.frequency 概述：
+ 水文频率（P-III曲线）相关计算模块
+ 主要参考《水利水电工程水文计算规范》（DL5431-2009）、《水利水电工程设计洪水计算规范》（SL44-2006）

## 功能概述
&ensp;本程序可一次完成一个水文系列频率计算的全部工作，对连续系列和不连续系列均为适用，根据输入的数据自动判断连续系列和不连续系列。本程序完成的工作内容包括：系列排队、计算经验频率及统计参数值、通过优选P-Ⅲ型曲线的参数$C_v, C_s$值进行适线或用目估法适线、绘制频率曲线图、计算所采用的频率曲线的各设计频率下的设计值等。本程序可以计算特长系列。
    
为满足工程的实际需要，本程序除可用优选统计参数的方法适线外，还可用目估适线法进行适线。因为本程序在用优选法适线时，对各经验点据是给以等权重的处理。而当需要对各点据给以非等权重的处理时（如：设计洪水中要求多照顾首几项洪水；在年径流计算时要多照顾末端；或由于基本资料精度差等），单用优选法就不合适，此时可改用目估适线法。为了减少目估适线时的盲目性，实际使用时，一般采用优选与目估适线相结合的方法，即先用优选法选出一条通过点群中心的频率曲线。在此基础上再用目估的方法对优选出的参数$C_v, C_s$做少许调整，重新适线，以达到对各点据给以不同权重的目的，获得满意的结果。本程序在一张图上可绘多条频率曲线（用彩色加以区别），以供适线之用。

## class PearsonThree(cv, cs, avg=1)

+ base object

+ 假设已知皮尔逊三型曲线的各统计参数，进行相关计算及绘图。

#### Initialize Parameters：
+ :param cv: float 变差系数
+ :param cs: float 偏态系数
+ :param avg: float 均值（若单纯计算模比系数Kp，此项可不指定）

#### methods：
+ def set_param(cv, cs, avg)

重新进行参数设置

+ def calc_q(p):
		
计算指定频率的洪水流量，也可以重新指定均值用于计算图集

:param p: float 频率（注意是小数不是百分数）

:return: float 流量

+ def calc_kp(p):

计算指定频率的模比系数 Kp 值。

:param p:  float 频率（注意是小数不是百分数）

:return: kp float 模比系数 Kp 值

+ def show_curve(\*args, \*\*kwargs):

绘制图像

\*args, \*\*kwargs 参数如下：

:param pms: list 经验频率点 [(年份, 洪水流量，经验频率), ……]  所有数据包含历史特大洪水
	
:param survey: list 历史调查特大洪水年份列表 [年份1, 年份2, ……]（1、不包含连续系列中的特大洪水；2、仅不连续系列输入）

:param title: str 图像标题

:param colors: list 指定线条颜色列表

:param ticks: list 自定义X轴刻度标注, 单位为%，1表示频率为1%；格式为 ['.01', '1', ……] 或 [.1, .2, 1, ……]，最好为数字字符串，这样显示出来的与指定的完全一样，如果为数字，由于浮点数在计算机表示不是完全相等，会导致显示异常，例如 0.1 显示为 0.099999999999

+ save_curve(path, format='png', size=(15.3, 9.2), dpi=100, \*args, \*\*kwargs)

将曲线保存至文件

:param path: 文件保存路径。

:param format: str 图片文件格式， 详细支持格式见 matplotlib 文档

:param size: tuple 设置保存图片尺寸

:param dpi: int 设置保存图片的dpi

\*args, \*\*kwargs 参数同 show_curve 方法：

#### important parameters：

+ param = [cv, cs, avg] list 曲线的统计参数

+ distribution 使用 param 统计参数的 scipy.stats.gamma 实例对象 参考[https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html?highlight=gamma](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.gamma.html?highlight=gamma)

标准 Gamma 分布 ：
$$f(x,a) = \frac{x^{a-1}e^{-x}}{\Gamma (a)}$$

移动或缩放操作，使用$loc$和$scale=\frac{1}{\beta}$参数，则分布函数：

$$
\begin{align}
gamma.pdf(x, a, loc, scale) &= \frac{f(\frac{x - loc}{scale}, a)}{sacle} \\\\
     &= \frac{\beta^a \cdot (x - loc)^{a-1} \cdot e^{-\beta(x-loc)}} {\Gamma(a)}
\end{align}
$$

可以推出：P-III曲线总体三参数$[C_v, C_s, avg]$与Gamma分布三参数$[a, loc, scale]$换算关系如下：
$$a = \frac{4}{C_s^2}$$
$$loc = avg \cdot (1- \frac{2C_v}{C_s})$$
$$scale = \frac{avg \cdot C_v \cdot C_s}{2}$$

## class PearsonThreeFit(floods, survey=None, N=None, l=0, method='fit1', is_fit_avg=False, name='XX站')

+ base PearsonThree
+ 根据实测资料进行P-III 曲线拟合。由于继承自P-III 曲线类，可以进行P-III 曲线相关计算，计算方法来自（SL44-2006《水利水电工程设计洪水计算规范》）

#### Initialize Parameters
+ :param floods: list n*2 array like [(年份int, 洪水流量int), ……]  所有数据包含特大洪水
+ :param survey: list 历史调查特大洪水年份列表 [年份1, 年份2, ……]（1、不包含连续系列中的特大洪水；2、仅不连续系列输入）
+ :param N: int 重现期（仅不连续系列输入）
+ :param l: int 连续系列中的特大洪水项数（仅不连续系列输入）
+ :param method: str 估计参数的方法。
        "moment"->直接使用矩法；
	"fit1"->适线法_离差平方和准则，采用矩法初步估计，然后适线(默认)；
	"fit2"->适线法_离差绝对值和准则，采用矩法初步估计，然后适线；
	"fit3"->适线法_相对离差平方和准则，采用矩法初步估计，然后适线。
+ :param is_fit_avg: bool 适线时是否对均值进行寻优。True表示对均值寻优，False表示采用矩法计算的均值(默认)。
			在 method设置为非"moment"时生效。
+ :param name: str 站名。

#### methods：
+ def calc_pm()

计算经验频率。初始化对象的时候已经调用，计算结果保存至 对象的 pms 属性中，一般不需要调用此方法，避免重复计算，影响效率。

:return: list [(年份1, 流量1, 频率1), (年份2, 流量2, 频率2), ……]

+ def calc_statistic_param_moment()

矩法计算统计参数。初始化对象的时候已经调用，计算结果保存至 对象的 param_moment 属性中，一般不需要调用此方法，避免重复计算，影响效率。

:return: list [Cv, Cs, 均值]

+ def calc_statistic_param_fit(method=None)

使用矩法进行参数估计初值,然后用指定的准则优化拟合配线， 如果找不到最优解，将使用矩法估计的值

:param method:  见初始化的描述

:return: list [Cv, Cs, 均值]

+ def set_fit_method(method='fit1', is_fit_avg=False)

重新设置适先方法。

:param method: str 适线方法，具体见 __init__() 中的描述

:param is_fit_avg: bool 同__init__() 中的 is_fit_avg

:return: None

##### 以下方法继承自 PearsonThree 类 ，使用方法一致
+ def set_param(cv, cs, avg)
+ def calc_q(p):		
+ def calc_kp(p):
+ def show_curve(*args, **kwargs) 
+ def save_curve(path, format='png', size=(15.3, 9.2), dpi=100, \*args, \*\*kwargs)

#### important parameters:
+ param_moment list 距法估计的参数
+ pms list 实测系列的经验频率 [(年份1, 流量1, 频率1), (年份2, 流量2, 频率2), ……]
+ param = [cv, cs, avg] list 曲线的统计参数
+ distribution 使用 param 统计参数的 scipy.stats.gamma 实例对象


