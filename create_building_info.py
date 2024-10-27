from lxml import etree
import requests



url = 'http://10.100.1.24:8988/web/Common/Tsm.html'
header = {
    'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36 Edg/130.0.0.0',
    # 'Referer':'http://10.100.1.24:8988/web/common/checkEle.html?ticket=C29361EF2A394D0B8377FB50F69D9A64&from=ehall&cometype=&timestamp=20241027223134156',
    # 'Cookies':'JSESSIONID=73AFE63E02355A7EF076D7EA0190AA6C',
    'Host':'10.100.1.24:8988',
    'X-Requested-With':'XMLHttpRequest',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive'
}

# params = {'query_elec_roominfo':{'ticket':'C29361EF2A394D0B8377FB50F69D9A64','from':'ehall','timestamp':'20241027183342827'}}
# data = {"query_elec_roominfo":{"aid":"0030000000002505",
#                                "account":"823767",
#                                "room":{"roomid":"a325","room":"a325"},
#                                "floor":{"floorid":"","floor":""},
#                                "area":{"area":"青岛校区","areaname":"青岛校区"},
#                                "building":{"buildingid":"1503975890","building":"凤凰居2号楼"}},
#         'funname':'synjones.onecard.query.elec.building',
#         'json':'true'}
info3 = {"area":"青岛校区","areaname":"青岛校区"}
info2 = {"aid":"0030000000002505","account":"823767","area":'%s' % info3}
info1 = {"query_elec_roominfo":'%s' % info2}
data = {'jsondata':'%s' % info1,'funname':'synjones.onecard.query.elec.building','json':'true'}
response = requests.post(url=url, data=data, headers=header)
print(response)
html = response.text
print(html)

tree = etree.HTML(html)
with open('building_info.csv','a') as f:
    for i in range(1, 28):
        building_data = tree.xpath(f'//*[@id="buildingul"]/li[{i}]/@onclick()')[0]
        f.write(building_data)