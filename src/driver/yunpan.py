#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.abspath(__file__ + "/../../../.."))
from src.common.config_parser import GetConfig
from src.common.logger import logger
from src.common.web_driver import WebDrive


class BaiDu:
    def __init__(self, webdrive, user_name, user_pwd):
        self.webdrive = webdrive
        self.user_name = user_name
        self.user_pwd = user_pwd

    def login(self):
        logger.info("<--------------- start login --------------->")
        user_name = self.user_name
        user_pwd = self.user_pwd
        self.webdrive.action_cmd("login_baidu", "login_click", "click")
        self.webdrive.action_cmd("login_baidu", "login_name", "input", user_name)
        self.webdrive.action_cmd("login_baidu", "login_pwd", "input", user_pwd)
        self.webdrive.action_cmd("login_baidu", "login_btn", "click")
        logger.info("<--------------- login success --------------->")


if __name__ == "__main__":
    url = GetConfig('web_info.cfg').get_item("lpf_info", "url")
    user_name = GetConfig('web_info.cfg').get_item("lpf_info", "name")
    user_pwd = GetConfig('web_info.cfg').get_item("lpf_info", "pwd")
    webdrive = WebDrive(url=url)
    Login = BaiDu(webdrive=webdrive, user_name=user_name, user_pwd=user_pwd)
    Login.login()
