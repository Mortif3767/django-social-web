### 基于Django的用户图片分享社交网站  
  
#### 网站主要功能  
  
**1.用户认证：** 用户注册、登录、编辑个人资料`profile`，修改以及重置密码。  
**2.用户社交：** 用户之间关注系统。  
**3.图片分享：** 用户可从互联网引用照片分享到网站，使用 **`Redis`** 存储图片浏览量。  
**4.用户动态：** 创建活动流`actions`应用，记录显示用户行为，例如：分享照片，关注用户等。  
  
#### 网站功能实现  
  
**`account`应用**  
1.使用django内置`authentication`框架中的操作视图函数实现：**登录、退出、修改密码、密码重置**等功能。  
2.建立视图函数实现**注册**`views.register`功能，扩展`django authentication`框架中的`User model`，建立`Profile model`，实现**编辑个人资料**功能`views.edit`。  
3.通过中间表`Contact`建立`User`模型多对多关系，实现用户关注`follower`与被关注`followed`关系。  
  
**`images`应用**  
1.建立`Image model`，创建`ImageCreateForm`表单，定义`clean_url`方法，确保图片分享url合法，覆写`save`方法，从互联网下载照片。  
2.使用`sorl-thumbnail`缩略图显示。  
3.使用 **`Redis`** 存储视图函数中图片浏览量，并生成图片浏览排行`views.image_ranking`。  
  
**`actions`应用**   
建立`Action model`，定义属性`user`：操作用户，`verb`：字符串存储行为，添加**通用关系**`target`：目标对象。  

**其他**  
1.尝试增加额外数据冗余优化读取性能，使用`Image model`额外字段`total_likes`优化聚合函数计算照片总喜欢量，在`images`应用中添加信号接收函数`signals.user_like_changed`，保持冗余数据更新。  
2.使用messages框架，实现消息提醒。  
  
```
|- django-social-web
    |- account\     #app
    |- images\      #app
    |- actions\     #app
    |- bookmarks\   #subject
    #...
```
