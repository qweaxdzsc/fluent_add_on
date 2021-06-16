from requests_html import HTMLSession
import cgitb
cgitb.enable(format='text')

session = HTMLSession()

url = 'http://www.baidu.com/'

obj = session.get(url)

obj.encoding = 'utf-8'

obj.html.render()
print(obj.text)

