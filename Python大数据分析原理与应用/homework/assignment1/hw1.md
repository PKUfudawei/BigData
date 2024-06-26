# Assignment 1

作者: 付大为	学号: 2201110122

## 1. 读取患者的检查样本数据，并补全缺失数据（均值填充即可），之后划分训练样本和测试样本，搭建逻辑回归模型，并计算在测试集上预测的准确率。

导入第三方库并读取样本数据:

```python
import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split

df = pd.read_csv('./breast_cancer.csv')
```

补全缺失数据(均值填充):

```python
df.fillna({k: df.mean(skipna=True)[k] for k in df.columns if df[k].isnull().any()}, inplace=True)
```

获取feature数据与label数据, 分别记为X和y:

```python
X = df.iloc[:, :-1].values
y = df.iloc[:, -1].values
```

按照80% : 20%比例划分训练样本和测试样本:

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

搭建逻辑回归模型:

```python
model = linear_model.LogisticRegression()
```

拿训练集进行拟合:

```python
model.fit(X_train, y_train)
```

计算在测试集上预测的准确率:

```python
y_predict = model.predict(X_test)
print(accuracy_score(y_true=y_test, y_pred=y_predict))
# 0.956140350877193
```

## 2.  计算测试集上预测结果的混淆矩阵

计算测试集上的混淆矩阵:

```python
cm = confusion_matrix(y_true=y_test, y_pred=y_predict)
pd.DataFrame(data={'预测不患癌症': cm[:, 0], '预测患癌症': cm[:, 1]}, index=['实际患癌症', '实际不患癌症'])
```

结果如下

![image-20230420223636652](/Users/DaweiFu/Library/Application Support/typora-user-images/image-20230420223636652.png)

## 3.  输出逻辑回归模型的参数k0-k30，对每一个**测试样本**计算对应的 y 和 f(y) 值，画出 y 与 f(y) 的散点图，其中正样本以红色表示，负样本以蓝色表示。（正/负样本指数据集中的真实正/负样本）

$$
y=k_0+k_1x_1+k_2x_2+\cdots+k_{30}x_{30}\\f(y)=\frac{1}{1+e^{-y}}
$$

首先查看fitting后的model参数

```python
print('k_0:', model.intercept_)
print('k_1 ~ k_30:', model.coef_)
```

![15811682001796_.pic](https://p.ipic.vip/mj221r.jpg)

然后在测试集上计算 y 和 f(y)

```python
y = np.dot(X_test, model.coef_.reshape(-1))
f_y = 1 / (1 + np.exp(-y))
```

接下来准备可视化

```python
df_scatter = pd.DataFrame({'y': y, 'f(y)': f_y, 'label': ['positive' if label==1 else 'negative' for label in y_test]})
```

我选择用第三方库plotly画图

```python
import plotly.express as px
fig = px.scatter(df_scatter, x="y", y="f(y)", color='label', color_discrete_sequence=['red', 'blue'])
fig.update_traces(marker=dict(size=5))
fig.show()
fig.write_image('./scatter.pdf')
```

$$


$$
