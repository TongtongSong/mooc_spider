#!/usr/bin python
# -*- coding:utf-8 -*-
# @Author: Tongtong Song(TJU)
# @Data: 2020/11/15
# @Last Update Time: 2020/11/22 16:45
# @Others: For 大数据分析理论与算法
# @File: src/get_into_page.py

import time
from selenium.webdriver.common.action_chains import ActionChains  # 模拟鼠标操作
from src.utils import get_Into_Page, get_Soup, filter_digit


def get_Into_Main_Page(logger, main_url, categroys, driver):
    # 启动Chrome
    class_cate_name_list = []
    class_cate_url_list = []
    logger.info('进入主界面')
    driver = get_Into_Page(main_url, driver)
    # 鼠标移动
    ele = driver.find_element_by_class_name('_6lpb5')
    ActionChains(driver).move_to_element(ele).perform()
    soup = get_Soup(driver)

    spans = soup.find_all(name='a', attrs={"rel": "noopener noreferrer",
                                           'target': '_blank'})
    for span in spans:
        class_cate_name = span.string
        class_cate_url = span['href']
        if class_cate_name in categroys and class_cate_url.endswith('.htm'):
            class_cate_name_list.append(class_cate_name)
            class_cate_url_list.append(class_cate_url)
            logger.info('获取到%s类的链接:%s' % (class_cate_name, class_cate_url))

    class_cate_dict = {
        '类名': class_cate_name_list,
        '链接': class_cate_url_list
    }
    return class_cate_dict


def get_Into_Cate_Page(logger, class_cate_name_list, class_cate_url_list, driver):
    """
    :param class_cate_name_list:
    :param class_cate_url_list:
    :param logger:
    :param class_cate_url_dict:
    :param driver:
    :return:
    """
    cate_class_num_list = []
    cate_student_num_list = []
    class_name_list = []
    class_type_list = []
    class_cate_list = []
    class_cat_name_list_store = []
    for idx, class_cate_url in enumerate(class_cate_url_list):
        driver = get_Into_Page(class_cate_url, driver)
        soup = get_Soup(driver)
        try:
            content = soup.find(class_='b_hjr')
            class_num_text = content.find(class_='Sdujj').span.string
            class_num = int("".join(list(filter(str.isdigit, class_num_text))))
            page_num = int(soup.find(class_='_2WoTy').find_all(class_='_20fst')[-1].string)
            student_num_total = 0

            for page_idx in range(page_num):
                class_condictions = soup.find_all(class_='_2mbYw')
                for class_condiction_session in class_condictions:
                    # 获取课程名
                    class_name = class_condiction_session.h3.string
                    try:
                        # 获取课程类别
                        try:
                            class_type = class_condiction_session.find(class_='H_ce0').string
                        except:
                            class_type = 'null'
                        # 获取学生数
                        student_num_text = class_condiction_session.find(class_='_3DcLu').string
                        student_num = int(filter_digit(student_num_text))
                        student_num_total += student_num
                        # 填写字典
                        class_name_list.append(class_name)
                        class_type_list.append(class_type)
                        class_cate_list.append(class_cate_name_list[idx])
                        logger.info(
                            '找到第%d课程:%s(正在查找%s类)' % (len(class_name_list),
                                                     class_name, class_cate_name_list[idx]))
                    except:
                        logger.info('%s课程查找失败' % class_name)
                if page_idx == page_num - 1:
                    break
                # 翻页
                ele = driver.find_element_by_partial_link_text('下一页')
                ele.click()
                time.sleep(0.1)
                soup = get_Soup(driver)
            class_cat_name_list_store.append(class_cate_name_list[idx])
            cate_class_num_list.append(class_num)
            cate_student_num_list.append(student_num_total)
        except:  # 有的页面回返回错误源代码，不进行接收
            logger.info('%s类课程查找失败' % class_cate_name_list[idx])

    cate_dict = {
        '类名': class_cat_name_list_store,
        '课程数': cate_class_num_list,
        '学生数': cate_student_num_list
    }

    class_dict = {
        '课名': class_name_list,
        '所属大类': class_cate_list,
        '类型': class_type_list
    }

    return cate_dict, class_dict


