import pywss
import pandas as pd
import numpy as np
import os
import json
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import SpectralClustering
from sklearn.mixture import GaussianMixture
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
from module import API_StudentInfo 

# relative_path = "../../sourcedata/"
# 获取当前文件路径
curPath = os.path.abspath(os.path.dirname(__file__))
# print(curPath)
# curpath向上2级路径即为rootpath
rootPath = '/'.join(curPath.split(os.path.sep)[:-2])
# print('rootPath:',rootPath)
# 与relative_path拼接
relative_path = rootPath + '/sourcedata/'
submit_record = pd.read_csv(relative_path + 'All_Class/all_class_submit_record.csv')
title_info = pd.read_csv(relative_path + 'Data_TitleInfo.csv')
# 统计每个知识点的题目数量，以字典形式存储
knowledge_count = title_info['knowledge'].value_counts().to_dict()

# 将时间戳转换为日期时间格式
submit_record['time'] = pd.to_datetime(submit_record['time'], unit='s')

# 提取时间特征
submit_record['hour'] = submit_record['time'].dt.hour # 0-23
submit_record['day'] = submit_record['time'].dt.day # 1-31
submit_record['month'] = submit_record['time'].dt.month # 1-12
# 按时间特征统计答题量
hourly_data = submit_record.groupby('hour').size()
daily_data = submit_record.groupby('day').size()
monthly_data = submit_record.groupby('month').size()

# 答题正确率
submit_record['is_correct'] = submit_record['state'].apply(lambda x: 1 if x == 'Absolutely_Correct' else 0)

# 计算每个学生的每个1级知识点总的尝试次数
submit_record['attempts_per_kg'] = submit_record.groupby(['student_ID', 'knowledge'])['index'].transform('count')
# 转换为宽格式 aggfunc='first' 聚合函数，用于处理重复的索引值，first表示取第一个值 pivot_table()函数用于数据透视表
knowledge_pivot = submit_record.pivot_table(index='student_ID', columns='knowledge', values='attempts_per_kg', aggfunc='mean').fillna(0)
# 每种知识点的尝试次数除以该知识点的题目数量，得到每种知识点的平均尝试次数
knowledge_pivot = knowledge_pivot / knowledge_pivot.columns.map(knowledge_count)
# 重命名列名（可选）
knowledge_pivot.columns = [f'attempts_{col}' for col in knowledge_pivot.columns]

# 计算特征
features = submit_record.groupby('student_ID').agg({
    # hour的计算有错误
    # 'hour': lambda x: x.value_counts().idxmax(), # 最常答题的时间段 匿名函数作用是返回出现次数最多的值 .value_counts()统计每个值出现的次数 .idxmax()返回出现次数最多的值
    'method': lambda x: x.value_counts().idxmax(), # 最常用的方法
})
# 这行代码的作用是将多级列索引转换为单级索引，并且分配容易理解的列名。
features.columns = [
    # 'most_common_hour', 
    'most_common_method', 
]

# 学生的活跃天数，需要注意答题记录中包含5个月的数据
temple_submit_record = submit_record.drop_duplicates(subset=['student_ID', 'month','day'], keep='first')
features['active_days'] = temple_submit_record.groupby('student_ID')['day'].count()

# 每个学生的答题时长 可能与题目尝试次数相关
temple_submit_record = submit_record.drop_duplicates(subset=['student_ID', 'month','day','hour'], keep='first')
features['learn_hours'] = temple_submit_record.groupby('student_ID')['hour'].count()
features['most_common_hour'] = temple_submit_record.groupby('student_ID').agg({'hour': lambda x: x.value_counts().idxmax()}) # 保证每个学生每天答题时间段只被计算一次

# 每道题目对应知识点最终得分率
submit_record = submit_record.sort_values(by=['student_ID', 'title_ID', 'knowledge','score'], ascending=[True, True, True, False])
submit_record = submit_record.drop_duplicates(subset=['student_ID', 'title_ID', 'knowledge'], keep='first')
submit_record['score_ratio'] = submit_record['score'] / submit_record['full_score']
# 每个学生每个知识点的平均得分率
submit_record['score_ratio_per_kg'] = submit_record.groupby(['student_ID', 'knowledge'])['score_ratio'].transform('mean')
score_pivot = submit_record.pivot_table(index='student_ID', columns='knowledge', values='score_ratio_per_kg', aggfunc='first').fillna(0)
score_pivot.columns = [f'score_ratio_{col}' for col in score_pivot.columns]

