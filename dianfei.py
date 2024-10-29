import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import csv
import urllib
import requests



def get_num():
    url = 'http://10.100.1.24:8988/web/Common/Tsm.html'
    header = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0',
        'Host':'10.100.1.24:8988',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive'
    }
    account = input('请输入账号：')
    building_name = urllib.parse.quote(input('请输入楼名：'))
    building_id = input('请输入楼号：')
    room_id = input('请输入房间号：')
    data = 'jsondata=%7B+%22query_elec_roominfo%22%3A+%7B+%22aid%22%3A%220030000000002505%22%2C+%22account%22%3A+%22'+account+'%22%2C%22room%22%3A+%7B+%22roomid%22%3A+%22'+room_id+'%22%2C+%22room%22%3A+%22'+room_id+'%22+%7D%2C++%22floor%22%3A+%7B+%22floorid%22%3A+%22%22%2C+%22floor%22%3A+%22%22+%7D%2C+%22area%22%3A+%7B+%22area%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22%2C+%22areaname%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22+%7D%2C+%22building%22%3A+%7B+%22buildingid%22%3A+%22'+building_id+'%22%2C+%22building%22%3A+%22'+building_name+'%22+%7D+%7D+%7D&funname=synjones.onecard.query.elec.roominfo&json=true'
    response = requests.post(url=url, data=data, headers=header)
    base_data = response.json()
    data = base_data["query_elec_roominfo"]["errmsg"]
    num = data[8:]
    if not num:
        num = "无法获取房间信息"
    return num


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
            server.quit()
        print("邮件发送成功")
    except Exception as e:
        print(f"邮件发送失败: {e}")


def judge():
    i = float(get_num())
    with open('log.csv','w',newline='',encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow([i,time.ctime()])
    if i <= 10:
        send_email()


if __name__ == '__main__':

    judge()

    schedule.every().hour.at(":00").do(judge())
    while True:
        schedule.run_pending()
        time.sleep(1)

