# -*- coding: utf-8 -*-
'''
第二步：两种方式得到的txt文档进行校对，校对内容包括两个文件的：
1.mail长度和数量
2.文档字节数
3.tel长度和数量
'''

# 导入需要的库
import os
import re
import shutil


# 移动文件夹
def move_file(movefile_path):
    # 旧地址和要移动到的地址
    try:
        # 获取文件夹地址
        oldpos = movefile_path
        newpos = r"E:\课题\wrongfile_txt\{}\txt_all\{}.txt".format(year, issuer_name)
        # 移动文件夹
        shutil.copy(oldpos, newpos)
    except:
        print(issuer_name + '移动异常')

for year in range(2003, 2006):
    # 读取文件，保留含有@和.com项数多的txt文档,并且含有数字最多的
    txt_path_list = ['txt_up&down', 'txt_left&right']
    issuer_path_li1, issuer_path_li2 = [], []
    for txt_path in txt_path_list:
        path = r"E:\课题\wrongfile_txt\{}\{}".format(year, txt_path)
        # 获取文件夹中的文件名
        issuer_name_li = os.listdir(path)
        for issuer_path in issuer_name_li:
            # 将文件名组合为各文件的地址
            issuer_path = path + '\\' + issuer_path
            if txt_path == 'txt_up&down':
                issuer_path_li1.append(issuer_path)
            elif txt_path == 'txt_left&right':
                issuer_path_li2.append(issuer_path)
    # 遍历 第一个txt文档中的信息
    info_num1_li = []
    for issuer_path in issuer_path_li1:
        # 得到 issuer_name和各自的地址
        issuer_name = re.findall('txt_up&down\\\\(.*?).txt', issuer_path, re.DOTALL)[0]
        info_dic = {
            'issuer_name1': issuer_name,
            'issuer_path': issuer_path,
            'mail_num1': 0
            }
        info_num1, len_mail1 = 0, 0
        issuer_telnum_sum1 = 0
        with open(issuer_path, 'r', encoding='utf-8') as fp:
            info_li = fp.readlines()
            for info in info_li:
                match_str = re.findall('(\S+?@.*?\.com)', info, re.DOTALL)
                issuer_telnum = len(re.findall('\d', info, re.DOTALL))
                issuer_telnum_sum1 += issuer_telnum
                # 测量mail 的长度
                num1 = len(match_str)
                if num1 != 0:
                    info_dic['mail_num1'] += len(match_str[0])
                info_num1 += num1
            info_dic['num1'] = info_num1
            info_dic['issuer_telnum'] = issuer_telnum_sum1
        info_num1_li.append(info_dic)
    # 遍历 第二个txt文档中的信息
    info_num2_li = []
    for issuer_path in issuer_path_li2:
        # 得到 issuer_name和各自的地址
        issuer_name = re.findall('txt_left&right\\\\(.*?).txt', issuer_path, re.DOTALL)[0]
        info_dic = {
            'issuer_name2': issuer_name,
            'issuer_path': issuer_path,
            'mail_num2': 0
            }
        info_num2, len_mail2 = 0, 0
        issuer_telnum_sum2 = 0
        with open(issuer_path, 'r', encoding='utf-8') as fp:
            info_li = fp.readlines()
            for info in info_li:
                match_str = re.findall('(\S+?@.*?\.com)', info, re.DOTALL)
                issuer_telnum = len(re.findall('\d', info, re.DOTALL))
                issuer_telnum_sum2 += issuer_telnum
                # 测量mail 的长度
                num2 = len(match_str)
                if num2 != 0:
                    info_dic['mail_num2'] += len(match_str[0])
                info_num2 += num2
            info_dic['num2'] = info_num2
            info_dic['issuer_telnum'] = issuer_telnum_sum2
        info_num2_li.append(info_dic)
    # 匹配两个文档中的issuer
    for info_num1, info_num2 in zip(info_num1_li, info_num2_li):
        # print(info_num1_li[0:1], info_num1_li[0:1])
        # 获取文件名
        issuer_name = list(info_num1.values())[0]
        # 确保两个文件的文件名相同
        if list(info_num2.values())[0] == list(info_num1.values())[0]:
            # if list(info_num1.keys())[0] == list(info_num2.keys())[0]:
            temp1 = list(info_num1.values())[3]
            temp2 = list(info_num2.values())[3]
            # break
            # 当两个文件中匹配到的含@和.com的项数相同时
            if temp1 == temp2:
                # 判断两个文档 mail是否完整,当两个文档中的 mail长度不相等时，保留长的，去掉短的
                len_mail1 == info_num1['mail_num1']
                len_mail2 == info_num2['mail_num2']
                if len_mail1 > len_mail2:
                    movefile_path = list(info_num1.values())[1]
                    move_file(movefile_path)
                    pass
                elif len_mail1 < len_mail2:
                    movefile_path = list(info_num2.values())[1]
                    move_file(movefile_path)
                    pass
                elif len_mail1 == len_mail2:
                    # 判断包含的数字多少，保留数字多的
                    issuer_telnum_sum1 = info_num1['issuer_telnum']
                    issuer_telnum_sum2 = info_num2['issuer_telnum']
                    if issuer_telnum_sum1 > issuer_telnum_sum2:
                        # 判断文档中包含的tel数量大小，移动数量多的
                        movefile_path = list(info_num1.values())[1]
                        move_file(movefile_path)
                        pass
                    elif issuer_telnum_sum1 < issuer_telnum_sum2:
                        # 判断文档中包含的tel数量大小，移动数量多的
                        movefile_path = list(info_num2.values())[1]
                        move_file(movefile_path)
                        pass
                    # 两个文档中数字相同时候
                    elif issuer_telnum_sum2 == issuer_telnum_sum1:
                        # 获取文件字节数
                        issuer1_sise = os.path.getsize(list(info_num1.values())[1])
                        issuer2_size = os.path.getsize(list(info_num2.values())[1])
                        # 判断文件大小，移动文件大的
                        if issuer1_sise == issuer2_size:
                            movefile_path = list(info_num1.values())[1]
                            move_file(movefile_path)
                            pass
                        # 第一个文件中字节多于第二个文件中字节
                        elif issuer1_sise > issuer2_size:
                            movefile_path = list(info_num1.values())[1]
                            move_file(movefile_path)
                            pass
                        # 第二个文件中字节多于第一个文件中字节
                        else:
                            movefile_path = list(info_num2.values())[1]
                            move_file(movefile_path)
                            pass
            # 当两个文件中匹配到的含@和.com的项数不同时候
            elif temp1 > temp2:
                movefile_path = list(info_num1.values())[1]
                # 保留第一个文件夹中的文件，移动到最终文件夹中
                move_file(movefile_path)
                pass
            else:
                movefile_path = list(info_num2.values())[1]
                # 保留第二个文件夹中的文件，移动到最终文件夹中
                move_file(movefile_path)
                pass
        else:
            print(issuer_name + ' error')
    print(' success!!!')







