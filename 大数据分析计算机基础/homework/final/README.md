# 项目说明: 中国历代人物传记资料库分析

### 小组成员: 付大为、田源

- 数据库下载地址: [latest.7z](https://github.com/cbdb-project/cbdb_sqlite/blob/master/latest.7z)
- 已下载好的数据库位置`latest.db`
- 题目概述: 下载Harvard University的[CBDB](https://projects.iq.harvard.edu/cbdb)数据库，结合网络上各种文献，分析该数据库结构，各个字段（属性）含义。可在地图上显示多人迁移路径，人际关系等多种应用。至少达到如下目标：

## 逐题解决

### 0. 读取数据库(SQLite格式)

- 这里我们采用了python中的`sqlite3`库作为读取SQLite格式的方式, 然后将其中的上百个表转化为**parquet**(二进制)格式和**csv**(字符串)格式, **parquet**格式便于程序快速读取和处理, **csv**格式便于我们直接查阅.
- 具体执行文件参考`database_to_tables.py`
- 转出的**parquet**文件位于`./parquet/`目录下, 转出的**csv**文件位于`./tables/`目录下

### 1. 数据库设计，尤其是表间关系；

- 在了解数据库之前先要知道什么是[主键和外键](https://www.cnblogs.com/PyLearn/p/7624768.html)

- 要了解数据库设计中表间关系的定义, 请参考[数据库表与表的关系](https://blog.csdn.net/weixin_44176169/article/details/104069544)
- 为了获取上百个表的相互关系, 我们要利用`pandas`库读取各个表的信息, 然后获取每个表的主键信息, 并探测该主键是否在其他表中扮演外键且是否是其他表的主键, 以此分别是**一对一**还是**一对多**关系
- 为了判断**多对多**关系, 我们可以看作两个**一对多**关系通过[复合主键或组合主键](https://blog.csdn.net/u011781521/article/details/71083112)的中间表联合起来形成**多对多**关系, 为此, 我们先找到这样只包含两个字段的表作为可能的中间表, 再在前面搜寻到的**一对多**关系与中间表匹配, 发现出存在若干**多对多**关系
- 具体执行文件参考`table_relationship.py`
- 上百个表的表间关系有数百个组合, 我们储存在了`表间关系.csv`文件中国, 为了更好地可视化, 我们利用第三方库`networkx`画出表间关系的网络图, 并且以绿色边表示一对一, 蓝色边表示一对多, 红色边表示多对多, 该可视图位于`./images/表间关系.pdf`

### 2. 数据库所有字段的含义；

- 利用第三方库`pandas`从CBDB的参考资料`cbdb_codebook.xlsx`中把xlsx格式读取为dataframe, 然后逐表记录字段含义, 再利用`pd.concat`函数拼接起来, 把结果储存到`./字段含义.csv`文件中
- 具体执行文件参考`field_meaning.py`

### 3. 探索中国历史人物如何数据化，以及数据如何存储，要求以案例说明；

- 这要求我们理解中国历史人物是如何被量化并且被记录进表格的
- 这里我们以`c_personid`为人物唯一标识, 查询以该键为主键的表格, 即可认为是历史人物信息相关表格. 结合`./字段含义.csv`文件, 并且把每个相关表格内的字段及其字段含义取得, 并且记录下该字段属于哪个表格, 最后把结果储存进`./人物字段.csv`文件
- 具体执行文件参考`historical_person_fields.py`
- 以韩愈为例进行案例说明:
  - **c_personid**: 3332
  - **是否为女性**: 0(否)
  - **指数年**: 768
  - **郡望**: 南阳
  - **享年**: 58
  - **社会区分**: 书法家、诗人、文人、工于文
  - ......

### 4. 历史人物的维度，以及每个维度的各朝代数量分布；

- 维度1: 从历史人物相关字段中得到历史人物姓氏数量分布, 并结合中国地图生成词云, 数据储存到`./姓氏排名.csv`中, 生成词云图储存到`./images/姓氏词云.jpg`中
- 维度2: 按照各朝代统计不同性别的历史人物数量, 生成图片储存到`./images/各朝代不同性别历史人物数量.pdf`中
- 维度3: 按照各朝代统计不同性别的历史人物平均寿命, 生成图片储存到`./images/各朝代不同性别历史人物平均寿命.pdf`中
- 维度4: 统计历史人物出生月份, 生成图片储存到`./images/出生月份.pdf`中
- 这里为了实习可视化我们利用了第三方库`wordcloud`和交互式画图库`plotly`, 具体执行文件参考`historical_person_dimension.py`

### 5. 在地图上呈现多个历史人物的迁移关系；

- 为了避免迁移路线过于密集, 我们每次只显示一个人物的迁移路线图, 并通过输入`c_personid`值指定查询哪个历史人物 (如苏轼为3767)
- 我们仍然利用`pandas`, `matplotlib`和`networkx`库来实现对迁移路线的地理网络图分析, 和执行可视化部分, 根据c_personid为索引画出相关人物的生平迁移路线图, 不以姓名为索引是因为繁体且可能重名. 并且将结果储存为`./images/{历史人物名}迁移路线.jpg`, 比如已经产生的结果为`./images/蘇軾迁移路线.jpg`
- 具体执行文件参考`historical_person_migration.py`

### 6. 可对某个专题深入分析，比如：隋唐时期的门阀政治、西晋门阀政治的区别等等；

- 这里我们选取的专题是**历史人物学术社交关系网络图分析**, 并且, 为了将其与[六度分隔理论](https://www.wikiwand.com/zh-hans/%E5%85%AD%E5%BA%A6%E5%88%86%E9%9A%94%E7%90%86%E8%AE%BA)结合起来研究, 我们特意从初始人物出发, 往外扩展到他的第七度人际关系, 以此研究六度分割理论的正确性
- 我们仍然利用`pandas`, `matplotlib`和`networkx`库实现对社交网络的分析以及漂亮的可视化, 并且为了区分每一度的人际关系, 将网络的边依据第几度赋予不同的颜色, 具体如下:
  - 第一度: 红色
  - 第二度: 绿色
  - 第三度: 暗橙色
  - 第四度: 紫色
  - 第五度: 暗灰色
  - 第六度: 粉色
  - 第七度: 青色
- 具体执行文件参考`association_network.py`
- 用到的迭代分析函数是`iter_association(personids, network, edge_color, assoc_type: str='03')`, 它的功能是迭代寻找第n度社交关系, 其中assoc_type=='03'表示寻找的是学术相关社交关系.
- 可视化部分函数是`plot_assocation_network(graph, name)`, 这里, 我们根据社交关系网络图, 利用Fruchterman-Reingold力导向算法定位节点, 该算法模拟网络的力导向表示, 将边视为使节点靠近的弹簧, 同时将节点视为互斥对象, 也被称为排斥引力, 模拟一直持续到位置接近平衡, 使得节点分布尽量四散均匀, 提高美观度. 同时我们将网络中的主要历史人物 (定义为节点连接数大于1/3最大节点连接数的节点) 的名字在节点中显示出来, 增强可读性
- 以朱熹为例, 输出的结果储存到`./images/朱熹七度社交关系网络图.pdf`, 在该图中我们可以看到青色的代表第七度关系的边远少于前面几度关系的边数, 这告诉我们, 六度分割理论在统计上具有一定的正确性, 说明大于七度的社交关系数是极少的. 但是六度分割理论显然不是一个数学严谨的理论 (比如刚出生的婴儿的社交关系路径一定等于父母的社交关系路径+1, 显然有可能大于六度), 图中会出现青色的代表第七度社交关系的边也说明了这一点.



