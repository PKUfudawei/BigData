# Final Project: Titanic - Machine Learning from Disaster

作者: 付大为	学号: 2201110122

# 背景

泰坦尼克号的沉没是历史上最臭名昭著的海难之一。

1912 年 4 月 15 日，在处女航期间，被广泛认为“永不沉没”的皇家邮轮泰坦尼克号在与冰山相撞后沉没。不幸的是，船上的每个人都没有足够的救生艇，导致 2224 名乘客和船员中的 1502 人死亡。

虽然幸存有一些运气因素，但似乎有些人比其他人更有可能活下来。

在这个挑战中，我们要建立一个预测模型来回答这个问题：“什么样的人更有可能生存？” 使用乘客数据（即姓名、年龄、性别、社会经济阶层等）。

# 数据集

## 下载地址

本次project用到的数据集来自kaggle的[Titanic](https://www.kaggle.com/competitions/titanic/overview)竞赛, 下载地址[见此](https://www.kaggle.com/competitions/titanic/data). 我已经把整个数据放在附件`data.zip`文件中

## 描述

在本次比赛中，我们有两个相似的数据集，其中包括姓名、年龄、性别、社会经济阶层等乘客信息。一个数据集名为 `train.csv`，另一个数据集名为`test.csv`。

`train.csv`将包含机上部分乘客（准确地说是 891 人）的详细信息，重要的是，将揭示他们是否幸存，也称为“基本事实”。

`test.csv`数据集包含类似的信息，但没有透露每位乘客的“基本事实”。预测这些结果是我们接下来的工作。

使用您在数据中找到的训练集`train.csv`，预测机上其他 418 名乘客（在 中找到`test.csv`）是否幸存。

## 变量解释

|    变量     |              定义               |                      key                       |
| :---------: | :-----------------------------: | :--------------------------------------------: |
| PassengerId |             乘客ID              |                                                |
|  Survived   |              生存               |                   0=否, 1=是                   |
|   Pclass    |            机票等级             |          1 = 第一，2 = 第二，3 = 第三          |
|    Name     |              姓名               |                                                |
|     Sex     |              性别               |                                                |
|     Age     |       以岁数为单位的年龄        |                                                |
|    SibSp    | 泰坦尼克号上的兄弟姐妹/配偶数量 |                                                |
|    Parch    |    登上泰坦尼克号的父母/孩子    |                                                |
|   Ticket    |              票号               |                                                |
|    Fare     |            旅客票价             |                                                |
|    Cabin    |             客舱号              |                                                |
|  Embarked   |            登船港口             | C = Cherbourg, Q = Queenstown, S = Southampton |

**Pclass**：社会经济地位（SES）的代称
1st = 上层
2nd = 中产
3rd = 底层

**Age**：如果年龄小于 1，则年龄为小数。如果年龄是估计的，则采用 xx.5 的形式

**sibsp**：数据集以这种方式定义家庭关系...
Sibling = 兄弟，姐妹，继兄，继妹
Spouse = 丈夫，妻子（情妇和未婚夫被忽略）

**Parch** : 数据集以这种方式定义家庭关系...
Parent = 母亲、父亲
Child =女儿、儿子、继女、继子
有些孩子只和保姆一起旅行，因此对他们来说 Parch=0。

# 算法选择

我们将选择并比较以下三种算法的结果

1. Logistic Regression
2. Random Forest
3. Xgboost

# 代码大纲

## 0. 加载数据集-训练集和测试集

导入第三方库并读取样本数据: 

```python
import pandas as pd
df_train = pd.read_csv('./data/train.csv')
df_test = pd.read_csv('./data/test.csv')
```

## 1. 数据清洗——填写“Age”、“Cabin”和“Embarked”中的缺失值

### 1.1 对于Age，我们知道上救生艇时“女士和孩子优先”的基本原则，所以我们相信年龄、性别和生存有着内在的联系。

在**训练集**中，我们按 (Sex, Survived) 对训练数据进行分组，并通过从相应的 (Sex, Survived) 组中使用bootstrap重采样方法来填充年龄的缺失值

```python
import random

age = {
    'male': {
        1: df_train['Age'][(df_train['Survived']==1) & (df_train['Sex']=='male') & ~df_train['Age'].isnull()].values,
        0: df_train['Age'][(df_train['Survived']==0) & (df_train['Sex']=='male') & ~df_train['Age'].isnull()].values
    },
    'female': {
        1: df_train['Age'][(df_train['Survived']==1) & (df_train['Sex']=='female') & ~df_train['Age'].isnull()].values,
        0: df_train['Age'][(df_train['Survived']==0) & (df_train['Sex']=='female') & ~df_train['Age'].isnull()].values
    }
}

for i in df_train['Age'][df_train['Age'].isnull()].index:
    df_train['Age'][i] = random.choice(age[df_train['Sex'][i]][df_train['Survived'][i]])
```

在**测试集**中，我们将测试数据按性别分组，并用**训练集**中同性别组的平均值填充年龄的缺失值

```python
mean_age = {
    sex: df_train['Age'][df_train['Sex']==sex].mean() for sex in df_train['Sex'].unique()
}
for i, v in df_test['Age'][df_test['Age'].isnull()].items():
    df_test['Age'][i] = mean_age[df_test['Sex'][i]]
```

### 1.2 对于Cabin，因为大多数值都被遗漏了，我们决定使用-1来填充**训练集**和**测试集**的所有遗漏值

在**训练集**中

```python
df_train.fillna({'Cabin': -1}, inplace=True)
```

在**测试集**中

```python
df_test.fillna({'Cabin': -1}, inplace=True)
```

### 1.3 对于 Embarked，只遗漏了两个值，所以使用 bootstrap 非常直接有效

在**训练集**中，我们通过对**训练集**使用bootstrap重采样来填充缺失值

```python
embarked = df_train['Embarked'][~df_train['Embarked'].isnull()].values
for i in df_train['Embarked'][df_train['Embarked'].isnull()].index:
    df_train['Embarked'][i] = random.choice(embarked)
```

在**测试集**中，我们仍然通过bootstrap重采样**训练集**来填充缺失值

```python
for i in df_test['Embarked'][df_test['Embarked'].isnull()].index:
    df_test['Embarked'][i] = random.choice(embarked)
```

### 1.4 额外填充测试集中缺失的*Fare*值

我们使用Pclass相同组的**训练集**的*Fare*平均值进行填充

```python
for i in df_test['Fare'][df_test['Fare'].isnull()].index:
    df_test['Fare'][i] = df_test['Fare'][df_test['Pclass']==df_test['Pclass'][i]].mean()
```

## 2. 分离特征和目标

从**训练集**和**测试集**中提取features和targets如下

```python
df_train_features, y_train = df_train.drop(['PassengerId', 'Survived', 'Name', 'Ticket'], axis=1), df_train['Survived'].values
df_test_features = df_test.drop(['PassengerId', 'Name', 'Ticket'], axis=1)
```

## 3. 数据预处理——数值型特征缩放和分类型特征编码

### 3.1 数值型特征缩放：标准化（也称为“Z-Score Normalization”）

**训练集**中, 首先可视化数值型特征的关联矩阵

```python
import plotly.express as px
import os

fig = px.imshow(df_train_features.corr().round(3), text_auto=True)
fig.show()
if not os.path.exists('./plots'):
    os.mkdir('./plots')
fig.write_image('./plots/train_numerical_corr.pdf')
```

得到的可视化结果如下

![train_numerical_corr](https://p.ipic.vip/0y2bu6.png)

然后对数值型变量使用z-normalization操作: $$z=\frac{x-\bar{x}}{\sigma_x}$$

```python
from sklearn.preprocessing import StandardScaler

z_scaler = StandardScaler()
numerical_train = df_train[[f for f in df_train_features.corr().columns]].values
numerical_train = z_scaler.fit_transform(numerical_train) 
```

**测试集**中, 也首先可视化数值型特征的关联矩阵

```python
fig = px.imshow(df_test_features.corr().round(3), text_auto=True)
fig.show()
if not os.path.exists('./plots'):
    os.mkdir('./plots')
fig.write_image('./plots/test_numerical_corr.png')
```

得到的可视化结果如下

![test_numerical_corr](https://p.ipic.vip/j0c144.png)

然后对数值型变量使用z-normalization操作: $$z=\frac{x-\bar{x}}{\sigma_x}$$

```python
z_scaler = StandardScaler()
numerical_test = df_test[[f for f in df_test_features.corr().columns]].values
numerical_test = z_scaler.fit_transform(numerical_test)
```

随后随着Tree Number上升进入饱和状态, 在Tree Number>60后甚至Accuracy略微下降, 可以认为是模型过大出现了过拟合现象.

### 3.2 分类特征编码——使用 OneHotEncoder

对于Cabin，我们只关心船舱的首字母

- **训练集**中

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder()
for i, v in df_train_features['Cabin'].items():
    if isinstance(v, str):
        df_train_features['Cabin'][i] = v[0]
    else:
        df_train_features['Cabin'][i] = str(v)
categorical_train = df_train_features[['Sex', 'Cabin', 'Embarked']].values
categorical_train_encoding = encoder.fit_transform(categorical_train).toarray()
```

- **测试集**中

```python
for i, v in df_test_features['Cabin'].items():
    if isinstance(v, str):
        df_test_features['Cabin'][i] = v[0]
    else:
        df_test_features['Cabin'][i] = str(v)
categorical_test = df_test_features[['Sex', 'Cabin', 'Embarked']].values
categorical_test_encoding = encoder.transform(categorical_test).toarray()
```

## 4. 构造和连接训练变量

```python
import numpy as np

X_train = np.concatenate([numerical_train, categorical_train_encoding], axis=1)
X_test = np.concatenate([numerical_test, categorical_test_encoding], axis=1)
```

其中**训练集**分类结果`y_train`已在前面求出

## 5. 模型训练和预测输出

我们为三种算法的实现提供统一的函数负责训练和预测, 如下

```python
model = {}
y_predict = {}

def train_and_predict(model_name, classifier):
    model[model_name] = classifier
    model[model_name].fit(X_train, y_train)
    y_predict[model_name] = model[model_name].predict(X_test)
    df_test['Survived'] = y_predict[model_name]
    output = df_test[['PassengerId', 'Survived']]
    if not os.path.exists('./submission'):
        os.mkdir('./submission')
    output.to_csv(f'./submission/{model_name}.csv', index=False, header=True)
```

### 5.1 Logistic Regression 模型

```python
from sklearn.linear_model import LogisticRegression

train_and_predict(model_name='logistic', classifier=LogisticRegression())
```

### 5.2 Random Forest 模型

```python
from sklearn.ensemble import RandomForestClassifier

train_and_predict(model_name='randomForest', classifier=RandomForestClassifier())
```

### 5.3 Xgboost 模型

```python
import xgboost as xgb

train_and_predict(model_name='xgboost', classifier=xgb.XGBClassifier())
```

我们将三种模型的结果提交到kaggle进行检验, 得到**测试集**上准确率结果如下

![16991686856121_.pic](https://p.ipic.vip/7dwnpb.jpg)

# 结果分析

我们可以看到随机森林(Random Forest)的准确率比Logistic Regression模型准确率略高, 这也说明随机森林模型通过多个随机决策树投票的方式减小了模型variance, 即减小了过拟合度, 从而在**测试集**上达到了更好的效果.

而Xgboost模型比前两个模型在**测试集**上的效果都要差, 可能是因为**训练集**的数据量还不够大, 对于Xgboost算法来说是欠拟合状态, 从而难以于前两个算法学习的结果相比较.

# 代码实现

代码具体实现见附件`final.ipynb`文件中.

# 提交结果

见附件`submission.zip`文件
