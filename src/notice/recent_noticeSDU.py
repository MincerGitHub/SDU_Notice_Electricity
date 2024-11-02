from datetime import date
import time
import schedule
import json
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import pandas as pd

url0 = 'https://www.bkjx.sdu.edu.cn/index/gztz.htm'
url1 = 'https://online.sdu.edu.cn/txtlist.jsp?urltype=tree.TreeTempUrl&wbtreeid=1016'
url2 = 'https://www.youth.sdu.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1004'
url3 = 'https://www.cs.sdu.edu.cn/bkjy.htm'

def get_html(url):
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }
    response = requests.get(url=url, headers=head)
    try:
        html = response.text.encode('ISO-8859-1')
    except UnicodeEncodeError:
        html = response.text
    return html

def create_content(link):
    soup = BeautifulSoup(get_html(link), 'html.parser')
    ps = soup.find_all('p')
    content = ''
    for p in ps:
        content_r = p.get_text()
        content_c = re.sub(r'\s+', ' ', content_r)
        content = content + content_c
    return content

def create_datas0():
    datas = []
    tree = etree.HTML(get_html(url0))
    for i in range(1,6):
        data = []
        time = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[{i}]/div[3]/text()')[0].strip('[]')
        data.append(time)
        title = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[{i}]/div[2]/a/text()')[0]
        data.append(title)
        link = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/div[2]/div/div[{i}]/div[2]/a/@href')[0]
        if not link.startswith('h'):
            link = 'https://www.bkjx.sdu.edu.cn/' + link
        data.append(link)
        data.append('本科生院')
        data.append(create_content(link))
        datas.append(data)
    return datas

def create_datas1():
    datas = []
    tree = etree.HTML(get_html(url1))
    for i in range(1,6):
        data = []
        time = tree.xpath(f'/html/body/div/section/div/div[2]/div[1]/a[{i}]/div[3]/div[1]/text()')[0]
        data.append(time)
        title = tree.xpath(f'/html/body/div/section/div/div[2]/div[1]/a[{i}]/div[1]/text()')[0]
        data.append(title)
        link = tree.xpath(f'/html/body/div/section/div/div[2]/div[1]/a[{i}]/@href')[0]
        if not link.startswith('h'):
            link = 'https://online.sdu.edu.cn/' + link
        data.append(link)
        data.append('学生在线')
        data.append(create_content(link))
        datas.append(data)
    return datas

def create_datas2():
    datas = []
    tree = etree.HTML(get_html(url2))
    for i in range(1,6):
        data = []
        a = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/div/span/text()')[0]
        b = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/div/p/text()')[0]
        seq = [a, b]
        time = '-'.join(seq)
        data.append(time)
        title = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/a/text()')[0]
        data.append(title)
        link = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/a/@href')[0]
        if not link.startswith('h'):
            link = 'https://www.youth.sdu.edu.cn/' + link
        data.append(link)
        data.append('青春山大')
        data.append(create_content(link))
        datas.append(data)
    return datas


def create_datas3():
    datas = []
    tree = etree.HTML(get_html(url3))
    for i in range(1,6):
        data = []
        time = tree.xpath(f'/html/body/div[4]/div/div[2]/div[2]/ul/li[{i}]/span/text()')[0]
        data.append(time)
        title = tree.xpath(f'/html/body/div[4]/div/div[2]/div[2]/ul/li[{i}]/a/text()')[0]
        data.append(title)
        link = tree.xpath(f'/html/body/div[4]/div/div[2]/div[2]/ul/li[{i}]/a/@href')[0]
        if not link.startswith('h'):
            link = 'https://www.cs.sdu.edu.cn/' + link
        data.append(link)
        data.append('计科学院')
        data.append(create_content(link))
        datas.append(data)
    return datas


def save_datas(datas, path):
    full_datas = pd.DataFrame(datas)
    full_datas = full_datas.rename(columns={0: 'time', 1: 'title', 2: 'url', 3:'source', 4:'content'})
    full_datas.to_excel(path, index=False, engine='openpyxl')


def main():
    lis = ['0', '0', '0', '0']
    with open("notice_initialize.json") as file:
        a = json.load(file)
    path = a['path'] + 'recent_notice_' + str(date.today()) + '.xlsx'
    print('loading...')
    if a['benkeshengyuan'] == '1':
        save_datas(create_datas0(), './cache/0.xlsx')
        lis[0] = '1'
    if a['xueshengzaixian'] == '1':
        save_datas(create_datas1(), './cache/1.xlsx')
        lis[1] = '1'
    if a['qingchunshanda'] == '1':
        save_datas(create_datas2(), './cache/2.xlsx')
        lis[2] = '1'
    if a['jikexueyuan'] == '1':
        save_datas(create_datas3(), './cache/3.xlsx')
        lis[3] = '1'

    collection = []
    for i in range(0, 4):
        if lis[i] == '1':
            exec(f"collection.append(pd.read_excel('cache/{i}.xlsx'))")
    result = pd.concat(collection)
    lis = ['0', '0', '0', '0']

    with pd.ExcelWriter(path, engine='xlsxwriter') as writer:
        result.sort_values(by='time', inplace=True, ascending=False)
        result.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        for i, col in enumerate(result.columns):
            column_len = result[col].astype(str).str.len().max() + 1
            worksheet.set_column(i, i, column_len)
    print('Success')

if __name__ == '__main__':
    with open('notice_initialize.json','r', encoding='utf-8') as file:
        init = json.load(file)
    print("初始化：输入'0'表示否/输入'1'表示是（请在1min内完成输入）")
    print('是否需要“本科生院,学生在线,青春山大,计科学院”的通知;并输入“路径（到目录,若空则默认为本文件夹下）”;是否定时执行（各项用,隔开）：')
    try:
        for i in range(0,60):
            time.sleep(1)
        print('继续进行定时保存通知')
    except KeyboardInterrupt:
        ans = input()
        ans_list = ans.split(',')
        init["benkeshengyuan"] = ans_list[0]
        init["xueshengzaixian"] = ans_list[1]
        init["qingchunshanda"] = ans_list[2]
        init["jikexueyuan"] = ans_list[3]
        init["path"] = ans_list[4]
        with open("notice_initialize.json", "w", encoding='utf-8') as file:
            json.dump(init, file, ensure_ascii=False, indent=4)

    main()

    if init["sleep"] == '0':
        schedule.every().day.at("08:00").do(main)

        while True:
            schedule.run_pending()
            time.sleep(10)







