# 文件介绍:

-   cleaned.parq: 20170906.csv 经过数据清洗后输出的文件, 下面的数据分析都以此数据库为基础. 该文件约 2.72G, 需要通过[北大网盘](https://disk.pku.edu.cn:443/link/89C0207485DAF19DDC0430FFDF8571C5)下载.
-   query_moving.py: 判断一辆货车在指定时间段内的是否位移，位移时长、位移距离.
-   visualize.py: 数据图形化显示 1 平方公里和 100 平方米范围内的数据密度图, 并以每 1 平方公里/100 平方米为方格画出北京及周边区域的路网连线图, 然后进行停车场排除(停车场方格的速度应该远大于周围方格), 再画出停车场排除后的路网连线图.
-   1km_square_before_clean_parking.png: 显示排除停车区前的以 1 平方公里为基本方格的路网连线图.
-   1km_square_after_clean_parking.png: 显示排除停车区后的以 1 平方公里为基本方格的路网连线图.
-   100m_square_after_clean_parking.png: 显示排除停车区前的以 100 平方米为基本方格的路网连线图.
-   100m_square_after_clean_parking.png: 显示排除停车区后的以 100 平方米为基本方格的路网连线图.

# 问题解答(代码运行示例)

1. `python3 query_moving.py`: 开始读取./cleaned.parq, 然后依照命令行提示格式输入脱敏车号、起始时间即可
2. `python3 visualize.py`: 开始读取./cleaned.parq, 然后画出 4 个.png 文件图.
