a = {
    "query_elec_roominfo": {
        "retcode": "0",
        "errmsg": "房间当前剩余电量349.40",
        "aid": "0030000000002505",
        "account": "823767",
        "meterflag": "amt",
        "bal": "",
        "price": "0",
        "pkgflag": "none",
        "area": {
            "area": "青岛校区",
            "areaname": "青岛校区"
        },
        "building": {
            "buildingid": "1503975890",
            "building": "凤凰居2号楼"
        },
        "floor": {
            "floorid": "",
            "floor": ""
        },
        "room": {
            "roomid": "a325",
            "room": "a325"
        },
        "pkgtab": []
    }
}



b = {
    "query_elec_building": {
        "retcode": "0",
        "errmsg": "请选择相应的楼栋：",
        "aid": "0030000000002505",
        "account": "823767",
        "area": {
            "area": "青岛校区",
            "areaname": "青岛校区"
        },
        "buildingtab": [
            {
                "buildingid": "1503975980",
                "building": "凤凰居6号楼"
            },
            {
                "buildingid": "1661835273",
                "building": "B5号楼"
            },
            {
                "buildingid": "1661835256",
                "building": "B2"
            },
            {
                "buildingid": "1574231830",
                "building": "T1"
            },
            {
                "buildingid": "1503975832",
                "building": "凤凰居1号楼"
            },
            {
                "buildingid": "1503975832",
                "building": "S1一多书院"
            },
            {
                "buildingid": "1599193777",
                "building": "S11"
            },
            {
                "buildingid": "1693031698",
                "building": "B9"
            },
            {
                "buildingid": "1503976004",
                "building": "凤凰居9号楼"
            },
            {
                "buildingid": "1503975890",
                "building": "凤凰居2号楼"
            },
            {
                "buildingid": "1503975967",
                "building": "S5凤凰居5号楼"
            },
            {
                "buildingid": "1503976037",
                "building": "凤凰居10号楼"
            },
            {
                "buildingid": "1503975890",
                "building": "S2从文书院"
            },
            {
                "buildingid": "1693031710",
                "building": "阅海居B10楼"
            },
            {
                "buildingid": "1693031698",
                "building": "阅海居B9楼"
            },
            {
                "buildingid": "1574231835",
                "building": "T3"
            },
            {
                "buildingid": "1503976004",
                "building": "S9凤凰居9号楼"
            },
            {
                "buildingid": "1503975988",
                "building": "S7凤凰居7号楼"
            },
            {
                "buildingid": "1503976037",
                "building": "S10凤凰居10号楼"
            },
            {
                "buildingid": "1503975995",
                "building": "S8凤凰居8号楼"
            },
            {
                "buildingid": "1599193777",
                "building": "凤凰居11/13号楼"
            },
            {
                "buildingid": "1574231833",
                "building": "专家公寓2号楼"
            },
            {
                "buildingid": "1503975902",
                "building": "凤凰居3号楼"
            },
            {
                "buildingid": "1693031710",
                "building": "B10"
            },
            {
                "buildingid": "1661835249",
                "building": "B1"
            },
            {
                "buildingid": "1503975950",
                "building": "凤凰居4号楼"
            },
            {
                "buildingid": "1503975980",
                "building": "S6凤凰居6号楼"
            }
        ]
    }
}











'''
对于请求问题！！！！！！！！

得到的：
%7B%22jsondata%22%3A%20%7B%22query_elec_building%22%3A%20%7B%22aid%22%3A%20%220030000000002505%22%2C%20%22account%22%3A%20%22823767%22%2C%20%22area%22%3A%20%7B%22area%22%3A%20%22%5Cu9752%5Cu5c9b%5Cu6821%5Cu533a%22%2C%20%22areaname%22%3A%20%22%5Cu9752%5Cu5c9b%5Cu6821%5Cu533a%22%7D%7D%7D%2C%20%22funname%22%3A%20%22synjones.onecard.query.elec.building%22%2C%20%22json%22%3A%20%22true%22%7D
%7B%22jsondata%22%3A%20%7B%22query_elec_building%22%3A%20%7B%22aid%22%3A%20%220030000000002505%22%2C%20%22account%22%3A%20%22823767%22%2C%20%22area%22%3A%20%7B%22area%22%3A%20%22%5Cu9752%5Cu5c9b%5Cu6821%5Cu533a%22%2C%20%22areaname%22%3A%20%22%5Cu9752%5Cu5c9b%5Cu6821%5Cu533a%22%7D%7D%7D%2C%20%22funname%22%3A%20%22synjones.onecard.query.elec.building%22%2C%20%22json%22%3A%20%22true%22%7D
jsondata=%7B%27query_elec_building%27%3A+%7B%27aid%27%3A+%270030000000002505%27%2C+%27account%27%3A+%27823767%27%2C+%27area%27%3A+%7B%27area%27%3A+%27%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%27%2C+%27areaname%27%3A+%27%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%27%7D%7D%7D&funname=synjones.onecard.query.elec.building&json=true
扒的应该的：
jsondata=%7B+%22query_elec_building%22%3A+%7B+%22aid%22%3A+%220030000000002505%22%2C+%22account%22%3A+%22823767%22%2C+%22area%22%3A+%7B%22area%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22%2C+%22areaname%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22++%7D+%7D+%7D&funname=synjones.onecard.query.elec.building&json=true
【对应】：
jsondata={+"query_elec_building":+{+"aid":+"0030000000002505",+"account":+"823767",+"area":+{"area":+"青岛校区",+"areaname":+"青岛校区"++}+}+}&funname=synjones.onecard.query.elec.building&json=true
扒的应该的：
jsondata=%7B+%22query_elec_roominfo%22%3A+%7B+%22aid%22%3A%220030000000002505%22%2C+%22account%22%3A+%22    823767    %22%2C%22room%22%3A+%7B+%22roomid%22%3A+%22    a325    %22%2C+%22room%22%3A+%22    a325    %22+%7D%2C++%22floor%22%3A+%7B+%22floorid%22%3A+%22%22%2C+%22floor%22%3A+%22%22+%7D%2C+%22area%22%3A+%7B+%22area%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22%2C+%22areaname%22%3A+%22%E9%9D%92%E5%B2%9B%E6%A0%A1%E5%8C%BA%22+%7D%2C+%22building%22%3A+%7B+%22buildingid%22%3A+%22    1503975890     %22%2C+%22building%22%3A+%22    %E5%87%A4%E5%87%B0%E5%B1%852%E5%8F%B7%E6%A5%BC    %22+%7D+%7D+%7D&funname=synjones.onecard.query.elec.roominfo&json=true
'''



c = '''
{
  "jsondata": "{ \"query_elec_roominfo\": { \"aid\":\"0030000000002505\", \"account\": \"823767\",\"room\": { \"roomid\": \"a325\", \"room\": \"a325\" },  \"floor\": { \"floorid\": \"\", \"floor\": \"\" }, \"area\": { \"area\": \"青岛校区\", \"areaname\": \"青岛校区\" }, \"building\": { \"buildingid\": \"1503975890\", \"building\": \"凤凰居2号楼\" } } }",
  "funname": "synjones.onecard.query.elec.roominfo",
  "json": "true"
}
'''
