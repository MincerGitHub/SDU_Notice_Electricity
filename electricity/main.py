import schedule
import time

import csv
import json
import urllib
import requests

import ways_to_remind as ws



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
    i = float(get_num())
    with open('log.csv','a',newline='',encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow([i,time.ctime()])
    if i <= 20 and len(cache) <= 3:
        with open('electricity_initialize.json','r', encoding='utf-8') as file:
            choice = json.load(file)["way"]
        if choice["mail"] == "1":
            ws.send_mail()
        if choice["windows"] == "1":
            ws.send_windows()
        if choice["duanxin"] == "1":
            ws.send_duanxin()
        cache.append('1')
    else:
        cache.clear()


if __name__ == '__main__':

    with open('electricity_initialize.json','r', encoding='utf-8') as file:
        init = json.load(file)
    print("初始化：（请在1min内完成输入）")
    print('v卡通账号,楼名,楼号,房间号,是否停止监控：')
    try:
        for i in range(0,2):
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

    cache = []
    main()

    if init["sleep"] == '0':
        schedule.every().hour.do(main)

    while True:
        schedule.run_pending()
        time.sleep(10)

