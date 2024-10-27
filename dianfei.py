import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import pandas as pd


def get_num():
    return 1


def send_email():
    receiver_email = input('请输入您的邮箱')
    msg = MIMEText('您的电费不足10元，请注意充值', 'plain', 'utf-8')
    msg['From'] = Header("849380859@qq.com")
    msg['To'] = Header(receiver_email)
    msg['Subject'] = Header('电费小贴士', 'utf-8')
    try:
        with smtplib.SMTP('smtp.qq.com', 25) as server:
            server.starttls()
            server.login("849380859@qq.com", 'gpalxuxufqmhbbdi')
            server.sendmail("849380859@qq.com", receiver_email, msg.as_string())
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")


def judge():
    i = get_num()
    df = pd.read_excel('log.xlsx')
    new_row = {'Column1': f'{i}', 'Column2': time.ctime()}
    df = df.append(new_row, ignore_index=True)
    df.to_excel('example.xlsx', index=False)
    if i <= 10:
        send_email()


schedule.every().hour.at(":00").do(judge())


while True:
    schedule.run_pending()
    time.sleep(1)
