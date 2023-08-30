"""
Classes
-------
1. PumpFailureAnalyzer: 断泵故障分析.
	* 基于DataFrame中油流量（oilFlow）和进油压力（inletOilPres）两个特征值输入建立断泵故障数据模型.
	* DataFrame有四列数据（序号serical、时间戳timing、油流量oilFlow、进油压力inletOilPres），serical为整数int类型（1,2,3...),timing时间戳(2017-11-10 15:13:01、2017-11-10 15:13:02、2017-11-10 15:13:03...)，油流量oilflow为区间[-1,360]的double(9,4)随机数，进油压力inletoilpres为区间[0.01,0.327]的double(9,4)随机数
	* 利用for循环语句进行单个数据流读取数据，将读取的两个特征值进入缓冲区间为5的缓冲区，输出DataFrame数据类型序号（serical）、（oilFlow）、时间戳（timing）、进油压力（inletOilPres）
    * 基于数据运行趋势且细化判断流程的故障判断方法
    * 判断条件：油流量突然大幅降低；低于额定值的90%；泵进油压力突然大幅降低；低于额定值的80%；




Methods
---------
1. detect_failure:检测断泵故障.
	- 输入输出数据均为df,将油流量和进油压力加入缓冲区

2. calculate_change_rate:计算油流量、压力的变化率，np.polyfit()函数是用于拟合多项式函数的函数.


3. save_results_to_csv:将监测结果保存到csv文件中.


4. visualize_data:可视化数据.

"""

from . import *
