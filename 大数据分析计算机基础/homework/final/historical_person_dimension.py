import os
import pandas as pd
import numpy as np
import plotly.express as px


def family_name_word_cloud(output: str):
    """
    从历史人物相关字段中得到历史人物姓氏数量分布, 并结合中国地图生成词云
    """
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')

    family_name = [s[0] for s in tables['BIOG_MAIN']['c_name_chn'].values]
    sery = pd.value_counts(family_name)
    df = pd.DataFrame({'姓氏': sery.index[:500], '数量': sery.values[:500]})
    with open(output, 'w', encoding='utf-8') as f:
        df.to_csv(f, index=False)
    print(f"已将数量前500的姓氏及其数量储存到{output}中")
    print("已将词云生成到./姓氏词云.jpg中")


def gender_number_per_dynasty(output: str):
    """
    按照各朝代统计不同性别的历史人物数量
    """
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
    # fig.show()
    fig.write_image(output)
    print(f"已将各朝代不同性别的历史人物数量统计储存到{output}中")
    
    
def lifetime_per_dynasty(output: str):
    """
    按照各朝代统计不同性别的历史人物平均寿命
    """
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
    # fig.show()
    fig.write_image(output)
    print(f"已将各朝代不同性别的历史人物平均寿命统计储存到{output}中")

    
def born_month(output: str):
    """
    统计历史人物出生月份
    """
    tables = {}
    table_names = []
    for f in os.listdir('./parquet'):
        table_names.append(f.split('.')[0])
        tables[f.split('.')[0]] = pd.read_parquet(f'./parquet/{f}')

    stats = pd.value_counts(tables['BIOG_MAIN']['c_by_month'][tables['BIOG_MAIN']['c_by_month']>0])

    fig = px.bar({'出生月份': stats.index, '计数': stats.values}, x='出生月份', y='计数', color='计数')
    # fig.show()
    fig.write_image(output)
    print(f"已将历史人物出生月份统计储存到{output}中")
    

def main():
    family_name_word_cloud(output='./姓氏排名.csv')
    gender_number_per_dynasty(output='./images/各朝代不同性别历史人物数量.pdf')
    lifetime_per_dynasty(output='./images/各朝代不同性别历史人物平均寿命.pdf')
    born_month(output='./images/出生月份.pdf')


if __name__ == "__main__":
    main()
