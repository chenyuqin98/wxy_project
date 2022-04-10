import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_regression
import statsmodels.api as sm


def read(file_name):
    df = pd.read_csv(file_name, encoding="utf8", skiprows=1, sep='\t')
    df = df[df.报表类型编码=='A']
    return df

if __name__ == "__main__":
    # list = ['价值', '偿债能力', '盈利能力', '经营能力', ]
    value = pd.read_csv('价值.txt', encoding="utf8", skiprows=1, sep='\t')
    solvency = read('偿债能力.txt')
    profitability = read('盈利能力.txt')
    management = read('经营能力.txt')
    print(value.shape, solvency.shape, profitability.shape, management.shape)

    merged = pd.merge(value, solvency, how='left', on=['股票代码','截止日期','行业名称','行业代码'])
    merged = pd.merge(merged, profitability, how='left', on=['股票代码', '截止日期','行业名称','行业代码'])
    merged = pd.merge(merged, management, how='left', on=['股票代码', '截止日期','行业名称','行业代码'])
    all_list = merged.columns.values.tolist()
    # selected_column = ['托宾Q值A', '流动比率', '速动比率', '营运资金与借款比', '资产负债率',
    #             '权益对负债比率', '长期资本负债率', '资产报酬率B',
    #             '总资产净利润率（ROA）B', '流动资产净利润率B', '固定资产净利润率B', '净资产收益率B',
    #             '投入资本回报率', '长期资本收益率', '营业成本率', '营业净利率',
    #             '销售费用率', '管理费用率', '财务费用率', '投资收益率', '研发费用率',
    #             '应收账款周转率B', '存货周转率B', '应付账款周转率B',
    #             '营运资金（资本）周转率B', '流动资产周转率B', '固定资产周转率B',
    #             '非流动资产周转率B', '总资产周转率B', '股东权益周转率B']
    selected_column = ['托宾Q值A', '流动比率', '速动比率', '营运资金与借款比', '资产负债率',
                       '权益对负债比率', '长期资本负债率', '营业成本率', '营业净利率',
                       '销售费用率', '管理费用率', '财务费用率', '投资收益率', '研发费用率',
                       '应收账款周转率B', '存货周转率B', '应付账款周转率B',
                       '营运资金（资本）周转率B', '流动资产周转率B', '固定资产周转率B',
                       '非流动资产周转率B', '总资产周转率B', '股东权益周转率B']
    print('', len(selected_column))
    selected_data = merged[selected_column]

    # print('na :', selected_data.isnull().any())
    selected_data = selected_data.dropna()
    # print('na :', selected_data.isnull().any())
    print('dropna: ', merged.shape, selected_data.shape)

    x, y = selected_data.drop(['托宾Q值A'], axis=1), selected_data['托宾Q值A']
    print(x.shape, y.shape)


    features_num = 3
    X_new = SelectKBest(f_regression, k=features_num).fit_transform(x, y)
    selector = SelectKBest(f_regression, k=features_num)
    # x_new = selector.fit(x, y)
    selector.fit(x, y)
    # selector.get_support()
    features_in = x.columns.values.tolist()
    p_values = selector.scores_
    x_new = selector._get_support_mask()
    print(features_num, ' features to select, result features: ')
    for i in range(len(x_new)):
        if x_new[i] ==True:
            print(features_in[i])
    # print(X_new)
    model = sm.OLS(y, X_new)
    rlt = model.fit()
    print(rlt.summary())
