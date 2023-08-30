import pandas as pd
import numpy as np

import Method_fault_analyzer
from Method_fault_analyzer import PumpFailureAnalyzer

# 指定要生成的数据数量
n = 1000
# 生成序号、时间戳、油流量和进油压力随机数列
serial = np.arange (1,n+1) # 序号，从1到n递增
timing = pd.date_range(start='2023-01-01 12:00:01',freq='s',periods=n) # 时间戳，从指定时间开始每秒递增
oilFlow = np.random.uniform(low=-1,high=360,size=n).round(decimals=4) # 油流量，随机生成区间[-1,360]的数值，保留四位小数
inletOilPres = np.random.uniform(low=0.01,high=0.327,size=n).round(decimals=4) # 进油压力，随机生成区间[0.01,0.327]的数值，保留四位小数
# 将数据列合并成一个DataFrame
df = pd.DataFrame({'serial':serial,'timing':timing,'oilFlow':oilFlow,'inletOilPres':inletOilPres})
print (df.head()) # 默认返回前5行
analyzer = PumpFailureAnalyzer()
for index,row in df.iterrows():
    # 使用df.iterrows()遍历DataFrame的每一行数据，从每一行中获取序号、时间戳、油流量和进油压力
    serial = row['serial']
    timing = row['timing']
    oilFlow = row['oilFlow']
    inletOilPres = row['inletOilPres']
    analyzer.detect_failure(serial,timing,oilFlow,inletOilPres)
analyzer.save_results_to_csv("d:/Work_data/pump_old_data/your_output_file.csv")
analyzer.visualize_data(df)