def get_Into_School_Cate_Page(logger, school_page_url, driver, add_front=''):
    """
    进入学校目录界面
    获取学校名和学校链接
    :param logger:
    :param school_page_url: 学校目录链接
    :param driver:
    :param add_front: 填写学校链接时填写在前面
    :return:
        dict: 学校链接字典，包含校名、学校链接
    """

    logger.info('进入学校目录页')
    driver = get_Into_Page(school_page_url, driver)
    soup = get_Soup(driver)

    soup = soup.find(id='g-body')  # 锁定内容
    school_contain_list = soup.find_all(name='a', class_='f-fl')
    count = 0
    school_name_list = []
    school_url_list = []
    for school_contain in school_contain_list:
        count += 1
        school_name = school_contain.img['alt']
        school_url = add_front + school_contain['href']
        school_name_list.append(school_name)
        school_url_list.append(school_url)
        logger.info('找到第%d个学校：%s,%s' % (count, school_name, school_url))

    dict = {
        '校名': school_name_list,
        '学校链接': school_url_list
    }
    return dict


def get_Into_School_Page(logger, school_dict, driver):
    """
    进入学校界面，获取学校相关信息
    :param logger:
    :param school_dict: 读取包含学校名和学校链接的字典
    :param driver:
    :return:
        dict: 课程信息字典，包含课程名、上课人数、课程链接、学校
    """
    school_list = list(school_dict['校名'].values())
    school_url_list = list(school_dict['学校链接'].values())
    total_school_num = len(school_list)
    class_url_list = []
    class_name_list = []
    class_student_num_list = []
    school_name_list = []
    for school_idx, school_name in enumerate(school_list):
        school_url = school_url_list[school_idx]
        driver = get_Into_Page(school_url, driver)
        soup = get_Soup(driver)
        soup = soup.find(id='g-body')
        while True:
            soup = soup.find(class_='m-upool', id='j-courses')  # 定位到课程区
            class_contents = soup.find_all(
                class_='u-courseCardWithTime-container')
            for class_content in class_contents:  # 遍历课程信息
                class_name = class_content.find(
                    class_='u-courseCardWithTime-teacher').text
                class_student_num = filter_digit(class_content.find(
                    class_='u-courseCardWithTime-people').text)
                if not class_student_num:
                    class_student_num = 0
                class_url = 'https:' + class_content['data-label']
                class_name_list.append(class_name)
                class_student_num_list.append(int(class_student_num))
                class_url_list.append(class_url)
                school_name_list.append(school_name)
                logger.info('已经找到%d门课(当前所查找学校:%s(%d/%d))' % (
                    len(class_url_list), school_name, school_idx + 1, total_school_num))
            if not soup.find(text='下一页'):  # 只有一页，获取当前页信息后立即退出
                break
            flag = soup.find(class_='js-disabled')
            if flag and flag.string == '下一页':  # 已经到最后一页
                break
            ele = driver.find_element_by_partial_link_text('下一页')
            ele.click()
            time.sleep(0.2)
            soup = get_Soup(driver)
            soup = soup.find(id='g-body')
    dict = {
        '课程名': class_name_list,
        '上课人数': class_student_num_list,
        '课程链接': class_url_list,
        '学校': school_name_list
    }
    return dict


