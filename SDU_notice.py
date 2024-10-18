import re
import time
import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_soup(url):
    head = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0'
    }
    response = requests.get(url=url, headers=head)
    html = response.text.encode('ISO-8859-1')
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def get_max():
    soup1 = get_soup('https://www.bkjx.sdu.edu.cn/index/gztz.htm', )
    max = soup1.find('td', id='fanye128813').string
    max = re.search(r'/\d{3}', max).group()
    max = re.sub('/', '', max)
    return max


def create_data(url):
    datas = []
    soup = get_soup(url)
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
            link.replace('../..', 'https://www.bkjx.sdu.edu.cn')
            link.replace('..', 'https://www.bkjx.sdu.edu.cn')
            data.append(link)
        datas.append(data)
    return datas



def get_news():
    datass = []
    url1 = 'https://www.bkjx.sdu.edu.cn/index/gztz.htm'
    for data in create_data(url1):
        datass.append(data)
    max = int(get_max())
    for i in range(2, max):
        time.sleep(0.5)
        url = f'https://www.bkjx.sdu.edu.cn/index/gztz/{i}.htm'
        for data in create_data(url):
            datass.append(data)
    return datass


def save_news(datass, path):
    full_datas = pd.DataFrame(datass)
    full_datas = full_datas.rename(columns={0: 'time', 1: 'title', 2: 'url'})
    full_datas = full_datas.sort_values(by=['time'], ascending=False)
    full_datas.to_excel(path, index=False)


if __name__ == '__main__':
    datas = get_news()
    path = input('Set path:')
    save_news(datas, path)
    print('Success')
