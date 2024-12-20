import pywss
import pandas as pd
import numpy as np
import os
import json
# from API_StudentInfo import student_info 
# from module import API_StudentInfo 

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


def getScoreRatioByKnowledge(submit_record: pd.DataFrame, kg_level: str):
    # 每道题目对应知识点最终得分率
    record_temp = submit_record.sort_values(by=['student_ID', 'title_ID', kg_level,'score'], ascending=[True, True, True, False])
    record_temp = record_temp.drop_duplicates(subset=['student_ID', 'title_ID', kg_level], keep='first')
    record_temp['score_ratio'] = record_temp['score'] / record_temp['full_score']
    # 每个学生每个知识点的平均得分率
    record_temp['score_ratio_per_kg'] = record_temp.groupby(['student_ID', kg_level])['score_ratio'].transform('mean')
    score_pivot = record_temp.pivot_table(index='student_ID', columns=kg_level, values='score_ratio_per_kg', aggfunc='first').fillna(0) # aggfunc：first mean max min效果都一样
    # score_pivot.columns = [f'score_ratio_{col}' for col in score_pivot.columns]
    # score_pivot = score_pivot.merge(API_StudentInfo.student_info[['student_ID', 'class']], on='student_ID', how='left').fillna(0)
    score_pivot = score_pivot.merge(record_temp.drop_duplicates(subset=['student_ID'])[['student_ID','class']], on='student_ID', how='left').fillna(0)
    # print(record_temp[record_temp['student_ID'] == 'zhx5rxgopln1p5hd10ql'][record_temp['knowledge'] == 'r8S3g'])

    return score_pivot


mtx_kg = getScoreRatioByKnowledge(submit_record, 'knowledge')
mtx_kg = mtx_kg.set_index('student_ID')
# print(mtx_kg.iloc[-10:])
mtx_sub_kg = getScoreRatioByKnowledge(submit_record, 'sub_knowledge')
mtx_sub_kg = mtx_sub_kg.set_index('student_ID')
# print(mtx_sub_kg.iloc[-10:])

full_score_kg = title_info.groupby('knowledge')['score'].sum()
full_score_sub_kg = title_info.groupby('sub_knowledge')['score'].sum()

def find_index(list, name):
    for i in range(0, len(list)):
        if list[i]["name"] == name:
            return i
    return -1

# 计算平均得分率(task2) 还是 计算 得分总分/总分(task1)，它们使用在了之前的两个任务中，现在需要考虑使用哪一个值更能体现学生的知识掌握水平
def resKnowledgeSunburstData(ctx: pywss.Context):
    print(ctx.url_params)
    student_id = ctx.url_params['student_id']
    # class_id = ctx.url_params['class_id']
    # 遍历full_score_sub_kg
    sunburst_data = []
    for index, value in full_score_sub_kg.items():
        # print(index, value) # b3C9s_j0v1yls8     4
        kg = index.split('_')[0]
        skg = index.split('_')[1]
        item = { "name":index, "value":value, "lr":mtx_sub_kg.loc[student_id, index] }
        idx = find_index(sunburst_data, kg)
        if idx  == -1:
            sunburst_data.append({"name":kg, "children":[item], "lr":mtx_kg.loc[student_id, kg]})
        else:
            sunburst_data[idx]["children"].append(item)

    res = {"status":0, "res_data":{ "name": "knowledge", "children": sunburst_data }}

    ctx.write(res)

def resAnswerStateData(ctx: pywss.Context):
    student_id = ctx.url_params['student_id']
    kg = ctx.url_params['kg']
    column_str = 'knowledge'
    if len(kg) > 10:
        column_str = 'sub_knowledge'

    temp_record = submit_record[submit_record['student_ID'] == student_id]
    temp_record = temp_record[temp_record[column_str] == kg]
    state_count = temp_record['state'].value_counts().to_dict()
    # title_count = temp_record.groupby('state')['title_ID'].value_counts()
    # print('state_count:',state_count)

    series = []
    item = { 'name': 'stateCount', 'type': 'bar', 'emphasis':{ 'focus':'series' }, 'data': [] }
    yAxis = sorted(state_count.keys())
    item['data'] = [state_count[state] for state in yAxis]
    series.append(item)

    titles = temp_record['title_ID'].unique()
    for title in titles:
        # title_series = { 'name': title, 'type': 'bar', 'data': []}
        title_state_count = temp_record[temp_record['title_ID'] == title]['state'].value_counts().to_dict()
        series.append({ 'name': title, 'type': 'bar', 'stack': 'question','emphasis':{ 'focus':'series' }, 'data': [title_state_count.get(state, 0) for state in yAxis] })
    
    res = {"status":0, "res_data":series, 'yAxis': yAxis}
    ctx.write(res)