def get_Into_Class_Page(logger, class_list, class_url_list, driver, find_flag=0):
    """
    进入课程界面，获取课程信息、根据评论获取学生昵称及链接、获取评论信息
    :param find_flag:
    :param logger:
    :param class_list: 课程名列表
    :param class_url_list: 课程链接列表
    :param driver:
    :return:
        class_condiction_dict: 课程信息字典，包含课程名、评论人数、评分
        user_urls_dict: 学生链接字典，包含昵称、个人链接
        comment_dict: 评论字典，包含昵称、课程、评论、打分
    """
    class_score_list = []
    comment_num_list = []
    if find_flag > 0:
        user_name_list = []
        user_url_list = []
        if find_flag > 1:
            class_name_list = []
            class_comment_list = []
            student_score_list = []

    total_class_num = len(class_list)
    index = []
    for class_idx, class_name in enumerate(class_list):
        class_name = class_name.strip()
        class_url = class_url_list[class_idx]
        driver = get_Into_Page(class_url, driver)

        # 点击课程评价
        ele = driver.find_element_by_id('review-tag-button')
        ele.click()
        soup = get_Soup(driver)
        comment_section = soup.find(id='comment-section')
        if comment_section.find(
                class_='ux-mooc-comment-course-comment_no-comment'):  # 没有评论
            comment_num = 0
        else:
            index.append(class_idx)
            try:
                comment_num = int(filter_digit(soup.find(id='review-tag-num').text))
            except:
                continue
        score = comment_section.find(
            class_="ux-mooc-comment-course-comment_head_rating-scores")
        if score:
            score = score.text
        else:
            score = -1

        comment_num_list.append(int(comment_num))
        class_score_list.append(float(score))
        if find_flag > 0 and comment_num > 0:
            while True:
                try:
                    comment_list_session = comment_section.find_all(
                        class_='ux-mooc-comment-course-comment_comment-list_item')
                    for comment_item_session in comment_list_session:
                        user_name = comment_item_session.find(
                            class_='ux-mooc-comment-course-comment_comment-list_item_body_user-info_name').string
                        user_url = comment_item_session.find(
                            class_='ux-mooc-comment-course-comment_comment-list_item_avatar').a['href']
                        user_name_list.append(user_name)
                        user_url_list.append('https://' + user_url)
                        if find_flag > 1:
                            comment = comment_item_session.find(
                                class_='ux-mooc-comment-course-comment_comment-list_item_body_content').span.string
                            stundent_score = len(comment_item_session.find_all(
                                class_='ux-icon-custom-rating-favorite'))
                            class_name_list.append(class_name)
                            class_comment_list.append(comment)
                            student_score_list.append(float(stundent_score))

                        logger.info('已经获得%d条信息(当前所查找课程:%s(%d/%d))' % (
                            len(user_name_list), class_name, class_idx + 1,
                            total_class_num))
                    if not comment_section.find(
                            class_='ux-mooc-comment-course-comment_pager'):  # 只有一页，获取当前页信息后立即退出
                        break
                    flag = comment_section.find(class_='th-bk-disable-gh')
                    if flag and flag.string == '下一页':  # 已经到最后一页
                        break
                    ele = driver.find_element_by_partial_link_text('下一页')
                    ele.click()
                    time.sleep(0.2)
                    soup = get_Soup(driver)
                    comment_section = soup.find(id='comment-section')
                except:
                    pass
    class_condiction_dict = {
        '课程名': class_list,
        '评论人数': comment_num_list,
        '得分': class_score_list
    }
    if find_flag > 0:
        user_urls_dict = {
            '昵称': user_name_list,
            '个人链接': user_url_list,
        }
        if find_flag > 1:
            comment_dict = {
                '昵称': user_name_list,
                '课程': class_name_list,
                '评论': class_comment_list,
                '打分': student_score_list
            }
            return class_condiction_dict, user_urls_dict, comment_dict
        return class_condiction_dict, user_urls_dict
    return class_condiction_dict


def get_Into_User_Page(logger, user_url_list, driver):
    """
    进入学生界面，获取学生信息
    :param logger:
    :param user_url_list: 学生链接列表
    :param driver:
    :return:
         dict: 学生信息列表，包含昵称、教育状态、学习时长、讨论次数、获得赞数、关注人数、粉丝数
    """
    user_name_list = []
    education_list = []
    study_time_list = []
    discuss_count_list = []
    zan_count_list = []
    follow_count_list = []
    fan_count_list = []
    student_count = 0
    teacher_count = 0
    for user_idx, user_url in enumerate(user_url_list):
        driver = get_Into_Page(user_url, driver)
        soup = get_Soup(driver)
        try:
            user_info_session = soup.find(class_='u-userInfo-container')
            user_name = user_info_session.find(class_='u-ui-name').span.string
            education = user_info_session.find(class_='u-ui-tag').span.string
            study_time = user_info_session.find(class_='u-ui-time-cont').span.string
            discuss_count = user_info_session.find(
                class_='u-ui-discuss-cont').span.string
            zan_count = user_info_session.find(class_='u-ui-zan-cnt').span.string
            follow_count = filter_digit(user_info_session.find(
                class_='u-ui-f2f').span.contents[0].string)
            fan_count = filter_digit(user_info_session.find(
                class_='u-ui-f2f').span.contents[1].string)
            if not user_name: user_name = 'null'
            if not education: education = 'null'
            if not study_time: study_time = 'null'
            if not discuss_count: discuss_count = -1
            if not zan_count: zan_count = -1
            if not follow_count: follow_count = -1
            if not fan_count: fan_count = -1

            education = ''.join(education.strip().split())
            education_list.append(education)
            study_time_list.append(study_time)
            discuss_count_list.append(int(discuss_count))
            zan_count_list.append(int(zan_count))
            follow_count_list.append(int(follow_count))
            fan_count_list.append(int(fan_count))
            user_name_list.append(user_name)
            student_count += 1
            logger.info('已经获得%d条学生信息:%s,%s,%s,%d,%d,%d,%d' % (
                student_count, user_name, education, study_time,
                int(discuss_count), int(zan_count), int(follow_count), int(fan_count)))
        except:
            teacher_count += 1
            logger.info('获得%d条老师信息:%s' % (teacher_count, user_url))

    dict = {
        '昵称': user_name_list,
        '教育状态': education_list,
        '学习时长': study_time_list,
        '讨论次数': discuss_count_list,
        '获得赞数': zan_count_list,
        '关注人数': follow_count_list,
        '粉丝数': fan_count_list
    }
    return dict
