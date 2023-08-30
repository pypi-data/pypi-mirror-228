import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
class PumpFailureAnalyzer:
    def __init__(self, buffer_size=5):
        """
        初始化断泵分析模型监测类
        :param buffer_size: 缓冲区大小。默认为5
        """
        self.buffer_size = buffer_size  # 缓冲区大小
        self.oilFlow_buffer = []  # 油流量缓冲区
        self.inletOilPres_buffer = []  # 进油压力缓冲区
        self.failure_timestamps = []  # 存储断泵故障发生的时间戳
    # 检测断泵故障
    def detect_failure(self, serial, timing, oilFlow, inletOilPres):
        """
        检测断泵故障
        :param serial: 序号,str:int
        :param timing: 时间戳,str:timestamp
        :param oilFlow: 油流量,str:double(9,4)
        :param inletOilPres: 进油压力,str:double(9,4)
        :return:
        """
        # 将油流量和进油压力加入缓冲区
        if len(self.oilFlow_buffer) < self.buffer_size:
            self.oilFlow_buffer.append(oilFlow)
            self.inletOilPres_buffer.append(inletOilPres)
            return
        self.oilFlow_buffer.pop(0)
        self.inletOilPres_buffer.pop(0)
        self.oilFlow_buffer.append(oilFlow)
        self.inletOilPres_buffer.append(inletOilPres) # 更新缓冲区数据
        pressure_change_rate = self.calculate_change_rate(self.inletOilPres_buffer)
        flow_change_rate = self.calculate_change_rate(self.oilFlow_buffer)

        if (pressure_change_rate > -0.04 or inletOilPres < (0.303 * 0.8)) and (flow_change_rate > -0.05 or oilFlow < (337 * 0.9)):
                fault_status = '疑似断泵'
                self.failure_timestamps.append(timing)
        else:
            fault_status = '正常'
    def calculate_change_rate(self,data):
        timestamps = np.arange(len(data)) # 生成时间戳序列
        if data is not None:
            coeffs = np.polyfit(timestamps,data,1) # 计算油流量、压力的变化率，np.polyfit()函数是用于拟合多项式函数的函数，1表示
            trend = coeffs[0] # coeffs[0]表示斜率，油流量的变化率
            return trend
        return
    # 将监测结果保存到csv文件中
    def save_results_to_csv(self, output_path):
        results = pd.DataFrame({'timestamp': self.failure_timestamps})
        results.to_csv(output_path, index=False)
        print(f"检测结果已保存至 {output_path}")
        # 可视化数据
    def visualize_data(self,df):
        serials = np.arange(len(df)) # 创建时间序列，长度和缓冲区数据相同
        oilFlows = df['oilFlow']
        inletOilPres = df['inletOilPres']
        fig, ax1 = plt.subplots(constrained_layout=True)
        ax2 = ax1.twinx()
        line1, = ax1.plot(serials,oilFlows, '-',color='r',linewidth = 2.0,label = 'oilFlow' )
        line2, = ax2.plot( serials,inletOilPres, '-', color='b', linewidth=2.0,label = 'inlet_oil_Pres')
        plt.legend((line1,line2),('oilFlow','inlet_oil_pres'),frameon=False,loc="lower right",fontsize='small')
        ax1.set_title('oilFlow and inlet_oil_pres')
        ax1.set_ylabel('oilFlow',fontsize = 14)
        ax2.set_ylabel('inlet_oil_pres', fontsize=12)
        plt.show()










