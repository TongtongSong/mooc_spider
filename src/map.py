#!/usr/bin python
# -*- coding:utf-8 -*-
# @Author: Tongtong Song(TJU)
# @Data: 2020/11/15
# @Last Update Time: 2020/11/21 12:00
# @Others: For 大数据分析理论与算法
# @File: src/map.py

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Map
import os
import re
from selenium import webdriver
from src.utils import get_Into_Page, get_Soup, get_Chorme_Option


def city_to_province():
    area_data = {
        '北京': ['北京', '北京市', '朝阳区', '海淀区', '通州区', '房山区', '丰台区', '昌平区', '大兴区', '顺义区', '西城区', '延庆县', '石景山区', '宣武区', '怀柔区',
               '崇文区',
               '密云县',
               '东城区', '门头沟区', '平谷区'],
        '广东': ['广东', '广东省', '东莞市', '广州市', '中山市', '深圳市', '惠州市', '江门市', '珠海市', '汕头市', '佛山市', '湛江市', '河源市', '肇庆市', '潮州市',
               '清远市',
               '韶关市', '揭阳市', '阳江市', '云浮市', '茂名市', '梅州市', '汕尾市'],
        '山东': ['山东', '山东省', '济南市', '青岛市', '临沂市', '济宁市', '菏泽市', '烟台市', '泰安市', '淄博市', '潍坊市', '日照市', '威海市', '滨州市', '东营市',
               '聊城市',
               '德州市', '莱芜市', '枣庄市'],
        '江苏': ['江苏', '江苏省', '苏州市', '徐州市', '盐城市', '无锡市', '南京市', '南通市', '连云港市', '常州市', '扬州市', '镇江市', '淮安市', '泰州市', '宿迁市'],
        '河南': ['河南', '河南省', '郑州市', '南阳市', '新乡市', '安阳市', '洛阳市', '信阳市', '平顶山市', '周口市', '商丘市', '开封市', '焦作市', '驻马店市', '濮阳市',
               '三门峡市', '漯河市', '许昌市', '鹤壁市', '济源市'],
        '上海': ['上海', '上海市', '松江区', '宝山区', '金山区', '嘉定区', '南汇区', '青浦区', '浦东新区', '奉贤区', '闵行区', '徐汇区', '静安区', '黄浦区', '普陀区',
               '杨浦区',
               '虹口区', '闸北区', '长宁区', '崇明县', '卢湾区'],
        '河北': ['河北', '河北省', '石家庄市', '唐山市', '保定市', '邯郸市', '邢台市', '河北区', '沧州市', '秦皇岛市', '张家口市', '衡水市', '廊坊市', '承德市',
               '三河市'],
        '浙江': ['浙江', '浙江省', '温州市', '宁波市', '杭州市', '台州市', '嘉兴市', '金华市', '湖州市', '绍兴市', '舟山市', '丽水市', '衢州市'],
        '陕西': ['陕西', '陕西省', '西安市', '咸阳市', '宝鸡市', '汉中市', '渭南市', '安康市', '榆林市', '商洛市', '延安市', '铜川市'],
        '湖南': ['湖南', '湖南省', '长沙市', '邵阳市', '常德市', '衡阳市', '株洲市', '湘潭市', '永州市', '岳阳市', '怀化市', '郴州市', '娄底市', '益阳市', '张家界市',
               '湘西州', '吉首市'],
        '重庆': ['重庆', '重庆市', '江北区', '渝北区', '沙坪坝区', '九龙坡区', '万州区', '永川市', '南岸区', '酉阳县', '北碚区', '涪陵区', '秀山县', '巴南区', '渝中区',
               '石柱县', '忠县', '合川市', '大渡口区', '开县', '长寿区', '荣昌县', '云阳县', '梁平县', '潼南县', '江津市', '彭水县', '璧山县', '綦江县',
               '大足县', '黔江区', '巫溪县', '巫山县', '垫江县', '丰都县', '武隆县', '万盛区', '铜梁县', '南川市', '奉节县', '双桥区', '城口县'],
        '福建': ['福建', '福建省', '漳州市', '泉州市', '厦门市', '福州市', '莆田市', '宁德市', '三明市', '南平市', '龙岩市'],
        '天津': ['天津', '天津市', '和平区', '北辰区', '河北区', '河西区', '西青区', '津南区', '东丽区', '武清区', '宝坻区', '红桥区', '大港区', '汉沽区', '静海县',
               '宁河县',
               '塘沽区', '蓟县', '南开区', '河东区'],
        '云南': ['云南', '云南省', '昆明市', '红河州', '大理市', '文山州', '德宏州', '曲靖市', '昭通市', '楚雄州', '保山市', '玉溪市', '丽江市', '思茅地区',
               '西双版纳州', '怒江州', '迪庆州', '蒙自市', '楚雄市', '临沧市', '个旧市', '景洪市', '普洱市'],
        '四川': ['四川', '四川省', '成都市', '绵阳市', '广元市', '达州市', '南充市', '德阳市', '广安市', '阿坝州', '巴中市', '遂宁市', '内江市', '凉山州', '攀枝花市',
               '乐山市',
               '自贡市', '泸州市', '雅安市', '宜宾市', '资阳市', '眉山市', '甘孜州', '西昌市', '汶川县', '广汉市'],
        '广西': ['广西', '广西壮族自治区', '贵港市', '玉林市', '北海市', '南宁市', '柳州市', '桂林市', '梧州市', '钦州市', '来宾市', '河池市', '百色市', '贺州市',
               '崇左市',
               '防城港市'],
        '安徽': ['安徽', '安徽省', '芜湖市', '合肥市', '六安市', '宿州市', '阜阳市', '安庆市', '马鞍山市', '蚌埠市', '淮北市', '淮南市', '宣城市', '黄山市', '铜陵市',
               '亳州市',
               '池州市', '巢湖市', '滁州市'],
        '海南': ['海南', '海南省', '三亚市', '海口市', '琼海市', '文昌市', '东方市', '昌江县', '陵水县', '乐东县', '五指山市', '保亭县', '澄迈县', '万宁市', '儋州市',
               '临高县',
               '白沙县', '定安县', '琼中县', '屯昌县'],
        '江西': ['江西', '江西省', '南昌市', '赣州市', '上饶市', '吉安市', '九江市', '新余市', '抚州市', '宜春市', '景德镇市', '萍乡市', '鹰潭市'],
        '湖北': ['湖北', '湖北省', '武汉市', '宜昌市', '襄樊市', '荆州市', '恩施市', '孝感市', '黄冈市', '十堰市', '咸宁市', '黄石市', '仙桃市', '随州市', '天门市',
               '荆门市',
               '潜江市', '鄂州市', '神农架林区', '襄阳市'],
        '山西': ['山西', '山西省', '太原市', '大同市', '运城市', '长治市', '晋城市', '忻州市', '临汾市', '吕梁市', '晋中市', '阳泉市', '朔州市'],
        '辽宁': ['辽宁', '辽宁省', '大连市', '沈阳市', '丹东市', '辽阳市', '葫芦岛市', '锦州市', '朝阳市', '营口市', '鞍山市', '抚顺市', '阜新市', '本溪市', '盘锦市',
               '铁岭市'],
        '台湾': ['台湾', '台湾省', '台北市', '高雄市', '台中市', '新竹市', '基隆市', '台南市', '嘉义市'],
        '黑龙江': ['黑龙江', '黑龙江省', '齐齐哈尔市', '哈尔滨市', '大庆市', '佳木斯市', '双鸭山市', '牡丹江市', '鸡西市', '黑河市', '绥化市', '鹤岗市', '伊春市',
                '大兴安岭地区',
                '七台河市'],
        '内蒙古': ['内蒙古', '内蒙古自治区', '赤峰市', '包头市', '通辽市', '呼和浩特市', '乌海市', '鄂尔多斯市', '呼伦贝尔市', '兴安盟', '巴彦淖尔市', '乌兰察布市',
                '锡林郭勒盟',
                '阿拉善盟'],
        '香港': ["香港", "香港特别行政区"],
        '澳门': ['澳门', '澳门特别行政区'],
        '贵州': ['贵州', '贵州省', '贵阳市', '黔东南州', '黔南州', '遵义市', '黔西南州', '毕节市', '铜仁市', '安顺市', '六盘水市', '凯里市',
               '都匀市', '兴义市'],
        '甘肃': ['甘肃', '甘肃省', '兰州市', '天水市', '庆阳市', '武威市', '酒泉市', '张掖市', '陇南地区', '白银市', '定西市', '平凉市',
               '嘉峪关市', '临夏回族自治州', '金昌市', '甘南州', '陇南市'],
        '青海': ['青海', '青海省', '西宁市', '海西州', '海东地区', '海北州', '果洛州', '玉树州', '黄南藏族自治州'],
        '新疆': ['新疆', '新疆维吾尔自治区', '乌鲁木齐市', '伊犁州', '昌吉市', '石河子市', '哈密市', '阿克苏市', '巴音郭楞州', '喀什地区',
               '塔城地区', '克拉玛依市', '和田市', '阿勒泰州', '吐鲁番地区', '阿拉尔市', '博尔塔拉州', '五家渠市', '奎屯市', '伊宁市',
               '克孜勒苏州', '图木舒克市', '库尔勒市', '阿克苏市'],
        '西藏': ['西藏', '西藏藏族自治区', '拉萨市', '山南地区', '林芝地区', '日喀则地区', '阿里地区', '昌都地区', '那曲地区'],
        '吉林': ['吉林', '吉林省', '吉林市', '长春市', '白山市', '白城市', '延边州', '松原市', '辽源市', '通化市', '四平市', '延吉市'],
        '宁夏': ['宁夏', '宁夏回族自治区', '银川市', '吴忠市', '中卫市', '石嘴山市', '固原市']
    }

    city_to_province_dict = {value: key for key in area_data for value in area_data[key]}
    return city_to_province_dict


