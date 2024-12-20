import pywss
import pandas as pd
import numpy as np
import os
import json
from module import API_task2 
# from API_StudentInfo import student_info 
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
submit_record['time'] = pd.to_datetime(submit_record['time'], unit='s')
# print('maxdate:',max(submit_record['time']))
# print(submit_record.loc[0, 'time'])
maxWeekNum = 22

title_info = pd.read_csv(relative_path + 'Data_TitleInfo.csv')
full_score_sub_kg = title_info.groupby('sub_knowledge')['score'].sum()

def readSubmitRecord():
    submit_record = pd.read_csv(relative_path + 'All_Class/all_class_submit_record.csv')
    # submit_record = submit_record.drop_duplicates(subset=['student_ID','time']) # 去除数据处理时增加的重复数据
    submit_record['time'] = pd.to_datetime(submit_record['time'], unit='s')
    # submit_record['hour'] = submit_record['date'].dt.hour # 0-23
    # submit_record['day'] = submit_record['date'].dt.day # 1-31
    # submit_record['month'] = submit_record['date'].dt.month # 1-12
    return submit_record


def getScoreRatioByKnowledge(submit_record: pd.DataFrame, kg_level: str, week: int, student_list: list) -> pd.DataFrame:

    # 使用一个特殊的学生ID，将知识点得分率透视表的列名保存下来
    s = 'fdd714a996ac8bd8006d'
    isExist = s in student_list
    if not isExist:
        student_list.append(s) # 修改了形参student_list的值，但是不会影响到实参student_list的值

    submit_record_week = submit_record[submit_record['student_ID'].isin(student_list)]
    # 将指定时间之后的数据score字段置为0
    submit_record_week.loc[submit_record_week['time'] > pd.Timestamp('2023-8-31') + pd.Timedelta(week * 7, 'd'), 'score'] = 0
    # 以2023-8-31为初始时间，去除当前周数之后的submit_record
    # submit_record_week = submit_record[submit_record['time'] <= pd.Timestamp('2023-8-31') + pd.Timedelta(week * 7, 'd')]
    
    
    # 每道题目对应知识点最终得分率
    record_temp = submit_record_week.sort_values(by=['student_ID', 'title_ID', kg_level,'score'], ascending=[True, True, True, False])
    record_temp = record_temp.drop_duplicates(subset=['student_ID', 'title_ID', kg_level], keep='first')
    record_temp['score_ratio'] = record_temp['score'] / record_temp['full_score']
    # 每个学生每个知识点的平均得分率
    record_temp['score_ratio_per_kg'] = record_temp.groupby(['student_ID', kg_level])['score_ratio'].transform('mean')
    # 透视表：学生ID，知识点，得分率
    score_pivot = record_temp.pivot_table(index='student_ID', columns=kg_level, values='score_ratio_per_kg', aggfunc='first').fillna(0) # aggfunc：first mean max min效果都一样
    # 根据student_ID合并学生信息：student_ID, class
    # score_pivot = score_pivot.merge(record_temp.drop_duplicates(subset=['student_ID'])[['student_ID','class']], on='student_ID', how='left').fillna(0)
    score_pivot = score_pivot.merge(record_temp.drop_duplicates(subset=['student_ID'])[['student_ID']], on='student_ID', how='left').fillna(0)
    score_pivot = score_pivot.set_index('student_ID')
    # print(record_temp[record_temp['student_ID'] == 'zhx5rxgopln1p5hd10ql'][record_temp['knowledge'] == 'r8S3g'])

    # 从数据中删除特殊学生ID对应的数据
    if not isExist:
        # print('student_list:',student_list)
        student_list.remove(s)
        # print('score_pivot:',score_pivot)
        score_pivot = score_pivot.drop(s)
    

    return score_pivot

