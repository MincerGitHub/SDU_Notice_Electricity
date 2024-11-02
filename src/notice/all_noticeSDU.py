import pandas as pd
from bs4 import BeautifulSoup
import requests
import re
from lxml import etree
import json
from datetime import date
import threading


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


def get_max0():
    soup1 = BeautifulSoup(get_html(url0), 'html.parser')
    max = soup1.find('td', id='fanye128813').string
    max = re.search(r'/\d{3}', max).group()
    max = re.sub('/', '', max)
    return max

def get_max1():
    soup1 = BeautifulSoup(get_html(url1), 'html.parser')
    max = soup1.find(string=re.compile('/(.*?)页'))
    max = re.search(r'/(.*?)页', max).group()
    max = re.sub('[^0-9]', '', max)
    return max

def get_max2():
    soup1 = BeautifulSoup(get_html(url2), 'html.parser')
    max = soup1.find('span', class_="p_dot")
    max = max.next_sibling.text
    return max

def get_max3():
    tree = etree.HTML(get_html(url3))
    max = tree.xpath('/html/body/div[4]/div/div[2]/div[3]/div/span[1]/span[8]/a/text()')[0]
    return max


def create_data(tick, url):
    datas = []
    if tick == '0':
        soup = BeautifulSoup(get_html(url), 'html.parser')
        for unit in soup.find_all('div', class_='leftNews3', recursive=True):
            data = []
            unit =str(unit)
            times = re.findall(r'<div style="float:right;">\[(.*?)]</div>', unit)
            data.append(*times)
            titles = re.findall(r'title="(.*?)"', unit)
            if not titles:
                titles = ['nothing']
            data.append(*titles)
            links = re.findall(r'<a href="(.*?)"', unit)
            for link in links:
                if not link.startswith('h'):
                    link.replace('../../','').replace('../','')
                    link = 'https://www.bkjx.sdu.edu.cn/' + link
                data.append(link)
            data.append('本科生院')
            datas.append(data)
        return datas
    elif tick == '1':
        soup = BeautifulSoup(get_html(url), 'html.parser')
        for unit in soup.find_all('a', class_='item', recursive=True):
            data = []
            unit =str(unit)
            times = re.findall(r'<div class="date">(.*?)</div>', unit)
            data.append(*times)
            titles = re.findall(r'<div class="title">(.*?)</div>', unit)
            if not titles:
                titles = ['nothing']
            data.append(*titles)
            links = re.findall(r'href="(.*?)"', unit)
            for link in links:
                if not link.startswith('h'):
                    link = 'http://online.sdu.edu.cn/' + link
                data.append(link)
            data.append('学生在线')
            datas.append(data)
        return datas
    elif tick == '2':
        tree = etree.HTML(get_html(url))
        for i in range(1, 21):
            data = []
            a = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/div/span/text()')
            b = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/div/p/text()')
            time = '-'.join(a + b)
            data.append(time)
            title = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/a/text()')[0]
            title = title
            data.append(title)
            link = tree.xpath(f'/html/body/div[2]/div[2]/div[2]/ul/li[{i}]/a/@href')[0]
            if not link.startswith('h'):
                link = 'https://www.youth.sdu.edu.cn/' + link
            data.append(link)
            data.append('青春山大')
            datas.append(data)
        return datas
    elif tick == '3':
        soup = BeautifulSoup(get_html(url), 'html.parser')
        for unit in soup.find_all(r'li', id=re.compile('line_u.*'), recursive=True):
            data = []
            unit =str(unit)
            times = re.findall(r'<span class="fr">(.*?)</span>', unit)
            data.append(*times)
            titles = re.findall(r'title="(.*?)"', unit)
            if not titles:
                titles = ['nothing']
            data.append(*titles)
            links = re.findall(r'<a href="(.*?)"', unit)
            for link in links:
                if not link.startswith('h'):
                    link = 'https://www.cs.sdu.edu.cn/' + link
                data.append(link)
            data.append('计科学院')
            datas.append(data)
        return datas



def get_news(tick, maxi):
    datass = []
    url = eval('url' + tick)
    for data in create_data(tick, url):
        datass.append(data)
    for i in range(2, maxi):
        if tick == '0':
            urlf = f'https://www.bkjx.sdu.edu.cn/index/gztz/{i}.htm'
        elif tick == '1':
            urlf = f'https://online.sdu.edu.cn/txtlist.jsp?totalpage={maxi}&PAGENUM={i}&urltype=tree.TreeTempUrl&wbtreeid=1016'
        elif tick == '2':
            urlf = f'https://www.youth.sdu.edu.cn/list.jsp?totalpage={maxi}&PAGENUM={i}&urltype=tree.TreeTempUrl&wbtreeid=1004'
        elif tick == '3':
            urlf = f'https://www.cs.sdu.edu.cn/bkjy/{i-1}.htm'
        for data in create_data(tick, urlf):
            datass.append(data)
    return datass


def save_news(datass, path):
    full_datas = pd.DataFrame(datass)
    full_datas = full_datas.rename(columns={0: 'time', 1: 'title', 2: 'url', 3:'source'})
    full_datas.to_excel(path, index=False, engine='openpyxl')


def benkeshengyuan():
    maxi = int(get_max0())
    datass = get_news('0', maxi)
    save_news(datass, './cache/0.xlsx')

def xueshengzaixian():
    maxi = int(get_max1())
    datass = get_news('1', maxi)
    save_news(datass, './cache/1.xlsx')

def qingchunshanda():
    maxi = int(get_max2())
    datass = get_news('2', maxi)
    save_news(datass, './cache/2.xlsx')

def jikexueyuan():
    maxi = int(get_max3())
    datass = get_news('3', maxi)
    save_news(datass, './cache/3.xlsx')



def main():
    thread_list = []
    lis = ['0', '0', '0', '0']
    with open("notice_initialize.json") as file:
        a = json.load(file)
    path = a['path'] + 'all_notice_' + str(date.today()) + '.xlsx'
    print('loading...')
    if a['benkeshengyuan'] == '1':
        t0 = threading.Thread(target=benkeshengyuan())
        thread_list.append(t0)
        lis[0] = '1'
    if a['xueshengzaixian'] == '1':
        t1 = threading.Thread(target=xueshengzaixian())
        thread_list.append(t1)
        lis[1] = '1'
    if a['qingchunshanda'] == '1':
        t2 = threading.Thread(target=qingchunshanda())
        thread_list.append(t2)
        lis[2] = '1'
    if a['jikexueyuan'] == '1':
        t3 = threading.Thread(target=jikexueyuan())
        thread_list.append(t3)
        lis[3] = '1'
    for i in thread_list:
        i.start()
    for i in thread_list:
        i.join()

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

    main()