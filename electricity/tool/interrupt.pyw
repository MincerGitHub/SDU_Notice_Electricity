import json


with open('../electricity_initialize.json', 'r', encoding='utf-8') as file:
    init = json.load(file)
init["sleep"] = "1"
with open("../electricity_initialize.json", "w", encoding='utf-8') as file:
    json.dump(init, file, ensure_ascii=False, indent=4)