def get_University_List(driver, university_url):
    driver = get_Into_Page(university_url, driver)
    soup = get_Soup(driver)
    content = soup.find('tbody')
    u_to_city_dict = {}
    for id, tr in enumerate(content.find_all('tr')):
        if id > 2:
            tds = tr.find_all('td')
            if len(tds) == 5:
                u_to_city_dict[tds[1].contents[0]] = tds[3].contents[0]
    add_data = {'广东技术师范大学': '广东省', '成都信息工程大学': '成都市', '桂林旅游学院': '桂林市',
                '湖北文理学院': '湖北省', '岭南师范学院': '广东省', '中国计量大学': '南京市',
                '中国社会科学院大学': '北京市', '南京财经大学红山学院': '南京市', '宿迁学院': '宿迁市',
                '中国石油大学（华东）': '山东省', '南宁师范大学': '南宁市', '西藏民族大学': '咸阳市',
                '豫章师范学院': '江西省', '郑州轻工业大学': '郑州市', '国防科技大学': '长沙市', '东南大学成贤学院': '南京市',
                '苏州大学文正学院': '苏州市', '湖北长江互联网教育研究院': '湖北省', '四川计算机学会': '四川省',
                '中国地质大学（北京）': '北京市', '华北电力大学（保定）': '保定市', '江苏科技大学苏州理工学院': '苏州市',
                '南京审计大学金审学院': '南京市', '中国矿业大学徐海学院': '徐州市', '上海应用技术大学': '上海市',
                '河南中医药大学': '河南省', '中国矿业大学（北京）': '北京市', '南京理工大学紫金学院': '南京市',
                '江苏师范大学科文学院': '江苏省', '南京师范大学中北学院': '南京市', '上海立信会计金融学院': '上海市',
                '徐州医科大学': '徐州市', '第四军医大学': '西安市', '成都大学': '成都市', '北部湾大学': '广西壮族自治区',
                '天津体育学院运动与文化艺术学院': '天津市', '河南师范大学新联学院': '河南省',
                '中国人民解放军陆军工程大学': '南京市', '南京师范大学泰州学院': '泰州市',
                '南京信息工程大学滨江学院': '南京市', '南京传媒学院': '南京市',
                '中国人民警察大学': '廊坊市', '国家开放大学': '北京市',
                '中国矿大（徐州）': '徐州市'}
    u_to_city_dict.update(add_data)
    print(u_to_city_dict)
    return u_to_city_dict


