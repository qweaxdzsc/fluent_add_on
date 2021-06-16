from flask import Flask, request
from requests_html import HTMLSession
app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False


@app.route('/')
def get_content():
    url = request.args.get('url')
    session = HTMLSession()

    # 往新浪新闻主页发送get请求
    result = session.get(url)
    # print(sina.status_code)
    result.encoding = 'utf-8'

    return result.text


if __name__ == '__main__':
    print('test web:  http://localhost:8181')
    app.run(debug=True, host='0.0.0.0', port='8181')


