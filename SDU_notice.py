import re
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url):
    head = {
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
        # 'Referer':'https://www.bkjx.sdu.edu.cn/index/gztz/{}.htm'
    }
    response = requests.get(url=url, headers=head)
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_max():
    soup1 = get_soup('https://www.bkjx.sdu.edu.cn/index/gztz.htm')
    max = soup1.find('td', id='fanye128813')
    return max


def get_news():
    datas = []
    max = int(get_max())
    for i in range(1, max+1):
        url = f'https://www.bkjx.sdu.edu.cn/index/gztz/{i}.htm'
        soup = get_soup(url)
        for unit in soup.find_all('div', class_='leftNews3'):
            findLink = re.compile(r'<a herf="(.*?)">')
            findTitle = re.compile(r'<title="(.*?)">')
            findTime = re.compile(r'<div style="float:right;">(.*?)</div>')
            data =[]
            unit =str(unit)
            link = re.findall(findLink, unit)[0]
            data.append(link)
            titles = re.findall(findTitle, unit)[0]
            data.append(titles)
            times = re.findall(findTime, unit)[0]
            data.append(times)
            datas.append(data)
    return datas


def save_news(datas, path):
    pass


if __name__ == '__main__':
    datas = get_news()
    save_news(datas, 'news')
    print('Success')
