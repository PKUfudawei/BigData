def isPrime(N):
    if N <= 1:
        return False
    if N == 2:
        return True
    for i in range(2, N):
        if N % i == 0:
            return False
    return True


from flask import Flask  # 新增代码。装入Flask.第三方轻量级Web框架

app = Flask(__name__)  # 新增代码


@app.route("/")  # 新增代码，对应执行root()函数
def root():
    content = ""
    for i in range(200, 300):
        if isPrime(i) == True:
            content += str(i) + " "

    return "200-300的质数：" + content


@app.route("/400_500")  # 新增代码，对应执行root()函数
def XYZ():
    content = ""
    for i in range(400, 500):
        if isPrime(i) == True:
            content += str(i) + " "
    html = f"400-500的质数：<strong>{content}</strong><br>"
    html += "<a href='http://www.pku.edu.cn'>北京大学</a>"
    html += "<img src='/static/dxt.png'>"
    return html


if __name__ == "__main__":  # 新增代码
    app.run(debug=False, port=5050)

# eof
