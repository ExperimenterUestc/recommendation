毕业设计
电影推荐系统
随着互联网与移动互联网迅速普及，网络上的电影娱乐信息数量相当庞大，人们对获取感兴趣的电影娱乐信息的需求越来越大，个性化的电影推荐系统成为一个热门。推荐模块中使用了更切合实际的电影相似度计算方法，结合协同过滤算法基于用户与基于物品的过滤算法，有效的解决了系统的冷启动问题和推荐的准确性问题，推荐算法使用集中平均法来预测用户对电影的评分，避免了用户个人评分习惯对预测评分产生的不利影响。
1.数据由movie_lens和imdb获取
2.算法为基于用户和物品相结合的协同过滤算法
3.采用杰卡德相似和余弦相似度，考虑流行度，长尾效应
4.在django搭建的网站上予以实现。
