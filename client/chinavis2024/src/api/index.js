/* 
    包装接口，便于外部调用
*/

import ajax from './ajax'

// // 登录请求
// export const reqLogin = (username, password) => ajax('/manage/user/login', {username, password}, 'POST')
// // 用户注册
// export const reqRegister = (username, password) => ajax('/manage/user/register', {username, password}, 'POST')
// // 修改密码
// export const reqUpdatePwd = accountInfo => ajax('/manage/user/update', accountInfo, 'POST')
// // 文件删除请求
// export const reqDeleteFile = (doc_id) => ajax('/manage/docs/delete', {doc_id}, 'POST')
// // 文档预发布请求
// export const reqPrepareRelease = updateOptions => ajax('/manage/docs/release/basic', updateOptions, 'POST')
// // 文档中间发布请求
// export const reqMidRelease = signArea => ajax('/manage/docs/release/sign-area', signArea, 'POST')
// // 文档最终发布请求
// export const reqRelease = releaseOptions => ajax('/manage/docs/release/confirm', releaseOptions, 'POST')
// // 获取文档列表
// export const reqDocList = (doc_status, time_type, creator_id) => ajax('/manage/docs/list', {doc_status, time_type, creator_id})
// // 结束签署
// export const reqEndSign = endOptions => ajax('/manage/docs/sign-end', endOptions, 'POST')
// // 签署用户登记接口
// export const reqGetUid = () => ajax('/manage/user/get-uid')
// // 获取单个签署文件信息
// export const reqDocInfo = (doc_id) => ajax('/manage/docs/info', {doc_id})
// // 记录用户开始签署
// export const reqStartSign = (doc_id, uid) => ajax('/manage/sign/start-sign', {doc_id, uid}, 'POST')
// // 用户提交签名
// export const reqCommitSign = (doc_id, uid, imgBase64) => ajax('/manage/sign/commit',{doc_id, uid, imgBase64}, 'POST')
// // 下载签署好的文件 此API不会被使用
// export const reqDownload = doc_id => ajax('/manage/docs/download', {doc_id})
// // 补签接口
// export const reqRepeatSign = doc_id => ajax('/manage/docs/repeat-sign', {doc_id}, 'POST')

// 根据班级id获取班级学生列表
export const reqGetClassStudentList = classid_list => ajax('/studentinfo', {classid_list})
// 在当前选中的班级中实现模糊查询
export const reqStuFuzzySearch = (classid, searchcolumn, keyword) => ajax('/studentinfo/fuzzysearch', {classid, searchcolumn, keyword})
// 根据学生id列表、班级id列表、起止时间获取学生答题特征信息，POST请求
export const reqParallelDataOfStudentOrClass = (student_ids, class_ids, start_time, end_time) => ajax('/studentinfo/paralleldata', {student_ids, class_ids, start_time, end_time},'POST')
// export const reqParallelDataOfStudentOrClass = (studentid_ids, classid_ids, start_time, end_time) => ajax('/hello', {studentid_ids, classid_ids, start_time, end_time},'POST')
// export const reqParallelDataOfStudentOrClass = (studentid_ids, classid_ids, start_time, end_time) => ajax('/studentinfo/paralleldata', {studentid_ids, classid_ids, start_time, end_time})
// 获取旭日图数据
export const reqSunburstData = (student_id) => ajax('/knowledge_lr', {student_id})
// 获取学生某知识点答题状态信息
export const reqAnswerStatus = (student_id, kg) => ajax('/answer_state', {student_id, kg})
// 获取某学生活跃度信息
export const reqActivity = (student_id) => ajax('/student_activity', {student_id})
// 获取学生群体聚类结果
export const reqCluster = () => ajax('/student_clusters')
// 获取学生聚类特征tsne降维坐标
export const reqTsnePos = () => ajax('/tsne_dr')
// 获取学生群体在每一天的活跃度（提交次数）总和
export const reqActivitySum = () => ajax('/day_activity_river')
// 获取学生群体每个题目的尝试次数与正确率
export const reqAttemptAndCorrect = () => ajax('/attempts_correct')
