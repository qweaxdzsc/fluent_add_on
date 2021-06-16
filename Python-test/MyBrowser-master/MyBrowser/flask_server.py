from flask import Flask
from requests_html import HTMLSession
app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False


@app.route('/')
def get_content():
    # 获取请求对象
    session = HTMLSession()

    # 往新浪新闻主页发送get请求
    result = session.get('http://www.elecfans.com/d/1528701.html')
    # print(sina.status_code)
    result.encoding = 'utf-8'

    # 获取响应文本信息，与requests无区别
    # print(sina.text)
    result.html.render(scrolldown=4, sleep=2)
    return result.text


if __name__ == '__main__':
    print('test web:  http://localhost:8181')
    app.run(debug=True, host='0.0.0.0', port='8181')


