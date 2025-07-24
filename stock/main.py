import tushare as ts
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 初始化Tushare Pro (替换your_token)
pro = ts.pro_api('872881b185c7d82a99f42725b4aaefb949c6f451520fb251780889c2')


class DragonHeadStrategy:
    def __init__(self):
        self.today = datetime.now().strftime('%Y%m%d')
        self.yesterday = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
        self.stock_pool = []

    def get_basic_data(self):
        """获取基础数据"""
        # 获取当日涨停股票
        limit_up = pro.limit_list(trade_date=self.today)

        # 获取龙虎榜数据
        top_list = pro.top_list(trade_date=self.today)
        # 获取资金流向
        moneyflow = pro.moneyflow(trade_date=self.today)

        return limit_up, top_list, moneyflow

    def calculate_factors(self, data):
        """计算龙头因子"""
        print(data)
        df = data.copy()
        print(df)
        return
        # 空间高度因子
        df['连板天数'] = df['连续涨停天数']
        df['历史连板基因'] = df['股票代码'].apply(lambda x: self.check_history(x))

        # 强度因子
        df['早盘涨停'] = df['首次封板时间'] < '103000'
        df['封单强度'] = df['封板资金'] / df['成交额']

        # 板块协同因子
        industry = pro.stock_basic()
        df = pd.merge(df, industry[['ts_code', 'industry']], left_on='股票代码', right_on='ts_code')
        industry_rank = df.groupby('industry')['涨幅%'].mean().rank(ascending=False)
        df['板块排名'] = df['industry'].map(industry_rank)

        # 资金记忆因子
        top_list = pro.top_list(trade_date=self.today)
        df['知名游资'] = df['股票代码'].isin(top_list[top_list['buyer'].str.contains('拉萨')]['股票代码'])

        # 动态评估因子
        df['爆量回封'] = (df['换手率'] > df['换手率'].shift(1) * 1.5) & (df['打开次数'] > 0)

        return df

    def check_history(self, ts_code):
        """检查历史连板基因"""
        hist = pro.limit_list(ts_code=ts_code, start_date='20230101', end_date=self.yesterday)
        return 1 if hist['连续涨停天数'].max() >= 5 else 0

    def filter_stocks(self, df):
        """执行因子筛选"""
        # 基础识别因子
        cond1 = df['连板天数'] >= 3
        cond2 = df['早盘涨停'] == True
        cond3 = df['封单强度'] > 0.2
        cond4 = df['板块排名'] <= 3

        # 进阶确认因子
        cond5 = df['连板天数'] == df['连板天数'].max()  # 空间龙
        cond6 = df['知名游资'] == True

        # 风险排除
        cond7 = df['流通市值'] < 200
        cond8 = ~df['股票名称'].str.contains('ST')

        filtered = df[cond1 & cond2 & cond3 & cond4 & cond5 & cond6 & cond7 & cond8]
        return filtered

    def visualize_results(self, df):
        """可视化结果"""
        plt.figure(figsize=(12, 6))

        # 因子满足数量分布
        factors = ['连板天数', '早盘涨停', '封单强度', '板块排名', '知名游资']
        df['因子得分'] = df[factors].sum(axis=1)
        df['因子得分'].value_counts().sort_index().plot(kind='bar')
        plt.title('龙头因子得分分布')

        # 板块分布
        plt.figure(figsize=(10, 5))
        df['industry'].value_counts()[:5].plot(kind='pie', autopct='%1.1f%%')
        plt.title('龙头股行业分布')

        plt.show()

    def run(self):
        """执行策略"""
        print(f"正在执行龙头战法选股({self.today})...")

        # 数据获取与计算
        limit_up, top_list, moneyflow = self.get_basic_data()
        df = self.calculate_factors(limit_up)

        # 因子筛选
        result = self.filter_stocks(df)
        self.stock_pool = result[['股票代码', '股票名称', '连板天数', '涨幅%', 'industry']]

        # 结果展示
        print(f"\n筛选出{len(result)}只龙头候选股:")
        print(self.stock_pool)
        self.visualize_results(result)

        return self.stock_pool


# 运行策略
strategy = DragonHeadStrategy()
dragon_stocks = strategy.run()