# 计算学生总的得分
submit_record = submit_record.sort_values(by=['student_ID', 'title_ID', 'score'], ascending=[True, True, False])
submit_record = submit_record.drop_duplicates(subset=['student_ID', 'title_ID'], keep='first')
features['total_score'] = submit_record.groupby('student_ID')['score'].sum()


# 合并到特征表 how='left'表示左连接,左连接表示以左表为基础，右表中的数据只要在左表中有对应的就会被合并到一起，没有对应的就会被舍弃。
# fillna(0)表示将缺失值填充为0
features = features.merge(knowledge_pivot, on='student_ID', how='left').fillna(0)
features = features.merge(score_pivot, on='student_ID', how='left').fillna(0)

# 编码分类特征 .astype('category')表示将数据转换为分类数据，.cat.codes表示将分类数据转换为数值数据 
# 通过这种方式可以将分类数据转换为数值数据
# 对于某些非数值型特征（如小时、方法），我们需要将其转换为数值型以便于聚类分析。
# 作用是将最常答题的小时从类别类型转换为数值型编码。
# features['most_common_hour'] = features['most_common_hour'].astype('category').cat.codes
features['most_common_method'] = features['most_common_method'].astype('category')
method2code = features['most_common_method'].cat.categories.to_list()
features['most_common_method'] = features['most_common_method'].cat.codes
# features['major'] = features['major'].astype('category').cat.codes
# 输出most_common_method中方法名称与cat.codes的对应关系
# print(features['most_common_method'].cat.categories.to_list())

# 标准化特征
num_clusters = 6
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)
# 层次聚类
hierarchical = AgglomerativeClustering(n_clusters=num_clusters)
features['hierarchical_cluster'] = hierarchical.fit_predict(scaled_features)
# t-SNE降维
tsne = TSNE(n_components=2, random_state=42)
tsne_features = tsne.fit_transform(scaled_features)
# 添加t-SNE结果到features中
features['tsne_one'] = tsne_features[:, 0]
features['tsne_two'] = tsne_features[:, 1]

cluster_centers = features.drop(['tsne_one', 'tsne_two'], axis=1).groupby('hierarchical_cluster').mean()
# cluster_centers['most_common_hour'] = features.groupby('hierarchical_cluster').agg({'most_common_hour' : lambda x : x.value_counts().idxmax()})
cluster_centers['most_common_hour'] = features.groupby('hierarchical_cluster').agg({'most_common_hour' : 'median'})
cluster_centers['most_common_method'] = features.groupby('hierarchical_cluster').agg({'most_common_method' : lambda x : x.value_counts().idxmax()})

# print(cluster_centers)

def resStuClusterData(ctx: pywss.Context):
    cluster_ids = cluster_centers.index.values.tolist()
    cluster_data = []

    for _, value in cluster_centers.iterrows():
        cluster_data.append(value.to_list())

    indicator = []
    for axisname in cluster_centers.columns.values:
        indicator.append({"name":axisname, 
                        #   "max":features[axisname].max(), "min":features[axisname].min()
                          })

    res = {"status":0, "res_data":{ "cluster_ids": cluster_ids, "method2code": method2code, "cluster_data": cluster_data, 'indicator': indicator}}
    res = json.dumps(res, default=API_StudentInfo.default_dump)
    ctx.write(res)

posByCluster = []
def getPos(x:pd.DataFrame):
    y = x[['tsne_one', 'tsne_two']]
    pos = []
    for _, value in y.iterrows():
        pos.append(value.to_list())
    posByCluster.append(pos)

def resScatterData(ctx: pywss.Context):
    df = features.groupby('hierarchical_cluster')
    cluster_ids = [index for index, _ in df]
    df.apply(getPos)
    res = {"status":0, "res_data":{ "pos": posByCluster, "cluster_ids": cluster_ids }}
    res = json.dumps(res, default=API_StudentInfo.default_dump)

    ctx.write(res)

def readSubmitRecord():
    submit_record = pd.read_csv(relative_path + 'All_Class/all_class_submit_record.csv')
    submit_record = submit_record.drop_duplicates(subset=['student_ID','time']) # 去除数据处理时增加的重复数据
    submit_record['time'] = pd.to_datetime(submit_record['time'], unit='s')
    submit_record['hour'] = submit_record['time'].dt.hour # 0-23
    submit_record['day'] = submit_record['time'].dt.day # 1-31
    submit_record['month'] = submit_record['time'].dt.month # 1-12
    return submit_record

