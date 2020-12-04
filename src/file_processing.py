#!/usr/bin python
# -*- coding:utf-8 -*-
# @Author: Tongtong Song(TJU)
# @Data: 2020/11/15
# @Last Update Time: 2020/11/21 12:00
# @Others: For 大数据分析理论与算法
# @File: src/file_processing.py

import pandas as pd
import os


def Search_File(path, keyword):
    file_list = []
    for filename in os.listdir(path):
        fp = os.path.join(path, filename)
        if os.path.isfile(fp) and keyword in filename:
            file_list.append(fp)
        elif os.path.isdir(fp):
            Search_File(fp, keyword)
    return file_list


def Merge(dir,file_keyword,save_path,sort_col_name='',sheet_name='Sheet1'):
    file_list = Search_File(dir, file_keyword)
    print('合并%s到%s'%(','.join(file_list),save_path))
    if sort_col_name:
        print('按%s排序'%sort_col_name)
    # 合并数据
    merge_data=pd.ExcelFile(file_list[0]).parse(sheet_name)
    os.remove(file_list[0])
    for i in range(1,len(file_list)):
        current_data=pd.ExcelFile(file_list[i]).parse(sheet_name)
        merge_data=pd.concat([merge_data, current_data])
        os.remove(file_list[i])
    if sort_col_name:
        merge_data.sort_values(by=sort_col_name)
    merge_data.to_excel(save_path, index=False)
    print('合并成功')
