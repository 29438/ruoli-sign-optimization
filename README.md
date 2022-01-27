📃免责声明

本项目为Python学习交流的开源非营利项目，仅作为程序员之间相互学习交流之用，使用需严格遵守开源许可协议。严禁用于商业用途，禁止使用本项目进行任何盈利活动。对一切非法使用所产生的后果，我们概不负责。本项目对您如有困扰请联系我们删除。

📗使用方法

🔑常规部署

安装Python3.6+环境

下载并解压项目代码包

修改config.yml文件中的相关配置内容

运行以下命令安装项目依赖
```
pip install -r requirements.txt -t ./ -i https://mirrors.aliyun.com/pypi/simple
```

执行 Python index.py 即可运行项目

🚀快速部署

Linux环境可以直接使用下方命令一键部署

```
curl -sSO https://raw.fastgit.org/29438/ruoli-sign-optimization/master/actions/setup.sh && bash setup.sh
```

📅示例 腾讯云函数平台

打开百度搜索腾讯云函数，注册认证后，进入控制台。

点左边的函数服务，新建云函数，名称随意，运行环境选择python3.6，创建方式选择自定义创建

在高级配置中配置执行超时时间60秒，在触发器配置中选择自定义创建，触发周期选择自定义触发，配置cron表达式

如需每日上午0点执行可使用该表达式
0 0 0 * * * *
如需每日上午8点30分执行可使用该表达式
0 30 8 * * * *
如需每日中午12点执行可使用该表达式
0 0 12 * * * *
点击完成，不要关闭页面等待创建完成后，选择立即跳转

点击函数代码选项卡，等待编辑器初始化完成

在编辑器上方的菜单栏中，选择终端>新终端，将下方命令粘贴到弹出的终端中并回车，等待初始化环境完成，可能需要较长时间，请耐心等待(如长时间没反应可以按下CTRL+C键强制终止，然后再次尝试)

```
curl -sSO https://raw.fastgit.org/29438/ruoli-sign-optimization/master/actions/setup.sh && bash setup.sh
```

在编辑器左边的src目录下选择config.yml，配置你的用户签到信息，注意删除多余的示例并注意每行行首的缩进

最后，点击下方的部署即可完成部署(部署完成后，你可以点击测试按钮测试签到任务)

📢 公告