def getAttemptsByHour(submit_record: pd.DataFrame):
    learn_time_day = submit_record.groupby(['student_ID' ,'month', 'day', 'hour']).agg({'index': 'count'}).reset_index()
    learn_time_day = learn_time_day.groupby(['student_ID', 'hour']).agg({'index': 'sum'}).reset_index()
    # learn_time_day['time'] = learn_time_day['month'].astype(str) + '-' + learn_time_day['day'].astype(str)
    # learn_time_day = learn_time_day.drop(['month', 'day'], axis=1)
    # learn_time_day = learn_time_day.pivot(index='time', columns='hour', values='index').fillna(0)
    learn_time_day = learn_time_day.pivot(index='student_ID', columns='hour', values='index').fillna(0)
    return learn_time_day

def test_getAttemptsByHour():
    submit_record = readSubmitRecord()
    learn_time_day = getAttemptsByHour(submit_record)
    learn_time_day = learn_time_day.merge(features['hierarchical_cluster'], on='student_ID', how='left').fillna(0)
    print('learn_time_day:',learn_time_day[:5])
# test_getAttemptsByHour()

def resRiverFlowData(ctx: pywss.Context):
    submit_record = readSubmitRecord()
    learn_time_day = getAttemptsByHour(submit_record)
    learn_time_day = learn_time_day.merge(features['hierarchical_cluster'], on='student_ID', how='left').fillna(0)
    # data_by_group = learn_time_day.groupby('hierarchical_cluster').sum()
    data_by_group = learn_time_day.groupby('hierarchical_cluster').mean()
    # 将data_by_group转换为二维list:[[time, value, group],...]
    river_data = []
    for group, data in data_by_group.iterrows():
        for col in data.index:
            river_data.append([col, data[col], group])

    res = {"status":0, "res_data":river_data}
    res = json.dumps(res, default=API_StudentInfo.default_dump)
    ctx.write(res)

def resAttempsAndCorrectLineData(ctx: pywss.Context):
    submit_record = readSubmitRecord()
    attemptsByTitle = submit_record.groupby(['student_ID', 'title_ID']).agg({'index': 'count'}).reset_index()
    attemptsByTitle = attemptsByTitle.pivot(index='student_ID', columns='title_ID', values='index').fillna(0)
    attemptsByTitle = attemptsByTitle[title_info['title_ID'].unique()] # 按顺序排列
    attemptsByTitle = attemptsByTitle.merge(features['hierarchical_cluster'], on='student_ID', how='left').fillna(0)

    # submit_record['is_correct'] = submit_record['state'].apply(lambda x: 1 if x == 'Absolutely_Correct' else 0)
    submit_record['is_correct'] = submit_record['score'] / submit_record['full_score'] # 将得分率作为正确率
    correctByTitle = submit_record.groupby(['student_ID', 'title_ID']).agg({'is_correct': 'mean'}).reset_index().pivot(index='student_ID', columns='title_ID', values='is_correct').fillna(0)
    correctByTitle = correctByTitle[title_info['title_ID'].unique()] # 按顺序排列
    correctByTitle = correctByTitle.merge(features['hierarchical_cluster'], on='student_ID', how='left').fillna(0)

    #
    attempts = attemptsByTitle.groupby('hierarchical_cluster').mean()
    attempts_index = attempts.index.values
    attempts_list = attempts.values.tolist()
    correct = correctByTitle.groupby('hierarchical_cluster').mean()
    correct_index = correct.index.values
    correct_list = correct.values.tolist()

    # 
    res = {"status":0, "res_data":{ "attempts": {"index": attempts_index.tolist(), "data": attempts_list}, "correct": {"index": correct_index.tolist(), "data": correct_list}, "title": title_info['title_ID'].unique().tolist() }}
    res = json.dumps(res, default=API_StudentInfo.default_dump)
    ctx.write(res)

def register(app: pywss.App):
    # app.get("/knowledge_lr", resKnowledgeSunburstData)
    # app.get("/answer_state", resAnswerStateData)
    # app.get("/student_activity", resHeatMapData)
    app.get("/student_clusters", resStuClusterData) 
    app.get("/tsne_dr", resScatterData) 
    app.get("/day_activity_river", resRiverFlowData)
    app.get("/attempts_correct", resAttempsAndCorrectLineData)