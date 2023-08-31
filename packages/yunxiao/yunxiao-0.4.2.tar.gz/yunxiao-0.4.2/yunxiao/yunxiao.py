import configparser
from datetime import datetime, timedelta
import logging

import requests
import time
from requests import utils
import os

config = configparser.ConfigParser()


class Time:

    # 时间戳
    stamp_s = int(time.time())
    stamp_ms = int(time.time() * 1000)

    # 日
    _today_ = datetime.today()
    today = _today_.date().strftime("%Y-%m-%d")
    yesterday = (_today_.date() - timedelta(days=1)).strftime("%Y-%m-%d")
    tomorrow = (_today_.date() + timedelta(days=1)).strftime("%Y-%m-%d")

    # 周
    _this_week_monday_ = (_today_.date() - timedelta(days=_today_.weekday()))
    this_week_monday = _this_week_monday_.strftime("%Y-%m-%d")
    this_week_sunday = (_this_week_monday_ + timedelta(days=6)).strftime("%Y-%m-%d")
    last_week_monday = (_this_week_monday_ - timedelta(days=7)).strftime("%Y-%m-%d")
    last_week_sunday = (_this_week_monday_ - timedelta(days=1)).strftime("%Y-%m-%d")
    next_week_monday = (_this_week_monday_ + timedelta(days=7)).strftime("%Y-%m-%d")
    next_week_sunday = (_this_week_monday_ + timedelta(days=13)).strftime("%Y-%m-%d")

    # 月
    _this_month_start_ = _today_.replace(day=1)
    _next_month_start_ = _this_month_start_.replace(
        year=_today_.year + 1, month=1) if _today_.month == 12 else _this_month_start_.replace(month=_today_.month + 1)
    this_month_start = _this_month_start_.date().strftime("%Y-%m-%d")
    this_month_end = (_next_month_start_ - timedelta(days=1)).date().strftime("%Y-%m-%d")

    _last_month_ = _today_.replace(year=_today_.year - 1, month=12) if _today_.month == 1 else _today_.replace(
        month=_today_.month - 1)
    last_month_start = _last_month_.replace(day=1).date().strftime("%Y-%m-%d")
    last_month_end = (_today_.replace(day=1) - timedelta(days=1)).date().strftime("%Y-%m-%d")

    # 年
    this_year_start = _today_.replace(month=1, day=1).date().strftime("%Y-%m-%d")
    this_year_end = _today_.replace(month=12, day=31).date().strftime("%Y-%m-%d")
    last_year_start = _today_.replace(year=_today_.year - 1, month=1, day=1).date().strftime("%Y-%m-%d")
    last_year_end = _today_.replace(year=_today_.year - 1, month=12, day=31).date().strftime("%Y-%m-%d")


class YunXiao:

    def __init__(self, configfile: str = "yunxiao_config.ini"):

        self.configfile = configfile

        # 如果没有初始化配置文件，抛出异常并终止程序
        if not os.path.exists(self.configfile):
            config['AUTH'] = {
                'phone': 'your_phone',
                'password': 'your_password',
                'token': '',
                'cookie': ''
            }
            with open(configfile, 'w') as f:
                config.write(f)
            logging.error(f"请访问 {configfile} 配置你的用户名和密码。")
            raise Exception("未初始化配置文件。请访问 {configfile} 配置你的用户名和密码。")

        # 读取配置文件
        config.read(self.configfile)
        self.token = config['AUTH']['token']
        self.cookie = config['AUTH']['cookie']
        self.user = config['AUTH']['phone']
        self.pwd = config['AUTH']['password']

        # 未填写配置时
        if self.user == "your_phone" or self.pwd == "your_password":
            logging.error(f"请访问 {configfile} 配置你的用户名和密码。")
            raise Exception("未初始化配置文件。请访问 {configfile} 配置你的用户名和密码。")

        # 初始化 token：为空则刷新一次。
        if not self.token:
            self.renew_token()

        # 初始化 cooke：为空则刷新一次。
        if not self.cookie:
            self.renew_cookie()

    # 刷新 token
    def renew_token(self):
        """
        刷新 token.tmp 配置中存储的 token
        """
        mid_token = requests.post(
            url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/loginByPhonePwd",
            json={
                "_t_": Time.stamp_ms,
                "password": self.pwd,
                "phone": self.user,
                "userType": 1
            }
        ).json()["data"]["token"]

        token = requests.get(
            url="https://yunxiao.xiaogj.com/api/cs-crm/teacher/businessLogin",
            headers={"x3-authentication": mid_token},
            params={"_t_": Time.stamp_ms}
        ).json()["data"]["token"]

        config.read(self.configfile)
        config['AUTH']['token'] = token
        self.token = token
        with open(self.configfile, 'w') as f:
            config.write(f)

        logging.info("成功刷新 YUNXIAO_OAUTH_TOKEN")

    # 刷新 cookie
    def renew_cookie(self):
        """
        刷新 cookie.tmp 配置中存储的 cookie
        """
        # logging.debug("开始刷新 Cookie")
        res = requests.post(
            url="https://yunxiao.xiaogj.com/api/ua/login/password",
            params={
                "productCode": 1,
                "terminalType": 2,
                "userType": 1,
                "channel": "undefined"
            },
            json={
                "_t_": Time.stamp_ms,
                "clientId": "x3_prd",
                "password": self.pwd,
                "username": self.user,
                "redirectUri": "https://yunxiao.xiaogj.com/web/teacher/#/home/0",
                "errUri": "https://yunxiao.xiaogj.com/web/simple/#/login-error"
            },
            allow_redirects=False
        )
        res1 = requests.Session().get(
            url=res.json()["data"],
            cookies=res.cookies,
            allow_redirects=False
        )

        cookie1 = "UASESSIONID=" + requests.utils.dict_from_cookiejar(res.cookies)["UASESSIONID"]
        cookie2 = "SCSESSIONID=" + requests.utils.dict_from_cookiejar(res1.cookies)["SCSESSIONID"]
        headers = {"cookie": cookie1 + "; " + cookie2}

        res2 = requests.Session().get(
            url=res1.headers["location"],
            headers=headers,
            allow_redirects=False
        )

        res3 = requests.Session().get(
            url=res2.headers["location"],
            headers=headers,
            allow_redirects=False
        )

        cookie3 = "SCSESSIONID=" + requests.utils.dict_from_cookiejar(res3.cookies)["SCSESSIONID"]

        cookie = cookie1 + "; " + cookie3

        config.read(self.configfile)
        config['AUTH']['cookie'] = cookie
        self.cookie = cookie
        with open(self.configfile, 'w') as f:
            config.write(f)

        logging.info("成功刷新 YUNXIAO_OAUTH_COOKIE")