* 2022-1-27更新，秘钥升级
* 2021-11-7更新，配置文件有修改(<u>请**删掉**配置中不需要用到的**可选项**</u>，不然会出现"今日校园版本过旧，请更新")
* 2021-12-16更新，[pushplus](https://pushplus.hxtrip.com/index)使用方式更新，需要重新配置
* 发现bug记得提交issue

🛠 修改摘要

### 整体修改

- [x] 完善推送
- [x] 签到失败自动重试
- [x] 响应的json解析优化
- [x] 签到坐标随机偏移

------

- [x] 日志组件优化
- [x] 本地运行时保存执行日志

------

- [x] DeviceID通过用户名伪随机生成
- [ ] UA随机生成
- [x] 随机签到时间延迟

------

- [x] 政工签到

### autosign.py修改

- [x] 签到任务Title匹配
- [x] ismalposition参数本地判定
- [x] 支持签到已请假任务
- [x] 获取以往签到任务自动填写表单

### collection.py修改

- [x] 支持非必填项的填写，以及不填写必填项
- [x] 支持图片类型收集(图片位置填在value中)
  (感谢[1216332750](https://github.com/1216332750)在issues中提供的代码参考)
- [ ] 获取以往签到任务自动填写表单

## 用户配置高级教程

配置文件遵从[yaml](https://www.runoob.com/w3cnote/yaml-intro.html)语法。

单用户配置大致长这样

```yaml
  - type: 
    schoolName: 
    username: ""
    password: ""
    checkTitle: 
    forms: 
      - form:
          title: 
          value: 
    lon: 104.616858
    lat: 28.793022
    address:
    photo: 
```

### 获取历史签到信息

目前（仅签到任务）支持获取上次填报的表单、位置信息进行填报。（会忽略配置问卷中已有的表单和位置信息）

> 获取上次提交图片的功能还未经测试，如果遇到bug请反馈

可以通过添加```getHistorySign```项启动这个功能。

```yaml
  - type: 
    schoolName: 
    username: ""
    password: ""
    getHistorySign: True # 获取历史表单功能启动
```

### 时间格式

形如下的题目

> 9.最后核酸检测时间(日期时间)
> 题目规则:最早1900-01-01;最晚2099-12-31

其时间格式如下

```yaml
      - form:
          title: 
          value: "2001-01-01" # 一定要有引号(字符串)，否则会被识别为时间对象
```

如有其他时间格式，**按照表单中时间框中预览的格式填入**即可。

### 地点格式

地点的分隔符一般是```/```

```yaml
  - form:
      title: 
      value: "xx省/xxx/xxx/xxx" # 有些是xx/xx/xx
```

### 图片

查寝、政工签到都有```  photo```可填项。可以填入一个本地图片的位置（绝对/相对都可以）。

信息收集如果有图片收集，则可以作为问题答案填入```value```中。

> 备注：图片最好是.jpg格式

------

当填入一个列表的时候，会随机选取其中一项。

```yaml
    photo:
      - "图片文件夹"
      - "图片.jpg"
      - "图片2.jpg"
```

当填入一个字符串地址时，就以此地址寻找图片

```yaml
    photo: "图片.jpg"
```

或者

```yaml
    photo: "图片文件夹"
```

------

最终选取到的地址会进行判断：

* 如果地址指向一个文件，就会上传此文件。
* 如果地址指向一个文件夹，就会随机从中选取一个```.jpg```结尾的文件

### 代理

在用户配置中，配置```proxy```参数可以使用代理。

```yaml
  - type: 
    schoolName: 
    username: ""
    password: ""
    checkTitle: 
    forms: 
      - form:
          title: 
          value: 
    lon: 104.616858
    lat: 28.793022
    address:
    photo: 
    proxy: "http://host:port" # 注意缩进要和username、password等参数保持一致
```

代理请以```http://```或```https://```为开头。常见的形式有

* ```http://用户名:密码@123.123.123.123:1234```
* ```http://123.123.123.123:1234```

### 单独推送

用户配置中可以添加```sendMessage```推送仅该用户的签到情况，格式同整体推送（不需要的选项可以删掉）。

```yaml
  - type: 
    schoolName: 
    username: ""
    password: ""
    checkTitle: 
    forms: 
      - form:
          title: 
          value: 
    lon: 104.616858
    lat: 28.793022
    address:
    photo: 
    sendMessage:
      rl_emailApiUrl: http://mail.ruoli.cc/api/sendMail # 邮箱API的地址(不需要推送不用填)
      rl_email: "" # email 接受通知消息的邮箱(不需要推送不用填)
      qmsg_key: "" # qmsg推送的key(不需要推送不用填)
      qmsg_qq: "" # qmsg推送的qq号(不需要推送不用填)
      qmsg_isGroup: 0 # 此qq号是否为群(是的话填1，反之为0)
      pushplus_parameters: "" # pushplus参数，填入令牌即可推送。也可以填入"token=xxx&topic=xxx"形式自定义更多参数(注册pushplus请前往https://pushplus.hxtrip.com/index)
      smtp_host: "smtp.qq.com" # SMTP服务器域名
      smtp_user: "*****@qq.com" # SMTP服务器用户名
      smtp_key: "" # SMTP服务器密钥
      smtp_sender: "*****@qq.com" # 发送邮箱
      smtp_receivers:
        - "*****@qq.com" # 接收邮箱(可填多个)
```













# 警告：以下内容可能已经过时了

## 常见问题

* 如果在日志发现HTTP 418(I'm a teapot.)，意为被怀疑为爬虫脚本。
* 如果在模拟登录后开始抓取任务列表时HTTP 405(请求方式错误)

> Carlton大佬:
>
> ​	发生在cas登录时：
>
> ​	405是因为取辅导猫表单时候 发现没有登录态 302回你学校了
>
> ​	离谱就是，302回你学校cas服务以后他是登录的，又给你302回调回来了，302肯定是get，所以返回405

## 使用方法

### 第一步

登录腾讯云，进入腾讯云函数https://console.cloud.tencent.com/scf/list

### 第二步

选择一个**非广州的内陆节点**(比如上海、北京、成都)

![image-20210808213157826](README.assets/image-20210808213157826.png)

### 第三步

点击 **新建**

![image-20210808213307298](README.assets/image-20210808213307298.png)

### 第四步

选择自定义创建

选择本地上传文件夹

![image-20210808213511227](README.assets/image-20210808213511227.png)

然后上传文件夹

![image-20210808213748344](README.assets/image-20210808213748344.png)

### 第五步

触发器选择 **自定义创建**

触发周期选择 **自定义触发周期**

Cron表达式填```15 0,8 * * *```(意思是每天0点和8点15分触发)

最后点 **完成**

![image-20210808214224780](README.assets/image-20210808214224780.png)

### 第六步

自动跳转到函数管理，进入函数配置

点击**编辑**

将**执行超时时间**设置为100秒

最后**保存**

![image-20210808214408055](README.assets/image-20210808214408055.png)

![image-20210808214524063](README.assets/image-20210808214524063.png)

![image-20210808214601868](README.assets/image-20210808214601868.png)

### 第七步

进入 **函数代码**

进入**config.yml**

将依照config.yml里的注释，**将自己的配置信息填入config.yml**

![image-20210808214956680](README.assets/image-20210808214956680.png)

### 第八步

点击 **终端-新终端**

在终端中**输入**```pip3 install -r ./src/requirements.txt -t ./src/ -i https://mirrors.aliyun.com/pypi/simple```

**按回车**，然后**等待执行完毕**

执行完毕后，点击**部署**，并**等待部署完毕**

**大 功 告 成**，第二天看看自动签到是否成功吧。(如果没成功，去询问别人为什么失败的时候一定要截图日志最后那一页)

![image-20210808214914963](README.assets/image-20210808214914963.png)

![image-20210808215316573](README.assets/image-20210808215316573.png)

![image-20210808215517157](README.assets/image-20210808215517157.png)

