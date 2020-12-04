#!/usr/bin python
# -*- coding:utf-8 -*-
# @Author: Tongtong Song(TJU)
# @Data: 2020/11/15
# Last Update Time: 2020/11/20/ 20：57
# @Others: For 大数据分析理论与算法
# @File: src/utils.py


from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import logging
import time
import os

def get_Chorme_Option():
    chrome_options = Options()
    # 设置chrome浏览器无界面模式
    chrome_options.add_argument('lang=zh_CN.UTF-8')  # 设置中文
    chrome_options.add_argument('--disable-gpu')  # 规避bug
    chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
    # 设置手机请求头 （手机页面反爬虫能力稍弱）
    chrome_options.add_argument(
        'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/74.0.3729.157 Mobile Safari/537.36')

    return chrome_options


def init_logger(log_file=None):
    # 日志组件初始化
    log_format = logging.Formatter("[%(asctime)s %(levelname)s] %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.handlers = [console_handler]

    if log_file and log_file != '':
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    return logger


def filter_digit(string):
    # 过滤字符串中的数字
    return "".join(list(filter(str.isdigit, string)))


def get_Into_Page(url, driver):
    # 进入界面获取界面源码
    driver.get(url)
    time.sleep(0.1)
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    return driver


def get_Soup(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if not soup:
        # 如果没有获取到界面信息，则再让页面加载5s
        time.sleep(5)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup


def Exist_or_Make_Dir(dir):
    #
    if not os.path.exists(dir):
        os.mkdir(dir)