# 计算平均得分率(task2) 还是 计算 得分总分/总分(task1)，它们使用在了之前的两个任务中，现在需要考虑使用哪一个值更能体现学生的知识掌握水平
def resWeekViewData(ctx: pywss.Context):
    submit_record = readSubmitRecord()
    student_obj = ctx.json()['student_list']
    # 遍历student_list，键为cluster,值为student_list
    weekview_data = {}
    res_student_list = []
    for cluster, student_list in student_obj.items():
        # print(student_list)
        # 将student_list合并到res_student_list中
        res_student_list.extend(student_list)
        for week in range(1, maxWeekNum+1):
            mtx_sub_kg = getScoreRatioByKnowledge(submit_record, 'sub_knowledge', week, student_list)
            # mtx_sub_kg = mtx_sub_kg.set_index('student_ID')
            #输出列名
            # print('week:',week,',mtx_sub_kg.columns:',mtx_sub_kg.columns)
            # 遍历学生ID
            for student_id in student_list:
                # print(student_id)
                if student_id not in weekview_data:
                    weekview_data[student_id] = []
                week_item = { "name":'', "children": [],"score":0,'cluster':cluster}
                score = 0
                # 遍历full_score_sub_kg中每一个知识点
                for index, value in full_score_sub_kg.items():
                    # print(index, value) # b3C9s_j0v1yls8     4

                    skg = index.split('_')[1]
                    # 检测mtx_sub_kg.loc[student_id, index]是否存在，不存在则lr=0
                    # 修改getScoreRatioByKnowledge函数后，两者一定存在，故不用再判断
                    # if student_id in mtx_sub_kg.index and index in mtx_sub_kg.columns:
                    #     lr = mtx_sub_kg.loc[student_id, index]
                    # else:
                    #     lr = 0
                    # item = { "name":skg, "value":value, "lr":lr }
                    item = { "name":skg, "value":value, "lr":mtx_sub_kg.loc[student_id, index],'cluster':cluster }
                    week_item["children"].append(item)
                    # 计算学生所有知识点得分
                    score += item['lr'] * item['value']
                week_item['score'] = score
                weekview_data[student_id].append(week_item)
     
    # res = {"status":0, "res_data":{ "name": "knowledge", "children": sunburst_data }}
    res = {"status":0, "res_data":weekview_data, 'res_student_list':res_student_list}
    ctx.write(res)

def find_index(list, name):
    for i in range(0, len(list)):
        if list[i]["name"] == name:
            return i
    return -1

# 返回某一个群体的知识点得分率，群体为学生聚类号码、班级号码、学生ID列表
def resKnowledgeSunburstData(ctx: pywss.Context):
    submit_record = readSubmitRecord()
    student_list_part = ctx.json()['student_list']
    student_cluster = ctx.json()['student_cluster']
    student_class = ctx.json()['student_class']
    week = ctx.json()['week']
    print('student_list_part, student_cluster, student_class, week',student_list_part, student_cluster, student_class, week)

    # if not student_list:
    if student_cluster > -1:
        student_list = API_task2.features[API_task2.features['kmeans_cluster'] == student_cluster].index.tolist()
    elif student_class:
        student_list = API_StudentInfo.student_info[API_student_info.student_info['class'] == student_class].index.tolist()

    mtx_kg = getScoreRatioByKnowledge(submit_record, 'knowledge', week, student_list) # 学生-一级知识点得分率
    # mtx_kg = mtx_kg.set_index('student_ID')
    mtx_sub_kg = getScoreRatioByKnowledge(submit_record, 'sub_knowledge', week, student_list) # 学生-二级知识点得分率
    # mtx_sub_kg = mtx_sub_kg.set_index('student_ID')

    mtx_kg_mean = mtx_kg.mean()
    # 对mtx_sub_kg每个字段求平均值
    mtx_sub_kg_mean = mtx_sub_kg.mean()
    # 访问一级知识点xxx的平均得分率
    
    # 取出student_list_part学生ID对应的mtx_kg，mtx_sub_kg各个字段的平均值
    mtx_kg_part_mean = mtx_kg.loc[student_list_part].mean()
    mtx_sub_kg_part_mean = mtx_sub_kg.loc[student_list_part].mean()


    sunburst_data = []
    for index, value in full_score_sub_kg.items():
        # print(index, value) # b3C9s_j0v1yls8     4
        kg = index.split('_')[0]
        skg = index.split('_')[1]
        item = { "name":index, "value":value, "lr":mtx_sub_kg_mean.loc[index], 'lr_part':mtx_sub_kg_part_mean.loc[index] }
        idx = find_index(sunburst_data, kg)
        if idx  == -1:
            sunburst_data.append({"name":kg, "children":[item], "lr":mtx_kg_mean.loc[kg], 'lr_part':mtx_kg_part_mean.loc[kg]})
        else:
            sunburst_data[idx]["children"].append(item)

    res = {"status":0, "res_data":{ "name": "knowledge", "children": sunburst_data }}

    ctx.write(res)

def register(app: pywss.App):
    # 返回学生每周答题情况
    app.post("/weekview", resWeekViewData)
    app.post("/knowledge_lr", resKnowledgeSunburstData) # 返回某一个群体的知识点得分率，群体为学生聚类号码、班级号码、学生ID列表



