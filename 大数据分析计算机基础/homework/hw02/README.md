# 文件介绍:
- crawler.py: 用于获取并爬取2013~2020年教育部网页数据的代码文件(第1题), 并输出到students.txt
- population.py: 用于计算2000到2020年各省人口总数(第二题), 并以此更新students.txt
- 20??/: 目录下存放着对应于20??年的小学,初中,高中学生统计表的html解析文本
- students.txt: 存放各年各省的各年级学生人数以及省总人口数
- students.xlsx: 从students.txt转为Excel文件并包含了各省各年小学一年级人数图、各省各年小学一年级人数与总人口比例图，各省高中毕业生人数与总人口比例图、各省各年小学毕业生人数与高中人数比例图(第3题)

# 问题解答(代码运行示例)
1. `python3 crawler.py`
2. `python3 population.py`
3. 见students.xlsx文件内附图

