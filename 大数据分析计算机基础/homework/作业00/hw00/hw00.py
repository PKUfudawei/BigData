import numpy as np
import pandas as pd

with open('./contestData.txt', mode='r') as f:
    text=f.read().replace(',', ' ').split()
    
work_category = pd.read_csv('./work_cat.csv')

def encode1(lst: list, sort: bool=True):
    out = []
    for s in lst:
        if '强烈推荐' in s:
            out.append('2')
        elif '不推荐' in s:
            out.append('0')
        else:
            out.append('1')
    if sort:
        out.sort(reverse=True) ## from max to min
    return ''.join(out)

data1 = {
    '作品编号': np.array([int(text[i]) for i in range(0, len(text), 4)]),
    '得分构型': np.array([encode1(text[i+1:i+4]) for i in range(0, len(text), 4)])
}
data1['作品类别'] = np.array([
    work_category[work_category['作品编号']==i]['类别'].to_list()[0] for i in data1['作品编号']
])

df1 = pd.DataFrame(data=data1)
df1.to_csv('runResult00.txt', sep='\t', index=False, header=True, encoding="utf-8")

def encode2(lst: list):
    referee, level = [], []
    for l in lst:
        token = l.split('(')
        referee.append(token[0])
        level.append(token[1][:-1])
    
    return referee, level

data2 = {
    '作品编号': [i for i in data1['作品编号'] for _ in range(3)],
    '评委姓名': np.array([encode2(text[i+1:i+4])[0] for i in range(0, len(text), 4)]).flatten(),
    '推荐等级': np.array([encode2(text[i+1:i+4])[1] for i in range(0, len(text), 4)]).flatten(),
}
df2 = pd.DataFrame(data=data2)
df2.to_csv('runResult01.txt', sep='\t', index=False, header=True, encoding="utf-8")
