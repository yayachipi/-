import smtplib
from email.mime.text import MIMEText
from email.header import Header

def main():
    mail_host = "smtp.163.com"  # SMTP服务器
    mail_user = "***@163.com"  # 用户名
    mail_pass = "***"  # 密码
 
    sender = '***@163.com'  # 发件人邮箱(最好写全, 不然会失败)
    receivers = ['****@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
 
 
    content = '有票啦!'
    title = 'Python 帮你拿到票了'  # 邮件主题
    message = MIMEText(content, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = title
 
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("mail has been send successfully.")
    except smtplib.SMTPException as e:
        print(e)

if __name__ == '__main__':
    main()
