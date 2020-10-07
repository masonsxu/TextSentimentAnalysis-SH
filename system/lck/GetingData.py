from datetime import date, timedelta
from urllib import parse
from selenium import webdriver  # selenum库的使用需要提前安装对应的浏览器驱动
import pandas as pd
import numpy as np
import requests
import json
from json import loads
import time
import re


class GetingData:

    qq_account = None
    qq_password = None
    driver = None
    headers = {'host': 'h5.qzone.qq.com',
               'accept-encoding': 'gzip, deflate, br',
               'accept-language': 'zh-CN,zh;q=0.8',
               'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                             '59.0.3071.115 Safari/537.36',
               'connection': 'keep-alive'}
    # 设置爬取内容保存路径
    s = './system/lck/Users.csv'
    place = []
    data = []

    def get_key_values(self, body, key, end=';'):
        """提取body中不包括的key，分片操作

        :param body: 父字符串
        :param key: 子字符串
        :param end: 结束字符串，默认为;
        :return: 不包括子字符串的字符串
        """
        return body[body.find(key) + len(key): body.find(';', body.find(key))]


    def get_key(self,cookies):
        """获取cookie中的相关键的值
        解密
        :param cookies: 缓存
        :return: 相关键的值
        """
        key = self.get_key_values(cookies, 'p_skey=')
        h = 5381
        for i in key:
            h += (h << 5) + ord(i)
        return h & 2147483647


    def web_login_cookie(self,flag):
        """url = 'https://user.qzone.qq.com/QQ号相关的缓存
        实现自动化登录

        :return: 浏览器的缓存
        """

        self.login(self.driver, self.qq_account, self.qq_password, flag)
        time.sleep(10)
        self.driver.get('https://user.qzone.qq.com/{}'.format(self.qq_account))
        cookie = ''
        for elem in self.driver.get_cookies():  # 记录相关的Cookie
            # elem 为 dict类型
            cookie += elem["name"] + "=" + elem["value"] + ";"
        # cookies = cookie
        return cookie


    def login(self,driver, qq_account, qq_password, flag):
        """登录

        :param driver: 浏览器对象
        :param qq_account: QQ账号
        :param qq_password: QQ密码
        :return:
        """

        # 解决窗口最大化问题
        if flag == 0:
            driver.maximize_window()
        driver.get('http://user.qzone.qq.com')
        driver.switch_to.frame('login_frame')
        time.sleep(1)
        driver.find_element_by_id("switcher_plogin").click()
        driver.find_element_by_id("u").clear()
        driver.find_element_by_id("u").send_keys(qq_account)
        time.sleep(2)
        driver.find_element_by_id("p").clear()
        driver.find_element_by_id("p").send_keys(qq_password)
        time.sleep(2)
        driver.find_element_by_id("login_button").click()


    def send_requests(self,req, headers, url, params=None):
        """url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?'
        rd，g_t，qzonetoken（每次登录都发生变化，从Cookiezz中获取）
        :param req: 请求（Request）,该请求为会话
        :param headers: 请求头
        :param params: 请求参数
        :return: JSONP数据
        """
        if None != params:
            url = url + parse.urlencode(params)
        # url = url+'&offset='+str(0)
        page = req.get(url=url, headers=headers)
        return page.text


    # 控制日期格式
    def data_format(self,s):
        s = s.replace('年', '-').replace('月', '-').replace('日', '')
        if '昨天' in s:
            s = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        if '前天' in s:
            s = (date.today() + timedelta(days=-2)).strftime("%Y-%m-%d")
        if ':' in s:
                s = date.today().strftime("%Y-%m-%d")
        return s


    # 爬取好友位置
    def crawl_place(self):
        """

        :return: palace
        """
        print("开始爬取好友位置信息")
        cookie = self.web_login_cookie(0)
        g_tk = self.get_key(cookie)
        qzonetoken_friend = self.get_key_values(cookie, 'ptcz=')
        uin_friend = self.get_key_values(cookie, 'ptui_loginuin=')
        rd_friend = self.get_key_values(cookie, '_qpsvr_localtk=')
        self.headers['Cookie'] = cookie
        params_friend = {"uin": uin_friend, "fupdate": 1, "action": 1, "do": 1, "g_tk": g_tk, "rd": rd_friend,
                         'qzonetoken': qzonetoken_friend}
        url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?'
        req = requests.session()
        data_friend_str = self.send_requests(req, self.headers, url_friend, params=params_friend)
        data_friend_dict = loads(data_friend_str[0 + len('_Callback('):data_friend_str.find(');')])
        # print('data_friend_dict: ', data_friend_dict)

        # code = -3000 message = '请先登录'
        if data_friend_dict['code'] != 0:
            time.sleep(10)
            self.crawl_place()
        else:
            data_friend_list = list(data_friend_dict['data']['items_list'])
            for i in range(len(data_friend_list)):
                each_uin = data_friend_list[i]['uin']
                each_url = 'https://h5.qzone.qq.com/proxy/domain/base.qzone.qq.com/cgi-bin/user/cgi_userinfo_get_all?'
                params_each = {"uin": each_uin, "fupdate": 1, "vuin": uin_friend, "g_tk": g_tk, "rd": rd_friend,
                               'qzonetoken': qzonetoken_friend}
                time.sleep(1)
                data_each_str = self.send_requests(req, self.headers, each_url, params_each)
                try:
                    data_each_dict = loads(data_each_str[0 + len("_Callback("):data_each_str.find(");")])
                    dicts = data_each_dict.get('data')
                    if dicts != None:
                        pl = {'QQnum': str(dicts['uin']), 'country': dicts['country'], 'province': dicts['province'],
                              'city': dicts['city']}
                        self.place.append(pl)
                except json.decoder.JSONDecodeError as e:
                    continue
        print("位置信息爬取结束")


    # 爬取好友动态
    def crawl_info(self):
        print("开始爬取好友动态信息")
        cookie = self.web_login_cookie(1)
        g_tk = self.get_key(cookie)
        qzonetoken_friend = self.get_key_values(cookie, 'ptcz=')
        self.driver.get(
            'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_hat_get.cgi?hat_seed=1&uin=' + self.qq_account + 'fupdate=1&g_tk=' + str(
                g_tk) + '&qzonetoken=' + str(qzonetoken_friend) + '&g_tk=' + str(g_tk))
        friend_list = self.driver.page_source
        friend_list = str(friend_list)

        abtract_pattern = re.compile('\"(.\d*)\":\{\\n"realname":"(.*?)"}', re.S)
        QQ_name_list = re.findall(abtract_pattern, str(friend_list))  # 数组

        numList = dict()  # numList => (QQnum:QQname)  #列表

        for i in QQ_name_list:
            numList[str(i[0])] = str(i[1])

        last_source = ""
        tag = 1

        # print(numList)

        for key in numList.keys():
            QQnum = key
            QQname = numList[QQnum]

            if QQnum != "":  # 根据qq号查找好友说说（条件）
                count = 1
                begin = 0
                while tag == 1:

                    # -------------进入好友说说页面
                    # print("Begin:"+str(begin))
                    self.driver.get(
                        'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=' + QQnum + '&ftype=0&sort=0&pos=' + str(
                            begin) + '&num=40&replynum=200&g_tk=' + str(
                            g_tk) + '&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken=' + str(
                            qzonetoken_friend) + '&g_tk=' + str(g_tk))

                    try:
                        msg_list_json = self.driver.page_source
                    except:
                        begin = begin + 40
                        continue

                    msg_list_json = str(msg_list_json)
                    if last_source == msg_list_json:
                        break
                    else:
                        last_source = msg_list_json

                    # 检测是否没有权限访问
                    # print(msg_list_json)
                    abtract_pattern = re.compile(',"message":"(.*?)","name":', re.S)
                    message = re.findall(abtract_pattern, str(msg_list_json))
                    if message != []:
                        if str(message[0]) == '对不起,主人设置了保密,您没有权限查看':
                            break

                    # print(msg_list_json)
                    # 解析JSON
                    # webDriver没有现成的JSON解析器，所以采用获取源码的方式，然后使用正则表达式获取具体细节
                    msg_list_json = msg_list_json.split("msglist")[1]  # 拆分json，缩小范围，也能加快解析速度
                    msg_list_json = msg_list_json.split("smoothpolicy")[0]
                    msg_list_json = msg_list_json.split("commentlist")[1:]

                    # 只考虑含有文字信息的说说动态：1、文字说说（或带有配图的文字说说）
                    #              2、转发的说说：
                    #                   （1）配文字
                    #                   （2）不配文字

                    for text in msg_list_json:

                        # 1、先检查说说，用户是否发送了文字，如果没有文字，正则表达式匹配无效
                        abtract_pattern = re.compile(
                            '\}\],"content":"(.*?)","createTime":"(.*?)","created_time":(.*?),"', re.S)
                        msg_time = re.findall(abtract_pattern, str(text))

                        if msg_time != []:
                            # 2、如果作者说说有文字，那么检查是否有转发内容
                            abtract_pattern = re.compile("[\u4e00-\u9fa5]+", re.S)
                            msg = re.findall(abtract_pattern, str(msg_time[0][0]))
                            msg = "".join(msg)
                            sendTime = str(msg_time[0][1])

                            abtract_pattern = re.compile('\}\],"content":"(.*?)"},"rt_createTime":"(.*?)","', re.S)
                            text = text.split("created_time")[1]
                            msg_time2 = re.findall(abtract_pattern, str(text))

                            # 合并发送内容 格式：评论+转发内容
                            if msg_time2 != []:
                                # 只爬取中文文字信息
                                abtract_pattern = re.compile("[\u4e00-\u9fa5]+", re.S)
                                s = re.findall(abtract_pattern, str(msg_time[0][0]))
                                s = "".join(s)
                                msg = msg + "  转发内容:" + s

                        else:
                            # 3、说说内容为空，检查是否为 =>只有图片的说说 or 转发，不配文字
                            # 获取正文发送时间 （发送时间分为：正文发送时间 or 转发时间）
                            abtract_pattern = re.compile('"conlist":null,"content":"","createTime":"(.*?)",', re.S)
                            msgNull_time = re.findall(abtract_pattern, str(text))

                            if msgNull_time != []:
                                continue
                            else:
                                # 如果没有正文发送时间，那么就是说这条说为 =>转发，不配文字
                                abtract_pattern = re.compile('\}\],"content":"(.*?)"},"rt_createTime":"(.*?)","', re.S)
                                msg_time = re.findall(abtract_pattern, str(text))

                                abtract_pattern = re.compile("[\u4e00-\u9fa5]+", re.S)
                                s = re.findall(abtract_pattern, str(msg_time[0][0]))
                                s = "".join(s)

                                msg = "  转发内容:" + s
                                sendTime = str(msg_time[0][1])
                        # 写入本地文件
                        for p in self.place:
                            # 过滤掉动态为空和没有位置信息的数据
                            if str(QQnum) == p['QQnum'] and msg != "" and p['country'] == '中国' and p['province'] != '':
                                tdata = [str(QQnum), str(QQname), self.data_format(sendTime), str(p['country']),str(p['province']), str(p['city']), msg]
                                self.data.append(tdata)

                        count = count + 1

                    begin = begin + 40

    def __init__(self, qq_account, qq_password):
        self.qq_account = qq_account
        self.qq_password = qq_password
        self.driver = webdriver.Chrome()
        self.crawl_place()
        # print(place)
        self.crawl_info()
        self.driver.close()
        print('开始保存数据')
        data = np.asarray(self.data)
        data_Sheet = pd.DataFrame(data, columns=['number', 'name', 'date', 'country', 'province', 'city', 'message'])
        data_Sheet.to_csv(self.s, index=False, encoding='utf_8_sig')
        print('数据保存结束')

# 测试
# getData = GettingData('3578654497','19991211.qwe')