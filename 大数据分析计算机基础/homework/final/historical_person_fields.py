import os
import pandas as pd


def fields_of_person_dimension(output: str):
    """
    从./字段含义.csv中读取字段意义, 并根据所有的表格内容分析得到与历史人物相关字段含义及其表格
    """
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')
    table_keys = {i: tables[i].columns.values for i in tables}

    person_keys = {}
    for i in table_keys:
        if 'c_personid' in table_keys[i]:
            person_keys.update({k: i for k in table_keys[i]})

    meaning = pd.read_csv('./字段含义.csv')

    df = pd.DataFrame({
        '字段': [k for k in person_keys if k in meaning['column_code'].values], 
        '中文意思': [meaning['meaning_cn'].values[meaning['column_code']==k][0] for k in person_keys if k in meaning['column_code'].values],
        '隶属表格': [person_keys[k] for k in person_keys if k in meaning['column_code'].values],
    })
    with open(output, 'w', encoding='utf-8') as f:
        df.to_csv(f, index=False, header=True)
    print("已分析完和历史人物相关的所有字段及相关表格, 结果储存到./人物字段.csv中")
        

def main(output: str):
    fields_of_person_dimension(output=output)

  
if __name__ == "__main__":
    main(output='./人物字段.csv')