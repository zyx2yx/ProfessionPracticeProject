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


def register(app: pywss.App):
    # app.get("/knowledge_lr", resKnowledgeSunburstData)
    # app.get("/answer_state", resAnswerStateData)
    # app.get("/student_activity", resHeatMapData)
    app.get("/hi", lambda ctx: ctx.write("hi~")) 