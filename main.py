#!/usr/bin python
# -*- coding:utf-8 -*-
# @Author: Tongtong Song(TJU)
# @Data: 2020/11/15
# Last Update Time: 2020/11/22 16:40
# @Others: For 大数据分析理论与算法
# @File: main.py

import time
import os
from selenium import webdriver

import pandas as pd
from pandas import DataFrame

from src.utils import init_logger, get_Chorme_Option, Exist_or_Make_Dir
from src.get_into_page import get_Into_Main_Page, get_Into_Cate_Page, \
    get_Into_School_Cate_Page, get_Into_School_Page, get_Into_Class_Page, \
    get_Into_User_Page
from src.file_processing import Merge
from src.map import Draw_Map

if __name__ == '__main__':
    data_dir = 'data'
    log_dir = 'log'
    picture_dir = 'picture'

    Exist_or_Make_Dir(data_dir)
    Exist_or_Make_Dir(log_dir)
    Exist_or_Make_Dir(picture_dir)
    # 创建logger
    cur_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
    log_file_path = os.path.join(log_dir, 'spider_log' + cur_time + '.txt')
    logger = init_logger(log_file=log_file_path)

    # 获取chorme
    chrome_options = get_Chorme_Option()

    # 获取课程类有关信息
    # 参数配置
    main_url = 'https://www.icourse163.org'

    class_cate_col_name = '类名'
    class_cate_url_col_name = '链接'
    school_page_url = main_url + '/university/view/all.htm'
    categroys = ['计算机', '外语', '理学',
                 '工学', '经济管理', '心理学', '文史哲',
                 '艺术设计', '医药卫生', '教育教学',
                 '法学', '农林园艺', '音乐与舞蹈']
    driver = webdriver.Chrome(options=chrome_options)
    # 进入主界面，获取课程类对应链接
    class_cate_url_xlsx_file = os.path.join(data_dir, 'class_cate_url.xlsx')
    class_cate_url_dict = get_Into_Main_Page(logger, main_url, categroys, driver)
    DataFrame(class_cate_url_dict).to_excel(class_cate_url_xlsx_file, index=False)
    # 进入课程类界面，获取课程有关信息
    cate_xlsx_file = os.path.join(data_dir, 'cate.xlsx')
    class_xlsx_file = os.path.join(data_dir, 'class.xlsx')
    class_cate_url_dict = pd.read_excel(class_cate_url_xlsx_file).to_dict()
    class_cate_name_list = list(class_cate_url_dict[class_cate_col_name].values())
    class_cate_url_list = list(class_cate_url_dict[class_cate_url_col_name].values())
    cate_dict, class_dict = get_Into_Cate_Page(logger, class_cate_name_list,
                                               class_cate_url_list, driver)
    DataFrame(cate_dict).to_excel(cate_xlsx_file, index=False)
    DataFrame(class_dict).to_excel(class_xlsx_file, index=False)
    driver.close()
    driver.quit()

    # 获取课程，评论，学生的具体信息
    driver = webdriver.Chrome(options=chrome_options)
    # 获取学校目录界面，获取学校界面链接
    school_url_xlsx_file = os.path.join(data_dir, 'school_url.xlsx')
    school_dict = get_Into_School_Cate_Page(logger, school_page_url, driver,
                                            add_front=main_url)
    DataFrame(school_dict).to_excel(school_url_xlsx_file, index=False)

    # 进入学校界面,获取课程链接
    class_info_with_url_xlsx_file = os.path.join(data_dir, 'class_info_with_url.xlsx')
    school_dict = pd.read_excel(school_url_xlsx_file).to_dict()
    class_dict = get_Into_School_Page(logger, school_dict, driver)
    DataFrame(class_dict).to_excel(class_info_with_url_xlsx_file, index=False)

    # 进入课程界面，获取课程信息及用户链接
    # 参数配置

    class_info_with_url_xlsx_file = 'data/class_info_with_url.xlsx'
    student_num_col_name = '上课人数'
    class_url_col_name = '课程链接'
    class_col_name = '课程名'
    top_k = 10
    find_flag = 2
    # 0 只查找课程评分及评分及评论数信息，get_Into_Class_Page返回class_condiction_dict
    # 1 0基础上查找学生链接信息
    # 2 1基础上查找评论信息
    class_dict = pd.read_excel(class_info_with_url_xlsx_file).to_dict()
    student_num_dict = class_dict[student_num_col_name]
    sorted_idx_list = sorted(student_num_dict,
                             key=student_num_dict.__getitem__, reverse=True)
    start_idx = 0
    k = 2
    if top_k == 0:
        top_k = len(sorted_idx_list)
    while True:  # 每次查找并保存k个数据
        end_idx = start_idx + k
        if end_idx > top_k:
            end_idx = top_k
        idx_list = sorted_idx_list[start_idx:end_idx]
        file_end_str = str(start_idx) + '_' + str(end_idx)
        class_info_with_score_xlsx_file = os.path.join(data_dir,
                                                       'class_info_with_score' + file_end_str + '.xlsx')
        if find_flag >0:
            user_url_xlsx_file = os.path.join(data_dir, 'user_url' + file_end_str + '.xlsx')
            if find_flag >1:
                comment_xlsx_file = os.path.join(data_dir, 'comment' + file_end_str + '.xlsx')

        class_url_list = [list(class_dict[class_url_col_name].values())[idx] for idx in idx_list]
        class_list = [list(class_dict[class_col_name].values())[idx] for idx in idx_list]
        driver = webdriver.Chrome(options=chrome_options)
        if find_flag>1:
            class_condiction_dict, user_url_dict, comment_dict = \
                get_Into_Class_Page(logger, class_list, class_url_list, driver, find_flag)
        elif find_flag >0:
            class_condiction_dict, user_url_dict = \
                get_Into_Class_Page(logger, class_list, class_url_list, driver, find_flag)
        else:
            class_condiction_dict = \
                get_Into_Class_Page(logger, class_list, class_url_list, driver, find_flag)
        DataFrame(class_condiction_dict).to_excel(class_info_with_score_xlsx_file, index=False)
        if find_flag >0:
            DataFrame(user_url_dict).to_excel(user_url_xlsx_file, index=False)
            if find_flag >1:
                DataFrame(comment_dict).to_excel(comment_xlsx_file, index=False)
        driver.close()
        driver.quit()
        start_idx = end_idx
        if end_idx == top_k:
            break

    class_info_with_score_all_xlsx_file = os.path.join(data_dir, 'class_info_with_score_all.xlsx')
    Merge(dir=data_dir, file_keyword='class_info_with_score', save_path=class_info_with_score_all_xlsx_file)
    if find_flag >0:
        user_url_all_xlsx_file = os.path.join(data_dir, 'user_url_all.xlsx')
        Merge(dir=data_dir, file_keyword='user_url', save_path=user_url_all_xlsx_file)
        if find_flag >1:
            comment_all_xlsx_file = os.path.join(data_dir, 'comment_all.xlsx')
            Merge(dir=data_dir, file_keyword='comment', save_path=comment_all_xlsx_file)
    if find_flag > 0:
        # 进入个人界面，获取个人信息
        user_url_all_xlsx_file = os.path.join(data_dir, 'user_url_all.xlsx')
        user_url_col_name = '个人链接'
        user_url_dict = pd.read_excel(user_url_all_xlsx_file).to_dict()
        user_url_list = list(user_url_dict[user_url_col_name].values())
        length = 4000  # 由于每获取一次信息需要访问一个界面，因此在进行超过4000个数据爬取时，建议分批多机进行数据爬取，否则，可能会出现访问错误
        start_idx = 0
        k = 2000
        while True:  # 每次查找并保存k个数据
            end_idx = start_idx + k
            if end_idx > length:
                end_idx = length
            file_end_str = str(start_idx) + '_' + str(end_idx)
            user_info_xlsx_file = os.path.join(data_dir, 'user_info_' + file_end_str + '.xlsx')
            driver = webdriver.Chrome(options=chrome_options)
            user_info_dict = get_Into_User_Page(logger, user_url_list[start_idx:end_idx], driver)

            DataFrame(user_info_dict).to_excel(user_info_xlsx_file, index=False)
            driver.close()
            driver.quit()
            start_idx = end_idx
            if end_idx == length:
                break
        user_info_save_path = os.path.join(data_dir, 'user_info_all.xlsx')
        Merge(dir=data_dir, file_keyword='user_info', save_path=user_info_save_path)

        user_info_save_path = 'data/user_info_all.xlsx'
        Draw_Map(picture_dir, 'data/class_info_with_url.xlsx', user_info_save_path)
