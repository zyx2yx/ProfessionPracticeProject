import pywss

from module import API_StudentInfo



def helloHandler(ctx: pywss.Context): # 处理函数仅 pywss.Context 一个参数哦~
    ctx.write({"hello": "world"})

def main():
    app = pywss.App()
    app.use(pywss.NewCORSHandler())  # 使用全局中间件设置跨域

    app.get("/hi", lambda ctx: ctx.write("hi~"))  # 匿名函数也是不错的选择~
    app.post("/hello", helloHandler)
    API_StudentInfo.register(app)
    
    app.run(port=8080)  # 默认端口为8080

if __name__ == '__main__':
    """
    python3 main.py 启动服务
    """
    main()