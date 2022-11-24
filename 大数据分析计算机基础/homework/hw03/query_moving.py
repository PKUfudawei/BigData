#!/usr/bin/env python3
import pandas as pd
import numpy as np
import os
from datetime import datetime

degree_to_km = 60 * 60 * 31 / 1000


def clean_data():
    """
    数据清洗, 丢掉时间不合理或者经纬度过于偏离的数据, 储存到cleaned.parq
    """
    df = pd.read_csv('./20170906.csv', header=None, names=['id', 'time', 'longitude', 'latitude', 'info1', 'info2', 'info3', 'info4'])
    beijing = {
        'longitude_min': 115.7,
        'longitude_max': 117.4,
        'latitude_min': 39.4,
        'latitude_max': 41.6
    }
    normal = (
        np.char.startswith(df['time'].to_numpy(dtype=str), prefix='2017') & 
        (df['longitude'] < 119) &
        (df['longitude'] > 114) &
        (df['latitude'] < 42) &
        (df['latitude'] > 37)
    )

    with open('./cleaned.parq', 'wb') as f:
        df = df[['id', 'time', 'longitude', 'latitude']][normal].sort_values('time', inplace=False)
        df.to_parquet(f, index=False)


def path_length(time: np.array, x: np.array, y: np.array):
    """
    高速公路上货车的最高限速为100km/h, 因此采用的算法是果与相邻两点距离都超过限速, 说明该点飘移, 跳过此点坐标, 最后累加所有合理点之间距离
    """
    if len(time) >= 3:
        time = [datetime.strptime(t, "%Y-%m-%d %H:%M:%S") for t in time]
        delta_time = np.array([(time[i + 1] - time[i]).seconds for i in range(len(time) - 1)])
        new_x, new_y = [x[0]], [y[0]]
        for i in range(1, len(time) - 1):
            distance1 = np.sqrt((x[i] - x[i - 1])**2 + (y[i] - y[i - 1])**2) * degree_to_km
            distance2 = np.sqrt((x[i + 1] - x[i])**2 + (y[i + 1] - y[i])**2) * degree_to_km
            if distance1 > delta_time[i - 1] / 3600 * 100 and distance2 > delta_time[i] / 3600 * 100:
                continue  # 如果与相邻两点距离都超过限速, 说明该点飘移, 跳过此点坐标
            new_x.append(x[i])
            new_y.append(y[i])
        new_x.append(x[-1])
        new_y.append(y[-1])
        x, y = np.array(new_x), np.array(new_y)
    
    delta_x = x[1:] - x[:-1]
    delta_y = y[1:] - y[:-1]
    dist = np.sqrt(delta_x**2 + delta_y**2)
    moving_time = np.sum(delta_time[dist > 0])
    if moving_time > 0:
        print("在该时间段内发生位移")
        print("位移时长: %d小时%d分钟%d秒" % (moving_time // 3600, moving_time % 3600 // 60, moving_time % 3600 % 60))
        return np.sum(dist) * degree_to_km
    else:
        print("在该时间段内未发生位移")
        return 0


def query_path_length(df: pd.DataFrame, id: str, start_time: str, end_time):
    """
    按照脱敏车号, 查询起始时间, 查询终止时间, 得到该时间段内该车是否位移, 以及位移多久, 位移多远
    """
    print("筛选数据中, 请稍后")
    df_ = df[
        (df['id']==id) & 
        (df['time'] >= start_time) &
        (df['time'] <= end_time)
    ]
    return path_length(time=df_['time'].values, x=df_['longitude'].values, y=df_['latitude'].values)


def main():
    print("读取数据库中, 大约需要20秒")
    if not os.path.exists('./cleaned.parq'):
        print("先从原始数据库20170906.csv进行数据清洗")
        clean_data()
    df = pd.read_parquet('./cleaned.parq')
    id_no = input("请输入待查询脱敏车号(格式参考1f3e65be-d8cd-4d63-b525-fdaa5848188f): ")
    start_time = input("请输入查询起始时间(格式参考2017-01-06 04:32:10): ")
    end_time = input("请输入查询终止时间(格式参考2017-11-05 23:39:55): ")
    moving_length = query_path_length(df=df, id=id_no, start_time=start_time, end_time=end_time)
    if moving_length > 0:
        print("位移距离:", moving_length, 'km')


if __name__ == "__main__":
    main()