def test_resAnswerStateData():
    student_id = 'zhx5rxgopln1p5hd10ql'
    kg = 'm3D1v'
    column_str = 'knowledge'
    if len(kg) > 10:
        column_str = 'sub_knowledge'

    temp_record = submit_record[submit_record['student_ID'] == student_id]
    temp_record = temp_record[temp_record[column_str] == kg]
    state_count = temp_record['state'].value_counts().to_dict()
    # title_count = temp_record.groupby('state')['title_ID'].value_counts()
    # print('state_count:',state_count)

    series = []
    item = { 'name': 'stateCount', 'type': 'bar', 'data': [] }
    yAxis = sorted(state_count.keys())
    item['data'] = [state_count[state] for state in yAxis]
    series.append(item)

    titles = temp_record['title_ID'].unique()
    for title in titles:
        # title_series = { 'name': title, 'type': 'bar', 'data': []}
        title_state_count = temp_record[temp_record['title_ID'] == title]['state'].value_counts().to_dict()
        series.append({ 'name': title, 'type': 'bar', 'data': [title_state_count.get(state, 0) for state in yAxis] })
    # print('series:',series)
    # print('title_count:',title_count)
# test_resAnswerStateData()

def resHeatMapData(ctx: pywss.Context):
    student_id = ctx.url_params['student_id']
    temp_record = submit_record[submit_record['student_ID'] == student_id].copy()
    temp_record['time'] = pd.to_datetime(temp_record['time'], unit='s')
    temp_record['hour'] = temp_record['time'].dt.hour # 0-23
    temp_record['time'] = temp_record['time'].dt.date
    learn_time_day = temp_record.groupby(['time']).agg({'hour': lambda x: x.unique().size}).to_csv()
    res_data = []
    # 将csv_format单行保存为list, push到res_data中
    for line in learn_time_day.split('\r\n')[1:]: # 第一行是time,hour
        if line == '':
            break
        res_data.append(line.split(','))


    res = {"status":0, "res_data":res_data}
    ctx.write(res)

def test_resHeatMapData(submit_record: pd.DataFrame, student_id: str):

    # student_id = 'zhx5rxgopln1p5hd10ql'
    temp_record = submit_record[submit_record['student_ID'] == student_id].copy()
    temp_record['time'] = pd.to_datetime(temp_record['time'], unit='s')
    temp_record['hour'] = temp_record['time'].dt.hour # 0-23
    temp_record['time'] = temp_record['time'].dt.date

    # temp_record['time_date'] = temp_record['submit_time'].dt.strftime("%Y-%m-%d")
    learn_time_day = temp_record.groupby(['time']).agg({'hour': lambda x: x.unique().size})
    # print('learn_time_day:',learn_time_day[50:60].to_csv())
    csv_format = learn_time_day.to_csv()
    # print('csv_format:',csv_format)
    # for line in csv_format.split('\n'):
    #     print(line[0],line[1],type(line[0]))
    #     break
    res_data = []
    # 将csv_format单行保存为list, push到res_data中
    for line in csv_format.split('\r\n')[1:]: # 第一行是time,hour
        if line == '':
            break
        res_data.append(line.split(','))
    print('res_data:',res_data)
    
    # res = {"status":0, "res_data":temp_record.to_dict()}
    # ctx.write(res)
# test_resHeatMapData(submit_record, 'zhx5rxgopln1p5hd10ql')

def register(app: pywss.App):
    # app.get("/knowledge_lr", resKnowledgeSunburstData)
    app.get("/answer_state", resAnswerStateData)
    app.get("/student_activity", resHeatMapData)