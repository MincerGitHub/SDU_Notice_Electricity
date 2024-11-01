import smtplib
from email.mime.text import MIMEText
from email.header import Header
import json
import time

from win11toast import toast

from twilio.rest import Client


def send_mail():
    with open('electricity_initialize.json','r', encoding='utf-8') as file:
        a = json.load(file)
    try:
        print('请输入接收端邮箱（用,隔开）：')
        for i in range(0,60):
            time.sleep(1)
        print('继续进行邮件发送')
    except KeyboardInterrupt:
        ans = input()
        a["way"]["your_mails"] = ans.split(',')
        with open("notice_initialize.json", "w", encoding='utf-8') as file:
            json.dump(a, file, ensure_ascii=False, indent=4)
    finally:
        emails = a["way"]["your_mails"]

    for email in emails:
        msg = MIMEText('【电费小贴士】您的电费余额已不足20元，请及时充值', 'plain', 'utf-8')
        msg['From'] = Header("849380859@qq.com")
        msg['To'] = Header(email)
        msg['Subject'] = Header('电费小贴士', 'utf-8')
        try:
            with smtplib.SMTP('smtp.qq.com', 25) as server:
                server.starttls()
                server.login("849380859@qq.com", 'gpalxuxufqmhbbdi')
                server.sendmail("849380859@qq.com", email, msg.as_string())
                server.quit()
        except Exception as e:
            print(f"邮件发送失败: {e}")
    print("邮件发送成功")


def send_windows():
    toast('【电费小贴士】', '您的电费余额已不足20元，请及时充值', button={'activationType': 'protocol', 'arguments': r'file://C:/Users/84938/OneDrive/桌面/pythonProject/electricity/tool/interrupt.py', 'content': 'Stop reminding'}, scenario='incomingCall')


def send_duanxin():
    with open('electricity_initialize.json','r', encoding='utf-8') as file:
        b = json.load(file)
    try:
        print('请输入接收端电话（用,隔开）：')
        for i in range(0,60):
            time.sleep(1)
        print('继续进行短信发送')
    except KeyboardInterrupt:
        ans = input()
        b["way"]["your_mails"] = ans.split(',')
        with open("notice_initialize.json", "w", encoding='utf-8') as file:
            json.dump(b, file, ensure_ascii=False, indent=4)
    finally:
        phones = b["way"]["your_phones"]

    account_sid = 'AC1c4150b8829a141eb96a216009429fb9'
    auth_token = 'b45d4806c9e348047f6449562480de35'
    client = Client(account_sid, auth_token)
    for phone in phones:
        true_phone = "+86"+phone
        client.messages.create(
            to=true_phone,
            from_="+18722013611",
            body=" \n【电费小贴士】您的电费余额已不足20元，请及时充值")
    print('短信发送成功')