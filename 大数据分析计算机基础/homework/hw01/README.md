# 文件介绍:
- input_method.py: 是联想输入法执行文件(包含训练模块), 可同时用于字的联想和词的联想(即第2题和第3题)
- input_method.pickle: 是在news2016zh_train.json上训练得到的联想字频数据库, 同时保存了单字和词语的跟随字(按频次从高到低排列), 用于给input_method.py提供联想数据
- 联想输入法运行示例.jpeg: 演示联想输入法工作模式的图片
- count_frequency.py: 是产生HF_SingleHZ.txt和HF_Word.txt的代码文件(第4题和第5题)
- HF_SingleHZ.txt: 统计了覆盖80%文本(news2016zh_train.json)的最少单字, 并保存了字频、累计字频且按字频从高到低顺序.
- HF_Word.txt: 统计词语出现频次，将排名最高的10000个词语输出并保存了词条和频次

# 问题解答(代码运行示例)
1. 无要求
2. 命令行执行`python3 input_method.py (-n $number)`即可, 其中`$number`为最大候选字数目, 默认为50
3. 命令行执行`python3 input_method.py (-n $number)`即可, 其中`$number`为最大候选字数目, 默认为50
4. `python3 count_frequency.py`即可分析并产生HF_SingleHZ.txt文件(需要news2016zh_train.json文件)
5. `python3 count_frequency.py`即可分析并产生HF_Word.txt文件(需要news2016zh_train.json文件)

# 大文件链接
[北大网盘/SINA_News](https://disk.pku.edu.cn:443/link/3CED82219DA600FA892DEB2CE9D0D1C0)
