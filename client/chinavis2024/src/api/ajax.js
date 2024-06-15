// 封装axios函数，便于外部调用
import axios from 'axios'
// import {message} from 'antd'

/* 
    传入请求地址，请求数据，请求方法

    优化：
    1.统一处理失败请求
    2.请求成功，将响应的数据response.data传递下去，而不是传递response，外部就可以直接获取
    响应数据，不用再读取一次
*/
axios.defaults.baseURL = 'http://localhost:8080';
export default function ajax (url, data={}, method='GET'){
    return new Promise((resolve, reject) => {
        let promise
        // 发送请求
        if(method === 'GET'){
            promise = axios.get(url, { params: data })
        } else {
            promise = axios.post(url, data)
        }

        // 请求成功，就把请求成功的数据体data响应传递下去
        promise.then(response => {
            resolve(response.data)
        })
        // 请求失败 捕获失败的Promise
        .catch(error => {
            // message.error(error.message)
            console.log('请求失败', error)
        })
        
    })
}