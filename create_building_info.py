import json
import requests
import urllib
import csv


if '__main__' == __name__:
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
    a = {
        "jsondata":{ "query_elec_building": { "aid": "0030000000002505", "account": "823767", "area": {"area": "青岛校区", "areaname": "青岛校区"  } } },
        "funname":"synjones.onecard.query.elec.building",
        "json":"true"
    }
    b = json.dumps(a)
    data = urllib.parse.quote(b)
    response = requests.post(url=url, data=data, headers=header)
    base_data = response.json()
    with open('building_info.csv','w',newline='') as f:
        writer = csv.writer(f)
        for i in range(0,27):
            data = base_data["query_elec_building"]["buildingtab"][i]
            building = data["building"]
            buildingid = data["buildingid"]
            writer.writerow([building,buildingid])




