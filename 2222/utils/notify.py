'''发送邮件'''
# from email.mime.text import MIMEText  # 组装邮件
# import smtplib  # 链接服务器发送
#
# # 1. 组装邮件内容MTMEText
# content = '''Hi,all
# 附件中是测试报告，如有问题请指出
# '''
# content2 = '''<h2>测试报告</h2>
# <p>附件中是测试报告，如有问题请指出</p>
# '''
# msg = MIMEText(content,'plain','utf-8')
# # msg = MIMEText(content2,'html','utf-8')
# # 2.邮件头，From To 邮件主题
# msg['From']='<韩志超>zhichao.han@qq.com'
# # msg['From']='zhichao.han@qq.com'
# msg['To']='ivan-me@163.com,superhin@126.com'
# msg['Subject']='接口测试报告'
# # 3.登录smtp服务器，并发送
# smtp = smtplib.SMTP('smtp.163.com')
# # smtp = smtplib.SMTP_SSL('smtp.sina.cpm')
# # smtp.logn('ivan-me@163.com','hanzhichao123')  # 一般情况下要使用授权密码
# smtp.sendmail('ivan-me@163.com,superhin@126.com',msg.as_string())
# print("邮件发送成功")
#
# # receivers =


# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import smtplib
# import os

# # 1.复合格式（多部分）
# msg = MIMEMultipart()
# # 2.邮件正文
# body = MIMEText('hi,all\n附加中是测试报告，请查收','plain','utf-8')
# msg.attach(body)
# # 3.邮件头
# msg['From'] = 'ivan-me@163.com'
# msg['To'] = 'superhin@126.com'
# msg['Subject'] = '接口测试报告'
# # 4.附件
# f = open('report.html','rb')
# att1 = MIMEText(f.read(),'base64','utf-8')
# att1['Content-Type']='application/octet-stream'
# att1['Content-Disposition']='attachment; filename=report2.html'
# f.close()
# msg.attach(att1)
# # 5.发送
# smtp = smtplib.SMTP_SSL('smtp.163.com')
# smtp.login('ivan-me@163.com','hanzhichao123')
# smtp.sendmail('ivan-me@163.com','superhin@126.com',msg.as_string())



import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class Notice(object):
    def email(self, body, subject, receivers, file_name):
        """发送邮件
        body是正文信息
        subject邮件主题
        receivers是收件人列表
        file_path是附件路径"""

        smtp_conf = os.getenv('SMTP_CONFIG')
        smtp_host, is_ssl, user, password = smtp_conf.split(',')

        msg = MIMEMultipart()
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        msg['From'] = user
        msg['To'] = ','.join(receivers)
        msg['Subject'] = subject

        file_path = os.path.join(basedir, 'reports', file_name)
        att1 = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
        att1['Content-Type'] = 'application/octet-stream'
        att1["Content-Disposition"] = f'attachment; filename={file_name}'
        msg.attach(att1)

        smtp = smtplib.SMTP_SSL(smtp_host)
        smtp.login(user, password)
        for person in receivers:
            smtp.sendmail(user, person, msg.as_string())


if __name__ == '__main__':
    Notice().email('正文', '主题', ['superhin@126.com'], 'report.html')