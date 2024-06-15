import pywss
import pandas as pd
import numpy as np
import os

# relative_path = "../../sourcedata/"
# 获取当前文件路径
curPath = os.path.abspath(os.path.dirname(__file__))
# print(curPath)
# curpath向上2级路径即为rootpath
rootPath = '/'.join(curPath.split(os.path.sep)[:-2])
# print('rootPath:',rootPath)
# 与relative_path拼接
relative_path = rootPath + '/sourcedata/'

# dataprocess function
def addClassInfo2StudentList():
    
    student_info = pd.read_csv(relative_path + 'All_Class/all_class_submit_record.csv')
    # 对student_infoan按照student_ID去重
    student_info = student_info.drop_duplicates(subset=['student_ID'])
    # 只保留class，student_ID，sex，age，major 5列
    student_info = student_info.loc[:, ['class', 'student_ID','sex','age','major']]

    return student_info
# test
# stu = addClassInfo2StudentList()
# print(stu[stu['class'] == 'Class2'].to_dict(orient='records')[:2])
# print(stu[stu['class'] == 'Class2'].to_json(orient='records')[:100]) # json格式字符串

# handle function
student_info = addClassInfo2StudentList()


# response function
def resStudentInfo(ctx: pywss.Context):
    print(ctx.url_params)
    classid_list = ctx.url_params["classid_list[]"]
    # 如果classid_list不是list类型，则转换为list
    if not isinstance(classid_list, list):
        classid_list = [classid_list]
    res = {"status" : -1, "classid_list":classid_list, "res_data":[], "error_msg": "empty classid_list!"}
    for classid in classid_list:
        print(classid)
        if classid == "AllClass":
            res_student_info = student_info.to_dict(orient='records')
            res['status'] = 0
            res['res_data'].append(res_student_info)
            # res = {"status" : 0, "res_data" : res_student_info}
        elif classid in student_info['class'].values:
            # res_student_info = student_info[student_info['class'] == classid].to_json(orient='records')
            res_student_info = student_info[student_info['class'] == classid].to_dict(orient='records')
            # res_student_info = student_info[student_info['class'] == classid].to_dict(orient='records')[:3]
            # res = {"status" : 0, "res_data" : res_student_info}
            res['status'] = 0
            res['res_data'].append(res_student_info)
        else:
            # res = {"status" : -1, "error_msg": "classid not found!"}
            res['status'] = -1
            res['error_msg'] = "classid not found!"
    ctx.write(res)

def resStuFuzzySearch(ctx: pywss.Context):
    print(ctx.url_params)
    keyword = ctx.url_params["keyword"]
    classid = ctx.url_params["classid"]
    searchcolumn = ctx.url_params["searchcolumn"]
    res = {"status" : -1, "keyword":keyword, "res_data":[], "error_msg": "empty keyword!"}

    if keyword == "":
        ctx.write(res)
        return
    keyword = keyword.lower()
    res_student_info = student_info[student_info['class'] == classid][student_info[searchcolumn].str.lower().str.contains(keyword)]
    if res_student_info.empty:
        res['status'] = -1
        res['error_msg'] = "keyword not found!"
    else:
        res['status'] = 0
        res['res_data'] = res_student_info.to_dict(orient='records')
    ctx.write(res)
    
