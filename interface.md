
# 说明文档


总的来说，要输入的数据集为  txt文件 包含应用id 时间  点击次数  应用类别
     时间、点击次数、应用类别 会进入som  data参与训练
     输入 txt文件名  data
     输入 names list  names 各个特征描述

     要设置的参数 训练步数
     反馈  返回Topographic error  Quantization error

     设置 2D图像文件名

     设置 类数 n_clusters
     反馈 聚类评估  Calinski-Harabasz分数值

     获取hitmap  设置文件名

     获取聚类txt  设置文件名
## Mysm类
### 属性介绍
```
data  #数据集 numpy数组类型  时间、点击次数、应用类别 直接包含个特征值
names  #各个特征描述 Python list类型 例如 time clickcnt ID 
initialization='random' #初始方式选择 有 'random' 和 'pac'
train_rough_len=2 #训练步长 
train_finetune_len=5  #训练步长
view2D='view2D' #2D图形文件名 (.png)
n_clusters=4  #聚类数量
hitmap='hitmap' #hitmap图形文件名(.png)
outfile='out' #输出文件名(.txt)
```
    
*接口介绍*
- easytest 快速启动
- set_train_len  设置训练步长  train_rough_len    、 train_finetune_len
- set_view2D_name 设置输出2D图形文件名（png文件）
- set_n_clusters  设置 聚类数量
- set_hitmap_name  设置 输出hitmap图形文件名（png文件）
- set_outfile_name  设置 最终结果文件名(txt文件)
- build  建立SOM模型
- train  训练模型
- get_error  获取训练误差
- get_view2D  获取2D图形
- cluster   聚类
- Clu_assessment  获取聚类评价
- get_result    获取结果(txt文件)
- get_hitmap    获取hitmap图形



## 评价 
不像监督学习的分类问题和回归问题，我们的无监督聚类没有样本输出，也就没有比较直接的聚类评估方法。但是我们可以从簇内的稠密程度和簇间的离散程度来评估聚类的效果。常见的方法有轮廓系数Silhouette Coefficient和Calinski-Harabasz Index。个人比较喜欢Calinski-Harabasz Index，这个计算简单直接，得到的Calinski-Harabasz分数值ss越大则聚类效果越好。

Calinski-Harabasz分数值ss的数学计算公式是：
```
    s(k)=tr(Bk)tr(Wk)m−kk−1
    s(k)=tr(Bk)tr(Wk)m−kk−1
```
其中m为训练集样本数，k为类别数。BkBk为类别之间的协方差矩阵，WkWk为类别内部数据的协方差矩阵。trtr为矩阵的迹。
也就是说，类别内部数据的协方差越小越好，类别之间的协方差越大越好，这样的Calinski-Harabasz分数会高。在scikit-learn中， Calinski-Harabasz Index对应的方法是metrics.calinski_harabaz_score.