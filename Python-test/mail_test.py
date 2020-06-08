# smtplib 用于邮件的发信动作
import smtplib
from email.mime.text import MIMEText
# email 用于构建邮件内容
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
# 用于构建邮件头
import cgitb

cgitb.enable(format='text')

# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = 'zonghui.jin@estra-automotive.com'
password = 'abc=202003'

# 收信方邮箱
to_addr = 'zonghui.jin@estra-automotive.com'

# 发信服务器
smtp_server = 'smtp.office365.com'

# 构造邮件
msg = MIMEMultipart()

# 邮件头信息
msg['From'] = Header(from_addr)
msg['To'] = Header(to_addr)
msg['Subject'] = Header('python test')

# 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
main_content = '这是Python 邮件发送测试中的正文内容…'
msg.attach(MIMEText(main_content, 'plain', 'utf-8'))


# 附件
# path = r'G:\_HAVC_Project\EX11\EX11_01_vent'
# part = MIMEApplication(open('%s/EX11_V1_vent.csv' % path, 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="EX11_V1_vent.csv")
# msg.attach(part)
#
# part = MIMEApplication(open('%s/EX11-V1_vent-mesh-TUI.jou' % path, 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="EX11-V1_vent-mesh-TUI.jou")
# msg.attach(part)
#
# part = MIMEApplication(open('%s/project_info.py' % path, 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="project_info.py")
# msg.attach(part)
#
# part = MIMEApplication(open(r'G:\_HAVC_Project\EX11/EX11_input_coefficient_20200603.html', 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="EX11_input_coefficient_20200603.html")
# msg.attach(part)
#
# part = MIMEApplication(open(r'G:\_HAVC_Project\D2U-2\D2U-2_vent\D2U-2_vent_V18\D2U-2_V18_vent_transcript', 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="D2U-2_V18_vent_transcript")
# msg.attach(part)
#
# part = MIMEApplication(open(r'G:\_HAVC_Project\D2U-2\D2U-2_vent\D2U-2_vent_V18\result_D2U-2_V18_vent\evap_out.jpg', 'rb').read())
# part.add_header('Content-Disposition', 'attachment', filename="evap_out.jpg")
# msg.attach(part)

# 开启发信服务，这里使用的是加密传输
print('here')
server = smtplib.SMTP(host=smtp_server)
server.set_debuglevel(1)
# server.connect(smtp_server, 465)
server.ehlo()
server.starttls()
print('there')
# 登录发信邮箱
server.login(from_addr, password)
# 发送邮件
server.sendmail(from_addr, to_addr, msg.as_string())
# 关闭服务器
server.quit()

