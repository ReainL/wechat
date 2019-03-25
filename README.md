## wechat
[![](https://img.shields.io/badge/python-3-brightgreen.svg)](https://www.python.org/downloads/)

微信好友男女比例，区域排名，签名情感分析

|    程序   | 备注 |技术栈|
|:-------------:|:-------------:|:-----:|
| [微信好友性别占比](https://github.com/ReainL/wechat#2微信好友性别占比)|采集微信好友性别比例并绘制饼图|itchat, matplotlib|
| [微信好友头像](https://github.com/ReainL/wechat#3微信好友头像)|采集微信好友头像并拼接大图|itchat, math, PIL|
| [微信好友地区分布](https://github.com/ReainL/wechat#4微信好友地区分布)|采集微信好友区域分布并分别制作省会和城市Top10柱形图 |itchat, matplotlib|
| [微信好友个性签名情感分析](https://github.com/ReainL/wechat#5微信好友个性签名情感分析)|采集微信性别比例并绘制饼图|itchat, matplotlib, jieba, numpy, snownlp, wordcloud|
| [微信群好友统计](https://github.com/ReainL/wechat#6微信群好友统计)|采集微信群好友信息|itchat, matplotlib, PIL|


#### [1、微信登录](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_login.py)
```python
import itchat

itchat.auto_login(hotReload=True)
itchat.dump_login_status()
we_friend = itchat.get_friends(update=True)[:]
```
- [wechat_login.py](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_login.py) 运行此文件即可登录

返回的结果`we_friend`是微信好友的基本信息列表, 单个好友字典的 key 如下表：

|    key   | 备注 |
|:-------------:|:-------------:|
|UserName|微信系统内的用户编码标识|
|NickName|好友昵称|
|Sex|性别|
|Province|省份|
|City|城市|
|HeadImgUrl|微信系统内的头像URL|
|RemarkName|好友的备注名|
|Signature|个性签名|

#### [2、微信好友性别占比](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_friend.py)
通过统计好友人数、男生女生各多少人算出好友性别占比，再绘制饼图。

![](https://github.com/ReainL/wechat/blob/master/res/%E5%BE%AE%E4%BF%A1%E5%A5%BD%E5%8F%8B%E6%80%A7%E5%88%AB%E6%AF%94%E4%BE%8B.png?raw=true)

#### [3、微信好友头像](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_photo.py)

- 首先需要把好友头像保存在同一[目录](https://github.com/ReainL/wechat/tree/master/res/photos)下

- 设定最后拼图的大小，以及每行需要拼接几个头像，这里我采用图片的面积除以图片的张数

```python
each_size = int(math.sqrt(float(640 * 640) / len(ls)))  # 算出每张图片的大小多少合适
lines = int(640 / each_size)
image = Image.new('RGBA', (640, 640))   # 创建640*640px的大图
```

![微信好友头像](https://github.com/ReainL/wechat/blob/master/res/%E5%A5%BD%E5%8F%8B%E5%A4%B4%E5%83%8F%E6%8B%BC%E6%8E%A5%E5%9B%BE.jpg?raw=true)



#### [4、微信好友地区分布](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_area.py)

- 由于地区太多，故使用Python sorted函数进行排序，对地区和城市Top10进行柱状图展示

![微信好友城市Top10](https://github.com/ReainL/wechat/blob/master/res/%E5%BE%AE%E4%BF%A1%E5%A5%BD%E5%8F%8B%E5%9F%8E%E5%B8%82Top10.png?raw=true)

![微信好友区域Top10](https://github.com/ReainL/wechat/blob/master/res/%E5%BE%AE%E4%BF%A1%E5%A5%BD%E5%8F%8B%E5%8C%BA%E5%9F%9FTop10.png?raw=true)

通过区域和城市人数排名，其实大致看出你的户籍所在地和工作地点了。


#### [5、微信好友个性签名情感分析](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_sign.py)

这里主要做了两部分

- 第一部分使用jieba分词对好友个性签名进行切词，并制作词云图，这里的词云图背景使用比较火的[小猪佩奇](https://upload-images.jianshu.io/upload_images/6078268-8796daa744519d40.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)


![好友个性签名词云图](https://github.com/ReainL/wechat/blob/master/res/%E5%A5%BD%E5%8F%8B%E4%B8%AA%E6%80%A7%E7%AD%BE%E5%90%8D%E8%AF%8D%E4%BA%91%E5%9B%BE.png?raw=true)


- 第二部分使用snownlp对好友的签名做一个简单的情感分析

![好友个性签名情感值分布](https://github.com/ReainL/wechat/blob/master/res/%E5%A5%BD%E5%8F%8B%E7%AD%BE%E5%90%8D%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90.png?raw=true)

通过饼图来推测我的好友大多数正向情感要高于负向情感。

#### [6、微信群好友统计](https://github.com/ReainL/wechat/blob/master/pro_script/wechat_group.py)

之前加了一个中产互助社群，群成员既有一线京沪广深、二线杭宁苏夏，成渝武郑，也有四五七八线地级市县以及国外的朋友，群里刚好讨论了一个话题《三到五年后离开北上广的有多少打算的》，借此机会统计下目前有多少在一线工作，3年后会再次统计一波

群聊用户列表的获取方法为`update_chatroom`。

- 同样，如果想要更新该群聊的其他信息也可以用该方法
- 群聊在首次获取中不会获取群聊的用户列表，所以需要调用该命令才能获取群聊的成员
- 该方法需要传入群聊的UserName，返回特定群聊的详细信息
- 同样也可以传入UserName组成的列表，那么相应的也会返回指定用户的最新信息组成的列表
```python
import itchat
memberList = itchat.update_chatroom('@@abcdefg1234567', detailedMember=True)
```

![中产之路2群(新)好友性别比例](https://upload-images.jianshu.io/upload_images/6078268-10e924e8cc04ab6c.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
![中产之路2群(新)群好友人数Top20](https://upload-images.jianshu.io/upload_images/6078268-3b6267fba80fc133.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

性别比例这里就不再提，群内好友人数分布从图片中可以清晰看到Top3是北京、上海、深圳，的确如此。对于普通人来说，大城市发展的机会、空间、市场、机遇、机会都会比小城市大的多。

###### 最后, 想一块合作做更多有趣好玩的项目,欢迎关注公众号：

![Python攻城狮](https://upload-images.jianshu.io/upload_images/6078268-b8cbed4d7ab16023.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)
