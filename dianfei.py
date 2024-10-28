import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import pandas as pd
import json
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
    # a = {
    #     "jsondata":{ "query_elec_building": { "aid": "0030000000002505", "account": "823767", "area": {"area": "青岛校区", "areaname": "青岛校区"  } } },
    #     "funname":"synjones.onecard.query.elec.building",
    #     "json":"true"
    # }                                                        换指定房间的，指定账号的
    b = json.dumps(a)
    data = urllib.parse.quote(b)
    response = requests.post(url=url, data=data, headers=header)
    base_data = response.json()
    data = base_data["query_elec_roominfo"]["errmsg"]
    num = data[8:]
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


if __name__ == '__main__':
    judge()

    schedule.every().hour.at(":00").do(judge())
    while True:
        schedule.run_pending()
        time.sleep(1)

