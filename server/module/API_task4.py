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
student_num = submit_record['student_ID'].nunique()
# print('student_num:', student_num)

title_info = pd.read_csv(relative_path + 'Data_TitleInfo.csv')
full_score_sub_kg = title_info.groupby('sub_knowledge')['score'].sum()

exampledata = {
  'knowledgePoint': 'ROOT',
  'children': [{
    "knowledgePoint": "主知识点",
    "children": [
      {
        "knowledgePoint": "一级知识点1",
        "children": [
          { "question": "题目1", "submissions": 150, "score": 0.8 },
          { "question": "题目2", "submissions": 100, "score": 0.6 }
        ]
      },
      {
        "knowledgePoint": "一级知识点2",
        "children": [
          { "question": "题目3", "submissions": 120, "score": 0.75 }
        ]
      }
    ]
  }
    , {
    "knowledgePoint": "主知识点",
    "children": [
      {
        "knowledgePoint": "一级知识点1",
        "children": [
          { "question": "题目1", "submissions": 150, "score": 0.8 },
          { "question": "题目2", "submissions": 100, "score": 0.6 }
        ]
      },
      {
        "knowledgePoint": "一级知识点2",
        "children": [
          { "question": "题目3", "submissions": 120, "score": 0.75 },
          { "question": "题目4", "submissions": 120, "score": 0.75 },
        ]
      }
    ]
  }]
}

def kgisinList(list, kg):
    for i in range(0, len(list)):
        if list[i]["knowledgePoint"] == kg:
            return i
    return -1

def readSubmitRecord():
    submit_record = pd.read_csv(relative_path + 'All_Class/all_class_submit_record.csv')
    submit_record = submit_record.drop_duplicates(subset=['student_ID','time']) # 去除数据处理时增加的重复数据
    submit_record['time'] = pd.to_datetime(submit_record['time'], unit='s')
    # submit_record['hour'] = submit_record['date'].dt.hour # 0-23
    # submit_record['day'] = submit_record['date'].dt.day # 1-31
    # submit_record['month'] = submit_record['date'].dt.month # 1-12
    return submit_record

# 计算平均得分率(task2) 还是 计算 得分总分/总分(task1)，它们使用在了之前的两个任务中，现在需要考虑使用哪一个值更能体现学生的知识掌握水平
def resProblemViewData(ctx: pywss.Context):
  submit_record = readSubmitRecord()
  student_list_part = ctx.json()['student_list']
  student_cluster = ctx.json()['student_cluster']
  student_class = ctx.json()['student_class']

  student_list = []
  if student_cluster > -1:
    student_list = API_task2.features[API_task2.features['kmeans_cluster'] == student_cluster].index.tolist()
  elif student_class:
    student_list = API_StudentInfo.student_info[API_student_info.student_info['class'] == student_class].index.tolist()
  else:
    student_list = student_list_part

  problemview_data = {'knowledgePoint': 'ROOT','children': []}
  student_num = len(student_list)
  if student_num != 0:
    submit_record = submit_record[submit_record['student_ID'].isin(student_list)]

  # 对submit_record按title_ID分组统计各组提交记录总数，然后除以学生总数得到每道题目的平均提交次数
  submit_record_grouped = submit_record.groupby('title_ID').agg({'student_ID':'count'}).reset_index()
  submit_record_grouped['student_ID'] = submit_record_grouped['student_ID'] / student_num
  # 保留每个学生每道题目最高得分记录
  submit_record_temp = submit_record.sort_values(by=['student_ID', 'title_ID', 'score'], ascending=[True, True, False])
  submit_record_temp = submit_record_temp.drop_duplicates(subset=['student_ID', 'title_ID'], keep='first')
  submit_record_temp['correct_rate'] = submit_record_temp['score'] / submit_record_temp['full_score'] # 将得分率作为正确率
  # 对submit_record按照title_ID分组统计每组正确率之和，然后除以学生总数得到每道题目的平均正确率
  submit_record_title_r = submit_record_temp.groupby('title_ID').agg({'correct_rate':'sum'}).reset_index()
  submit_record_title_r['correct_rate'] = submit_record_title_r['correct_rate'] / student_num

  submit_record_grouped = submit_record_grouped.merge(submit_record_title_r, on='title_ID', how='left')
  # 为submit_record_grouped添加sub_knowledge字段，通过title_info中的sub_knowledge字段实现
  submit_record_grouped = submit_record_grouped.merge(title_info[['title_ID', 'sub_knowledge']], on='title_ID', how='left')
  # print(submit_record_grouped)

  # 为submit_record_grouped的列索引重命名
  submit_record_grouped.columns = ['question', 'submissions', 'score', 'sub_knowledge']
  # 遍历submit_record_grouped每一行，每行对应一个题目，分别包含'question', 'submissions', 'score', 'sub_knowledge'
  for index, row in submit_record_grouped.iterrows():
      # print(index, row) # 0 question          0001,...
      # 获取sub_knowledge字段的值
      skg_name = row['sub_knowledge']
      kg = skg_name.split('_')[0]
      skg = skg_name.split('_')[1]
      
      first_idx = kgisinList(problemview_data['children'], kg)
      if first_idx == -1:
        problemview_data['children'].append({"knowledgePoint":kg, "children": []})
        first_idx = len(problemview_data['children']) - 1
      second_idx = kgisinList(problemview_data['children'][first_idx]['children'], skg)
      if second_idx == -1:
        problemview_data['children'][first_idx]['children'].append({"knowledgePoint":skg, "children": []})
        second_idx = len(problemview_data['children'][first_idx]['children']) - 1
      problemview_data['children'][first_idx]['children'][second_idx]['children'].append({"question":row['question'], "submissions":row['submissions'], "score":row['score']})
  # print('problemview_data',problemview_data)
      
  # res = {"status":0, "res_data":{ "name": "knowledge", "children": sunburst_data }}
  res = {"status":0, "res_data":problemview_data}
  ctx.write(res)
    
# resProblemViewData('')

def register(app: pywss.App):
    # 返回学生每周答题情况
    app.post("/problemview", resProblemViewData)