def get_Student_Area(excel_file, u_to_city_dict, city_to_province_dict):
    university_list = list(u_to_city_dict.keys())
    city_list = list(set(list(u_to_city_dict.values())))
    class_df = pd.read_excel(excel_file)
    class_dict = class_df.to_dict()
    student_education_list = list(class_dict['教育状态'].values())
    study_time_list = list(class_dict['学习时长'].values())
    none_sense_list = ['nan', '其他']
    zaizhi_count = 0
    student_count = 0
    student_have_university_count = 0
    ok_student_have_university_count = 0

    area_have_student = {}
    area_have_study_time_all = {}
    area_have_study_time_avg = {}
    for area in city_list:
        try:
            province = city_to_province_dict[area]
            area_have_student[province] = 0.1  # 防止整除时为0
            area_have_study_time_all[province] = 0
            area_have_study_time_avg[province] = 0
        except:
            print(area)

    for i in range(len(student_education_list)):
        education = str(student_education_list[i])
        if education and education not in none_sense_list:
            education_list = re.split('[|-]', student_education_list[i])
            if education_list[0] == '在职':
                zaizhi_count += 1
            elif education_list[0] == '学生':
                student_count += 1
                if len(education_list) == 3 and education_list[1] != '其他':
                    university = education_list[1]
                    student_have_university_count += 1
                    if university in university_list:
                        try:
                            province = city_to_province_dict[u_to_city_dict[university]]
                            area_have_student[province] += 1
                            study_time = str(study_time_list[i])
                            if study_time != 'nan':
                                study_time = study_time.replace('分', '').split('时')
                                study_time = int(study_time[0]) + int(study_time[1]) / 60
                                area_have_study_time_all[province] += float(study_time)
                            ok_student_have_university_count += 1
                        except:
                            print(u_to_city_dict[university])
                    else:
                        print(university)
    for province, study_time_all in area_have_study_time_all.items():
        area_have_study_time_avg[province] = round(study_time_all / area_have_student[province], 0)
    print(zaizhi_count, student_count, student_have_university_count,
          ok_student_have_university_count)
    return area_have_student, area_have_study_time_all, area_have_study_time_avg


