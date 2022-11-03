#!/usr/bin/env python3
import requests
import pandas as pd
import time
import random
import os

from urllib.parse import urljoin
from bs4 import BeautifulSoup

headerData={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}


def parseProvince(string):
    def isChinese(char):
        # 判断字符是否为汉字
        return (0x4e00<=ord(char)<0x9fa5)
    
    return ''.join([char for char in string if isChinese(char)])


def parsePrimary(link: str, year: int):
    print(f'{year} 小学生统计表:', link)
    response = requests.get(link, headers=headerData)
    response.encoding = "utf-8"
    with open(f'./{year}/primary.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    bs = BeautifulSoup(response.text, "html.parser")
    table = bs.find_all('table')[4]
    df = pd.DataFrame(columns=['省份', '年份', '年级', '人数'])
    START = False
    for row in table.find_all('tr'):
        if len(row.find_all('p'))>0:
            column = row.find_all('p')
        else:
            column = row.find_all('td')
        province = parseProvince(column[0].text)
        if province=='北京':
            START = True
        if (not START) or len(province)==0:
            continue
        df.loc[len(df.index)] = [province, year, '小1', int(column[-7].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '小2', int(column[-6].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '小3', int(column[-5].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '小4', int(column[-4].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '小5', int(column[-3].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '小6', int(column[-2].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '小毕', int(column[1].text.strip() or 0)]
    return df


def parseJunior(link: str, year: int):
    print(f'{year} 初中生统计表:', link)
    response = requests.get(link, headers=headerData)
    response.encoding = "utf-8"
    with open(f'./{year}/junior.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    bs = BeautifulSoup(response.text, "html.parser")
    table = bs.find_all('table')[4]
    df = pd.DataFrame(columns=['省份', '年份', '年级', '人数'])
    START = False
    for row in table.find_all('tr'):
        if len(row.find_all('p'))>0:
            column = row.find_all('p')
        else:
            column = row.find_all('td')
        province = parseProvince(column[0].text)
        if province=='北京':
            START = True
        if (not START) or len(province)==0:
            continue
        df.loc[len(df.index)] = [province, year, '初1', int(column[-5].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '初2', int(column[-4].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '初3', int(column[-3].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '初4', int(column[-2].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '初毕', int(column[1].text.strip() or 0)]
    return df


def parseSenior(link: str, year: int):
    print(f'{year} 高中生统计表:', link)
    response = requests.get(link, headers=headerData)
    response.encoding = "utf-8"
    with open(f'./{year}/senior.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    bs = BeautifulSoup(response.text, "html.parser")
    table = bs.find_all('table')[4]
    df = pd.DataFrame(columns=['省份', '年份', '年级', '人数'])
    START = False
    for row in table.find_all('tr'):
        if len(row.find_all('p'))>0:
            column = row.find_all('p')
        else:
            column = row.find_all('td')
        province = parseProvince(column[0].text)
        if province=='北京':
            START = True
        if (not START) or len(province)==0:
            continue
        df.loc[len(df.index)] = [province, year, '高1', int(column[-4].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '高2', int(column[-3].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '高3', int(column[-2].text.strip() or 0)]
        df.loc[len(df.index)] = [province, year, '高毕', int(column[1].text.strip() or 0)]
    return df


def main():
    link0 = 'https://www.moe.gov.cn/jyb_sjzl/moe_560/2020/'
    r0 = requests.get(link0, headers=headerData)
    r0.encoding = "utf-8"
    bs0 = BeautifulSoup(r0.text, "html.parser")

    df = pd.DataFrame(columns=['省份', '年份', '年级', '人数'])

    for year in range(2013, 2021):
        if not os.path.exists(f'./{year}'):
            os.makedirs(f'./{year}')
        time.sleep(random.randint(1, 3))
        link_year = urljoin(link0, bs0.find('li', text=f'{year}年教育统计数据').a['href'])
        r1 = requests.get(link_year, headers=headerData)
        r1.encoding = "utf-8"
        bs1 = BeautifulSoup(r1.text, "html.parser")
        link_year_region = urljoin(link_year, bs1.find('a', text='各地基本情况')['href'])
        
        time.sleep(random.randint(1, 3))
        r2 = requests.get(link_year_region, headers=headerData)
        r2.encoding = "utf-8"
        bs2 = BeautifulSoup(r2.text, "html.parser")
        if bs2.find('a', text='普通高中学生数'):
            df_1 = parseSenior(urljoin(link_year_region, bs2.find('a', text='普通高中学生数')['href']), year)
        else:
            df_1 = parseSenior(urljoin(link_year_region, bs2.find('a', text='普通高中学生数(总计)')['href']), year)
        
        time.sleep(random.randint(1, 3))
        r3 = requests.get(urljoin(link_year_region, './index_1.html'), headers=headerData)
        r3.encoding = "utf-8"
        bs3 = BeautifulSoup(r3.text, "html.parser")
        if bs3.find('a', text='初中学生数'):
            df_2 = parseJunior(urljoin(link_year_region, bs3.find('a', text='初中学生数')['href']), year)
        else:
            df_2 = parseJunior(urljoin(link_year_region, bs3.find('a', text='初中学生数(总计)')['href']), year)
        if bs3.find('a', text='小学学生数'):
            df_3 = parsePrimary(urljoin(link_year_region, bs3.find('a', text='小学学生数')['href']), year)
        else:
            df_3 = parsePrimary(urljoin(link_year_region, bs3.find('a', text='小学学生数(总计)')['href']), year)
        df = pd.concat([df, df_3, df_2, df_1], ignore_index=True)
    
    with open('students.txt', 'w') as f:
        df.to_csv(f, sep='\t', index=False, header=True, encoding="utf-8")


if __name__=="__main__":
    main()
