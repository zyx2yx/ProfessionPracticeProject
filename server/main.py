import pywss

from module import API_StudentInfo
from module import API_task1
from module import API_task2
from module import API_task3
from module import API_task4

def cors(ctx: pywss.Context):
    if ctx.method == pywss.MethodOptions:
        ctx.set_header("Access-Control-Allow-Origin", "*")
        ctx.set_header("Access-Control-Expose-Headers", "*")
        ctx.set_header("Access-Control-Allow-Credentials", "true")
        ctx.set_header("Access-Control-Allow-Methods", "GET,POST,PUT,OPTIONS")
        return
    ctx.next()

def helloHandler(ctx: pywss.Context): # 处理函数仅 pywss.Context 一个参数哦~
    ctx.write({"hello": "world"})

def main():
    app = pywss.App()
    app.use(pywss.NewCORSHandler())  # 使用全局中间件设置跨域
    app.options("*", lambda ctx: None)  # 注册options路由

    app.get("/hi", lambda ctx: ctx.write("hi~"))  # 匿名函数也是不错的选择~
    app.post("/hello", helloHandler)
    API_StudentInfo.register(app)
    API_task1.register(app)
    API_task2.register(app)
    API_task3.register(app)
    API_task4.register(app)
    
    app.run(port=8080)  # 默认端口为8080

if __name__ == '__main__':
    """
    python3 main.py 启动服务
    """
    main()