import os
import requests
import csv
import pandas as pd


def main():
    url = 'http://10.100.1.24:8988/web/Common/Tsm.html'
    header = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0',
        'Host':'10.100.1.24:8988',
        'X-Requested-With':'XMLHttpRequest',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Connection': 'keep-alive'
    }
    data = 'jsondata=%7B+%22query_elec_building%22%3A+%7B+%22aid%22%3A+%220030000000002505%22%2C+%22account%22%3A+%22823767%22%2C+%22area%22%3A+%7B%22area%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22%2C+%22areaname%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22++%7D+%7D+%7D&funname=synjones.onecard.query.elec.building&json=true'
    response = requests.post(url=url, data=data, headers=header)
    base_data = response.json()
    with open('building_info.csv','w',newline='',encoding='UTF-8') as f:
        writer = csv.writer(f)
        for i in range(0,27):
            data = base_data["query_elec_building"]["buildingtab"][i]
            building = data["building"]
            buildingid = data["buildingid"]
            writer.writerow([building,buildingid])
    my_csv = pd.read_csv('building_info.csv', encoding='utf-8')
    with pd.ExcelWriter('building_info.xlsx', engine='xlsxwriter') as writer2:
        my_csv.to_excel(writer2,sheet_name='Sheet1', index=False, header=False)
        worksheet = writer2.sheets['Sheet1']
        for i, col in enumerate(my_csv.columns):
            column_len = my_csv[col].astype(str).str.len().max() + 1
            worksheet.set_column(i, i, column_len)
    os.remove('building_info.csv')


if '__main__' == __name__:
    main()
    print('生成完毕，请继续')


