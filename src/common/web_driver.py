#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import sys
import selenium
import selenium.webdriver.support.ui as ui
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from src.common.config_parser import GetConfig
from src.common.logger import logger
import time


class WebDrive:
    def __init__(self, url, TIMEOUT = 5):
        self.url = url
        self.TIMEOUT = TIMEOUT
        self.drive = selenium.webdriver.Chrome()
        self.open_url()

    def open_url(self):
        count = 1
        while count <= self.TIMEOUT:
            try:
                self.drive.delete_all_cookies()
                self.drive.get(self.url)
                self.drive.maximize_window()
                logger.info('open url %s success !' % self.url)
                break
            except Exception as e:
                logger.error('login fail =>' + e.message)
            self.drive.close()
            self.drive.implicitly_wait(10)
            count += 1

    def action_cmd(self, web_name, action_name, method, param=None, find_try_time=None):
        xpath = GetConfig("web_xpath.cfg").get_item(web_name, action_name)
        func_name = "action_" + method
        try:
            func = getattr(self, func_name)
        except AttributeError:
            logger.error('No method named : %s found !' % func_name)
        msg = "%s %s %s %s" % (action_name, xpath, method, param)
        logger.info(msg)
        res = func(xpath, param, find_try_time)
        return res

    def action_input(self, xapth, param, find_try_time):
        try:
            obj = self.find_element_by_xpath(xapth, find_try_time)
            obj.clear()
        except Exception as e:
            logger.error(str(xapth)+ "unable to find element")
        return obj.send_keys(param)

    def action_click(self, xapth, param, find_try_time):
        try:
            obj = self.find_element_by_xpath(xapth, find_try_time)
        except Exception as e:
            logger.error(str(xapth)+ "unable to find element")
        return obj.click()

    def find_element_by_xpath(self, xpath, find_try_time):
        try:
            element = self.drive.find_element_by_xpath(xpath)
        except Exception as e:
            element = None
        return element

