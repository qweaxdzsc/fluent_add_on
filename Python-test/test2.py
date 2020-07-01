import win32com.client
outlook = win32com.client.Dispatch("Outlook.Application")

# 创建一个邮件对象
mail = outlook.CreateItem(0)
# 对邮件的各个属性进行赋值
mail.To = "zonghui.jin@estra-automotive.com"
mail.Subject = "pythonwin32测试邮件"
mail.Body = "邮件正文"
# mail.Attachments.Add(r"C:\Users\BZMBN4\Desktop\host_mesh.txt")
# 添加多个附件
# mail.Attachments.Add("附件1绝对路径")
# mail.Attachments.Add("附件2绝对路径")...
# 邮件发送
mail.Send()
