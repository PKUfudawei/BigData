#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

degree_to_km = 60 * 60 * 31 / 1000


def clean_data():
    """
    数据清洗, 丢掉时间不合理或者经纬度过于偏离北京的数据, 储存到cleaned.parq
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


def raw_plot_1km2(x, y):
    """
    画出排除停车区之前的路网连线密度图, 以一平方千米内的数据个数为区域密度
    """
    print("清理停车区前的数据可视化: (以1平方公里为分区)")
    plt.figure(figsize=(8, 7))
    my_cmap = plt.cm.get_cmap("jet").copy()
    my_cmap.set_under('lightgrey', 1)
    x_bins = int((np.max(x) - np.min(x)) * degree_to_km)  # 按1km为距离分bin
    y_bins = int((np.max(y) - np.min(y)) * degree_to_km)  # 按1km为距离分bin
    h = plt.hist2d(x=x, y=y, bins=(x_bins, y_bins), vmin=1, vmax=3e3, cmap=my_cmap)
    plt.colorbar(h[3])
    print(f"已存为1km_square_before_clean_parking.png")
    plt.savefig("1km_square_before_clean_parking.png", bbox_inches='tight')
    # plt.show()
    return h
    
    
def raw_plot_100m2(x, y):
    """
    画出排除停车区之前的路网连线密度图, 以100平方米内的数据个数为区域密度
    """
    print("清理停车区前的数据可视化: (以100平方米为分区)")
    plt.figure(figsize=(8, 7))
    my_cmap = plt.cm.get_cmap("jet").copy()
    my_cmap.set_under('lightgrey', 1)
    x_bins = int((np.max(x) - np.min(x)) * degree_to_km * 10)  # 按100m为距离分bin
    y_bins = int((np.max(y) - np.min(y)) * degree_to_km * 10)  # 按100m为距离分bin
    h = plt.hist2d(x=x, y=y, bins=(x_bins, y_bins), vmin=1, vmax=3e1, cmap=my_cmap)
    plt.colorbar(h[3])
    print("已存为100m_square_before_clean_parking.png")
    plt.savefig("100m_square_before_clean_parking.png", bbox_inches='tight')
    # plt.show()
    return h
    

def clean_parking(h, name: str = '1km'):
    """
    以排除停车区之前的区域密度分布作为输入, 如果有停车区, 则停车区的密度会远大于周围九宫格的密度, 触发停车区判定则将停车区密度计为0
    """
    print("清理停车区后的数据可视化:")
    map_2d = h[0]
    for i in range(1, map_2d.shape[0]):
        for j in range(1, map_2d.shape[1]):
            neighbors = sorted(map_2d[i - 1:i + 2, j - 1:j + 2].flatten(), reverse=True)
            if len(neighbors)<=1:
                print(i, j)
            if neighbors[0] == map_2d[i, j] and neighbors[0] - np.mean(neighbors[1:]) > 0.9 * neighbors[0]:
                map_2d[i, j] = 0

    plt.figure(figsize=(8, 7))
    df = pd.DataFrame(map_2d[:, ::-1].T, index = [round(x, 3) for x in h[2][-1:0:-1]], columns = [round(x, 3) for x in h[1][1:]])
    gap = 100 if name=='1km' else 1000
    vmax = 3e3 if name=='1km' else 3e1
    sns.heatmap(df, vmin=0, vmax=vmax, center=0, annot=False, xticklabels = gap, yticklabels = gap)
    print(f"已存为{name}_square_after_clean_parking.png")
    plt.savefig(f"{name}_square_after_clean_parking.png", bbox_inches='tight')
    # plt.show()


def main():
    print("读取数据库中, 大约需要20秒")
    if not os.path.exists('./cleaned.parq'):
        print("先从原始数据库20170906.csv进行数据清洗")
        clean_data()
    df = pd.read_parquet('./cleaned.parq')
    x = df['longitude'].values
    y = df['latitude'].values
    h = raw_plot_1km2(x, y)
    clean_parking(h, name='1km')
    h = raw_plot_100m2(x, y)
    clean_parking(h, name='100m')


if __name__ == "__main__":
    main()
