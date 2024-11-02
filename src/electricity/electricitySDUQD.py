import schedule
import time

import csv
import json
import urllib
import requests

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from win11toast import toast
import os
from twilio.rest import Client


def send_mail():
    with open('electricity_initialize.json','r', encoding='utf-8') as file:
        a = json.load(file)
    try:
        print('请输入接收端邮箱（用,隔开）：')
        for i in range(0,30):
            time.sleep(1)
        print('继续进行邮件发送')
    except KeyboardInterrupt:
        ans = input()
        a["way"]["your_mails"] = ans.split(',')
        with open("electricity_initialize.json", "w", encoding='utf-8') as file:
            json.dump(a, file, ensure_ascii=False, indent=4)
    finally:
        emails = a["way"]["your_mails"]

    for email in emails:
        msg = MIMEText('【电费小贴士】您的电费余额已不足20元，请及时充值', 'plain', 'utf-8')
        msg['From'] = Header("3987865140@qq.com")
        msg['To'] = Header(email)
        msg['Subject'] = Header('电费小贴士', 'utf-8')
        try:
            with smtplib.SMTP('smtp.qq.com', 25) as server:
                server.starttls()
                server.login("3987865140@qq.com", 'aggafalqejktcdbc')
                server.sendmail("3987865140@qq.com", email, msg.as_string())
                server.quit()
        except Exception as e:
            print(f"邮件发送失败: {e}")
    print("邮件发送成功")


def send_windows():
    adjust = os.path.abspath('.').replace("\\","/")
    path = 'file:///' + adjust + '/tool/interrupt.pyw'
    toast('【电费小贴士】', '您的电费余额已不足20元，请及时充值', button={'activationType': 'protocol', 'arguments': path, 'content': 'Stop reminding'}, scenario='incomingCall')


def send_duanxin():
    with open('electricity_initialize.json','r', encoding='utf-8') as file:
        b = json.load(file)
    try:
        print('请输入接收端电话（用,隔开）：')
        for i in range(0,30):
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



def get_num():
    url = 'http://10.100.1.24:8988/web/Common/Tsm.html'
    header = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0',
        'Host':'10.100.1.24:8988',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive'
    }
    with open('electricity_initialize.json','r', encoding='UTF-8') as f:
        inited = json.load(f)
        account = inited["info"]["account"]
        building_name = inited["info"]["building_name"]
        building_id = inited["info"]["building_id"]
        room_id = inited["info"]["room_id"]
    data = 'jsondata=%7B+%22query_elec_roominfo%22%3A+%7B+%22aid%22%3A%220030000000002505%22%2C+%22account%22%3A+%22'+account+'%22%2C%22room%22%3A+%7B+%22roomid%22%3A+%22'+room_id+'%22%2C+%22room%22%3A+%22'+room_id+'%22+%7D%2C++%22floor%22%3A+%7B+%22floorid%22%3A+%22%22%2C+%22floor%22%3A+%22%22+%7D%2C+%22area%22%3A+%7B+%22area%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22%2C+%22areaname%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22+%7D%2C+%22building%22%3A+%7B+%22buildingid%22%3A+%22'+building_id+'%22%2C+%22building%22%3A+%22'+building_name+'%22+%7D+%7D+%7D&funname=synjones.onecard.query.elec.roominfo&json=true'
    response = requests.post(url=url, data=data, headers=header)
    base_data = response.json()
    data = base_data["query_elec_roominfo"]["errmsg"]
    num = data[8:]
    if not num:
        num = "无法获取房间信息"
    return num


def main():
    try:
        i = float(get_num())
    except ValueError:
        i = 0.404
    with open('log.csv','a',newline='',encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow([i,time.ctime()])
    if i <= 20 and len(cache) <= 3:
        with open('electricity_initialize.json','r', encoding='utf-8') as file:
            choice = json.load(file)["way"]
        if choice["mail"] == "1":
            send_mail()
        if choice["windows"] == "1":
            send_windows()
        if choice["duanxin"] == "1":
            send_duanxin()
        cache.append('1')
    else:
        cache.clear()


if __name__ == '__main__':

    with open('electricity_initialize.json','r', encoding='utf-8') as file:
        init = json.load(file)
    print("初始化：（请在1min内完成输入）")
    print('v卡通账号,楼名,楼号,房间号,是否停止监控：')
    try:
        for i in range(0,60):
            time.sleep(1)
        print('继续进行监控电费')
    except KeyboardInterrupt:
        ans = input()
        ans_list = ans.split(',')

        init["info"]["account"] = ans_list[0]
        init["info"]["building_name"] = urllib.parse.quote(ans_list[1])
        init["info"]["building"] = ans_list[2]
        init["info"]["room_id"] = ans_list[3]
        init["sleep"] = ans_list[4]
        with open("electricity_initialize.json", "w", encoding='utf-8') as file:
            json.dump(init, file, ensure_ascii=False, indent=4)
        print('设置成功')

    cache = []
    main()

    if init["sleep"] == '0':
        schedule.every().hour.do(main)

        while True:
            schedule.run_pending()
            time.sleep(10)