def getStudentSimpleFeatures(start_time, end_time):
    submit_record = pd.read_csv(relative_path + 'All_Class/all_class_submit_record.csv')
    submit_record = submit_record.drop_duplicates(subset=['student_ID','time']) # 去除数据处理时增加的重复数据
    
    submit_record['time'] = pd.to_datetime(submit_record['time'], unit='s')
    submit_record['hour'] = submit_record['time'].dt.hour # 0-23
    submit_record['day'] = submit_record['time'].dt.day # 1-31
    submit_record['month'] = submit_record['time'].dt.month # 1-12

    # submit_record['attempts_all'] = submit_record.groupby(['student_ID'])['index'].transform('count') # 
    # submit_record['attempts_avg'] = submit_record['attempts_all'] / 
    
    submit_record['is_correct'] = submit_record['state'].apply(lambda x: 1 if x == 'Absolutely_Correct' else 0)

    # 计算特征
    features = submit_record.groupby('student_ID').agg({
        # 'score': ['mean', 'sum', 'count'],
        # 'score': 'sum',
        'index': 'count', # 尝试次数
        'is_correct': 'mean', # 计算每个学生每次提交的平均正确率, 即正确次数数/尝试次数
        'class':"first", # 班级
        'hour': lambda x: x.value_counts().idxmax(), # 最常答题的时间段 匿名函数作用是返回出现次数最多的值 .value_counts()统计每个值出现的次数 .idxmax()返回出现次数最多的值
        'method': lambda x: x.value_counts().idxmax(), # 最常用的方法
        'title_ID': 'nunique', # 尝试的题目数量
        'state': lambda x: x.value_counts().idxmax(), # 最常出现的答题状态

    })
    features.columns = [
        "attempts_all",
        "avg_correct_rate",
        "class",
        "most_common_hour",
        "most_common_method",
        "attempts_questions_num",
        "most_common_state",
    ]
    features["attempts_avg"] = features["attempts_all"] / features["attempts_questions_num"]
    # print(features.iloc[:10,:])
    # 学生的活跃天数，需要注意答题记录中包含5个月的数据
    temple_submit_record = submit_record.drop_duplicates(subset=['student_ID', 'month','day'], keep='first')
    # 两次groupby后的结果能否与上面的结果合并？可以，因为groupby方法sort参数默认为True，即默认对结果进行排序
    # print(temple_submit_record.groupby('student_ID')['day'].count()[:10])
    features['active_days'] = temple_submit_record.groupby('student_ID')['day'].count()
    # print(features['active_days'][:100])
    # 每个学生的答题时长 可能与题目尝试次数相关
    temple_submit_record = submit_record.drop_duplicates(subset=['student_ID', 'month','day','hour'], keep='first')
    features['learn_hours'] = temple_submit_record.groupby('student_ID')['hour'].count()

    # 每道题目最终得分率
    submit_record = submit_record.sort_values(by=['student_ID', 'title_ID', 'score'], ascending=[True, True, False])
    submit_record = submit_record.drop_duplicates(subset=['student_ID', 'title_ID'], keep='first')
    submit_record['score_ratio'] = submit_record['score'] / submit_record['full_score']
    # 每个学生平均得分率
    features['avg_score_ratio'] = submit_record.groupby(['student_ID'])['score_ratio'].mean()
    # 计算学生总的得分
    features['total_score'] = submit_record.groupby('student_ID')['score'].sum()
    features = features[['total_score','learn_hours','active_days','avg_score_ratio','avg_correct_rate',
                         'attempts_avg','most_common_hour','most_common_state',
                         'most_common_method','attempts_questions_num','attempts_all','class']]

    return features

# f = getStudentSimpleFeatures("","")
# print(f[f['class'] == 'Class1']['most_common_state'].value_counts())

def resParallelDataOfStudentOrClass(ctx: pywss.Context):
    print(ctx.json())
    student_ids, class_ids, start_time, end_time = ctx.json().values()
    # print(student_ids, class_ids, start_time, end_time)
    if not student_ids and not class_ids:
        ctx.write({"status" : -1, "student_ids":student_ids, "class_ids":class_ids, "res_data":{}, "error_msg": "empty student_ids or class_ids!"})
        return

    res = {"status" : 0, "student_ids":student_ids, "class_ids":class_ids, "res_data":{}, "merge_list":student_id + class_ids,"res_list_data":[],"error_msg": "empty student_ids or class_ids!"}
    features = getStudentSimpleFeatures(start_time, end_time) # dataframe

    # 对每一个student_id, 取出该行数据，转化为list, 作为res.res_data.id的value
    for student_id in student_ids:
        res['res_data'][student_id] = features.loc[student_id].drop(['attempts_questions_num','attempts_all','class'],axis=1).to_list()
        res['res_list_data'].append(res['res_data'][student_id])
    # 按照class进行分组，每一组：除most_common_method，most_common_state按组取频次最高的值外，其余列全部按组取求均值
    features_class = features.groupby('class').agg({
        "total_score": 'mean',
        "learn_hours": 'mean',
        "active_days": 'mean',
        "avg_score_ratio": 'mean',
        "avg_correct_rate": 'mean',
        "attempts_avg": 'mean',
        "most_common_hour": lambda x: x.value_counts().idxmax(),
        "most_common_state": lambda x: x.value_counts().idxmax(),
        "most_common_method": lambda x: x.value_counts().idxmax(),
        # "attempts_questions_num": 'mean', # 次要特征
        # "attempts_all": 'mean', # 次要特征
    })
    # print('features_class:',features_class)
    for class_id in class_ids:
        res['res_data'][class_id] = features_class.loc[class_id].to_list()
        res['res_list_data'].append(res['res_data'][class_id])
    
    ctx.write(res)

def register(app: pywss.App):
    app.get("/studentinfo", resStudentInfo)
    app.get("/studentinfo/fuzzysearch", resStuFuzzySearch)
    app.post("/studentinfo/paralleldata", resParallelDataOfStudentOrClass)
    