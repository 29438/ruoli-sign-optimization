import traceback
import os
from todayLoginService import TodayLoginService
from actions.autoSign import AutoSign
from actions.collection import Collection
from actions.sleepCheck import sleepCheck
from actions.workLog import workLog
from actions.sendMessage import SendMessage
from actions.teacherSign import teacherSign
from login.Utils import Utils
from liteTools import *


def loadConfig():
    config = DT.loadYml('config.yml')
    # 全局配置初始化
    config['delay'] = tuple(config.get("delay", [5, 10]))

    # 用户配置初始化
    for user in config['users']:
        LL.log(1, f"正在初始化{user['username']}的配置")
        # 初始化静态配置项目
        defaultConfig = {
            'remarkName': '默认备注名',
            'state': None,
            'model': 'OPPO R11 Plus',
            'appVersion': '9.0.14',
            'systemVersion': '4.4.4',
            'systemName': 'android',
            "signVersion": "first_v3",
            "calVersion": "firstv",
            'getHistorySign': False
        }
        defaultConfig.update(user)
        user.update(defaultConfig)

        # 用户设备ID
        user['deviceId'] = user.get(
            'deviceId', RT.genDeviceID(user.get('schoolName', '')+user.get('username', '')))

        # 用户代理
        user['proxy'] = user.get('proxy')
        requestsProxies = dict()
        if not user['proxy']:  # 如果用户代理设置为空，则不设置代理。
            requestsProxies = dict()
        elif type(user['proxy']) == str:
            if "http://" in user['proxy'][0:7]:
                requestsProxies['http'] = user['proxy']
            elif "https://" == user['proxy'][0:8]:
                requestsProxies['https'] = user['proxy']
            else:
                raise Exception("代理应以http://或https://为开头")
        elif type(user['proxy']) == dict:
            requestsProxies = user['proxy']
        user['proxy'] = requestsProxies

        # 坐标随机偏移
        user['global_locationOffsetRange'] = config['locationOffsetRange']
        if 'lon' in user and 'lat' in user:
            user['lon'], user['lat'] = RT.locationOffset(
                user['lon'], user['lat'], config['locationOffsetRange'])
    return config


def working(user):
    LL.log(1, '准备登录')
    today = TodayLoginService(user)
    today.login()
    LL.log(1, '登录完成')
    # 登陆成功，通过type判断当前属于 信息收集、签到、查寝
    # 信息收集
    if user['type'] == 0:
        # 以下代码是信息收集的代码
        LL.log(1, '即将开始信息收集填报')
        collection = Collection(today, user)
        collection.queryForm()
        collection.fillForm()
        msg = collection.submitForm()
        return msg
    elif user['type'] == 1:
        # 以下代码是签到的代码
        LL.log(1, '即将开始签到')
        sign = AutoSign(today, user)
        sign.getUnSignTask()
        sign.getDetailTask()
        sign.fillForm()
        msg = sign.submitForm()
        return msg
    elif user['type'] == 2:
        # 以下代码是查寝的代码
        LL.log(1, '即将开始查寝填报')
        check = sleepCheck(today, user)
        check.getUnSignedTasks()
        check.getDetailTask()
        check.fillForm()
        msg = check.submitForm()
        return msg
    elif user['type'] == 3:
        # 以下代码是工作日志的代码
        LL.log(1, '即将开始工作日志填报')
        work = workLog(today, user)
        work.checkHasLog()
        work.getFormsByWids()
        work.fillForms()
        msg = work.submitForms()
        return msg
    elif user['type'] == 4:
        # 以下代码是政工签到的代码
        LL.log(1, '即将开始政工签到填报')
        check = teacherSign(today, user)
        check.getUnSignedTasks()
        check.getDetailTask()
        check.fillForm()
        msg = check.submitForm()
        return msg
    else:
        raise Exception('任务类型出错，请检查您的user的type')


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))  # 将工作路径设置为脚本位置

    # 加载配置
    config = loadConfig()
    maxTry = config['maxTry']

    # 开始签到
    # 自动重试
    for tryTimes in range(1, maxTry+1):
        LL.log(1, '正在进行第%d轮尝试' % tryTimes)
        # 遍历用户
        for user in config['users']:
            # 检查是否已经在上一轮尝试中签到
            if type(user['state']) == str:
                continue
            LL.log(1, '即将在第%d轮尝试中为[%s]签到' % (tryTimes, user['username']))

            # 用户间随机延迟
            RT.randomSleep(config['delay'])

            try:
                msg = working(user)
            except TaskError as e:
                msg = str(e)
            except Exception as e:
                msg = str(e)
                LL.log(3, traceback.format_exc(), user['username']+'签到失败'+msg)
                if maxTry != tryTimes:
                    continue

            # 消息格式化
            msg = '--%s|%d\n--%s' % (user['username'], tryTimes, msg)
            user['state'] = msg
            LL.log(1, msg)
            # 消息推送
            sm = SendMessage(user.get('sendMessage'))
            sm.send(msg, '今日校园自动签到')
            LL.log(1, sm.log_str)

    # 签到情况推送
    msg = '==签到情况==\n'
    for i in config['users']:
        msg += '[%s]\n%s\n' % (i['remarkName'], i['state'])
    LL.log(1, msg)
    sm = SendMessage(config.get('sendMessage'))
    sm.send(msg+'\n'+LL.getLog(4), '自动健康打卡')
    LL.log(1, sm.log_str)


def handler(event, context):
    '''阿里云的入口函数'''
    main()


def main_handler(event, context):
    '''腾讯云的入口函数'''
    main()
    return 'ok'


if __name__ == '__main__':
    try:
        main()
    finally:
        LL.saveLog(DT.loadYml('config.yml').get('logDir'))  # 生成日志文件