def get_Class_Area(excel_file, u_to_city_dict, city_to_province_dict):
    class_info_dict = pd.read_excel(excel_file).to_dict()
    university_list = list(class_info_dict['学校'].values())
    university_list_no_re = list(set(university_list))
    area_have_class = {}
    count = 0
    for u in university_list_no_re:
        try:
            area_have_class[city_to_province_dict[u_to_city_dict[u]]] = 0
        except:
            print(u)
    for u in university_list:
        try:
            area_have_class[city_to_province_dict[u_to_city_dict[u]]] += 1
            count += 1
        except:
            pass
    print(count)
    return area_have_class


def Draw_Map_Block(dict, file_path, title, max):
    data = list(dict.items())
    pop_geo = (
        Map().add("", data, "china")
            .set_global_opts(
            title_opts=opts.TitleOpts(title=title, pos_top="5%"),
            visualmap_opts=opts.VisualMapOpts(max_=max, pos_left="8%", is_piecewise=True))
    )

    pop_geo.render(file_path)


def Draw_Map(picture_dir, class_info_with_url_file, user_info_class_file):
    chrome_options = get_Chorme_Option()

    driver = webdriver.Chrome(options=chrome_options)
    university_site = \
        'http://www.chinadegrees.cn/xwyyjsjyxx/xwsytjxx/qgptgxmd/qgptgxmd.html'
    u_to_city_dict = get_University_List(driver, university_site)
    driver.close()
    driver.quit()

    city_to_province_dict = city_to_province()

    area_have_class = get_Class_Area(class_info_with_url_file, u_to_city_dict,
                                     city_to_province_dict)
    dict_to_draw = area_have_class
    print(dict_to_draw)
    file_name = 'area_have_class'
    block_picture_path = os.path.join(picture_dir, file_name + '_block.html')
    title = ''
    max_num = max(dict_to_draw.values())
    Draw_Map_Block(dict_to_draw, block_picture_path, title, max_num)

    area_have_student, area_have_study_time_all, area_have_study_time_avg = \
        get_Student_Area(user_info_class_file, u_to_city_dict, city_to_province_dict)
    file_name = 'area_have_student'
    block_picture_path = os.path.join(picture_dir, file_name + '_block.html')
    title = '单位（人）'
    dict_to_draw = area_have_student
    max_num = max(dict_to_draw.values())
    print(dict_to_draw)
    Draw_Map_Block(dict_to_draw, block_picture_path, title, max_num)

    file_name = 'area_have_study_time_all'
    block_picture_path = os.path.join(picture_dir, file_name + '_block.html')
    title = '单位（小时）'
    dict_to_draw = area_have_study_time_all
    max_num = max(dict_to_draw.values())
    print(dict_to_draw)
    Draw_Map_Block(dict_to_draw, block_picture_path, title, max_num)

    file_name = 'area_have_study_time_avg'
    block_picture_path = os.path.join(picture_dir, file_name + '_block.html')
    title = '单位（小时）'
    dict_to_draw = area_have_study_time_avg
    max_num = max(dict_to_draw.values())
    print(dict_to_draw)
    Draw_Map_Block(dict_to_draw, block_picture_path, title, max_num)
