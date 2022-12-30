import os
import pandas as pd
import numpy as np
import plotly.express as px


def family_name_word_cloud(output: str):
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')

    family_name = [s[0] for s in tables['BIOG_MAIN']['c_name_chn'].values]
    sery = pd.value_counts(family_name)
    df = pd.DataFrame({'weight': sery.values[:500], 'word': sery.index[:500]})
    with open(output, 'w', encoding='utf-8') as f:
        df.to_csv(f, index=False)


def gender_number_per_dynasty(output: str):
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')
    
    dynasty = [2, 23, 27, 5, 6, 15, 18, 19, 20, 21]
    df = pd.DataFrame({'朝代': [], '性别': [], '计数': []})
    df_dy = pd.read_parquet('./parquet/DYNASTIES.parq')
    for dy in dynasty:
        df.loc[len(df)] = [df_dy[df_dy['c_dy']==dy]['c_dynasty_chn'].values[0], '男', sum((tables['BIOG_MAIN']['c_dy']==dy) & (tables['BIOG_MAIN']['c_female']==0))]
        df.loc[len(df)] = [df_dy[df_dy['c_dy']==dy]['c_dynasty_chn'].values[0], '女', sum((tables['BIOG_MAIN']['c_dy']==dy) & (tables['BIOG_MAIN']['c_female']==0))]
    fig = px.bar(df, x="朝代", y="计数", color='性别', barmode='group', log_y=True, range_y=[1, 2e5])
    fig.show()
    fig.write_image(output)
    
    
def lifetime_per_dynasty(output: str):
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')
    
    dynasty = [2, 23, 27, 5, 6, 15, 18, 19, 20, 21]
    df = pd.DataFrame({'朝代': [], '性别': [], '平均寿命': []})
    df_dy = pd.read_parquet('./parquet/DYNASTIES.parq')
    for dy in dynasty:
        df.loc[len(df)] = [df_dy[df_dy['c_dy']==dy]['c_dynasty_chn'].values[0], '男', np.mean(tables['BIOG_MAIN'][(tables['BIOG_MAIN']['c_dy']==dy) & (tables['BIOG_MAIN']['c_female']==0)]['c_death_age'])]
        df.loc[len(df)] = [df_dy[df_dy['c_dy']==dy]['c_dynasty_chn'].values[0], '女', np.mean(tables['BIOG_MAIN'][(tables['BIOG_MAIN']['c_dy']==dy) & (tables['BIOG_MAIN']['c_female']==1)]['c_death_age'])]
    fig = px.bar(df, x="朝代", y="平均寿命", color='性别', barmode='group')
    fig.show()
    fig.write_image(output)

    
def born_month(output: str):
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')

    stats = pd.value_counts(tables['BIOG_MAIN']['c_by_month'][tables['BIOG_MAIN']['c_by_month']>0])

    fig = px.bar({'出生月份': stats.index, '计数': stats.values}, x='出生月份', y='计数', color='计数')
    fig.show()
    fig.write_image(output)
    

def main():
    family_name_word_cloud(output='./word_cloud.csv')
    gender_number_per_dynasty(output='./images/gender_number_per_dynasty.pdf')
    lifetime_per_dynasty(output='./images/lifetime_per_dynasty.pdf')
    born_month(output='./images/born_month.pdf')
    

if __name__ == "__main__":
    main()
