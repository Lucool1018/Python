# -*- coding: utf-8 -*-
# 导入第三方库
import shutil
import os
import re
import time
"""
程序一：1. 找出指定路径下的所有PNG文件，并将找到的PNG文件进行重命名，命名规则为：创建日期+
原始文件名，最后，将重命名好的PNG文件移动到其他指定文件夹下。
分解步骤：
1.1 提取所有文件名，使用正则表达式判断是否为png文件
1.2 使用rename函数进行重命名；
1.3 使用shutil移动文件夹
"""
# 1.1.1 os库提取所有文件名；
path1 = r"C:\Users\Lu_Cool\Desktop\python自动化办公\实验四\第一题"
file_names_li1 = os.listdir(path1)
# 1.1.2 re库判断是否为png文件；
for file_name in file_names_li1:
    match_rule = re.compile('png$', re.S)
    rst = re.findall(match_rule, file_name)
    # 1.1.3 设置移动文件后的路径
    new_path = path1 + '\\' + 'new_file'
    # 1.1.4 判断文件夹是否存在
    if os.path.exists(new_path) is False:
        # 1.1.5 使用os.mkdir函数创建文件
        os.mkdir(new_path)
    else:
        pass
    # 当文件名以png结尾，则表明时png文件
    if len(rst) != 0:
        # 1.2.1拼接出原始文件路径
        ori_path = path1+'\\'+file_name
        # 1.2.2 os库提取文件创建日期, 使用localtime转换出其中的年月日信息
        temp_time = time.localtime(os.path.getctime(ori_path))
        # 1.2.3 使用strftime函数将秒时间戳转化为年月日
        # std_time = time.strftime("%Y-%m-%d %H:%M:%S", temp_time)
        std_time = time.strftime("%Y-%m-%d", temp_time)  # 不包含时分秒
        # 1.2.4 拼接出新的文件名
        new_name = std_time + file_name
        # 1.2.5 拼接出旧的文件地址和新的文件[夹]地址
        old_path = path1 + '\\' + new_name
        # 1.3.1 使用os库的rename函数进行重命名[创建日期+原始文件名]
        os.rename(ori_path, old_path)
        # 1.3.2 使用shutil库的move移动文件
        shutil.move(old_path, new_path)
    # 当文件名不以.png结尾，则跳过
    else:
        pass


'''
程序二：2.获取指定路径下的所有文件和文件夹，每个文件的名称、大小、文件类型按行写入一个txt文
件中（若是文件夹，文件类型则为文件夹即可，不必包含文件夹中的内容）
分解步骤：
1.1 提取所有文件名，提取文件【名称】、【大小】、【后缀】
1.2 写入到txt文档中
'''
# os库提取所有文件名；
path2 = r"C:\Users\Lu_Cool\Desktop\python自动化办公\实验四\第二题"
file_names_li2 = os.listdir(path2)
# 设置存储信息的空字典
info_li = []
# 正则库判断文件类型
for file_name in file_names_li2:
    # 提取不含后缀的文件名
    match_rule1 = re.compile('(.*?)\.([a-z]+)', re.S)
    pure_file_name = re.findall(match_rule1, file_name)
    # 拼接出文件路径
    file_path = path2 + '\\' + file_name
    # 设置存储每一个文件信息的字典
    if len(pure_file_name) != 0:
        info_dic = {'file_name': pure_file_name[0][0]}
    else:
        info_dic = {'file_name': file_name}
    # 使用os库的stat函数来获取文件信息，选择其中的st_size获取文件大小
    info_dic['file_size'] = os.stat(file_path).st_size
    # 使用正则表达式进行匹配
    match_rule2 = re.compile('\.([a-z]+)', re.S)
    rst = re.findall(match_rule2, file_name)
    # 当没有匹配到后缀的时候，说明其为文件夹
    if len(rst) == 0:
        info_dic['file_type'] = '文件夹'
        info_li.append(info_dic)
    # 当匹配到后缀的时候该文件的文件类型即为该文件后缀
    else:
        info_dic['file_type'] = rst[0]
    # 将存储了文件信息的字典添加到列表中
    info_li.append(info_dic)
# 设置存储信息的txt文件路径
path = r"C:\Users\Lu_Cool\Desktop\python自动化办公\实验四\第二题\result.txt"
# 写入信息
with open(path, 'w+', encoding='utf-8') as fp:
    for index, info_dic in enumerate(info_li):
        # 写入文件信息
        fp.write('文件{}名称：{}\n'.format(index+1, info_dic['file_name']))
        fp.write('文件{}类型：{}\n'.format(index+1, info_dic['file_type']))
        fp.write('文件{}大小：{}\n'.format(index+1, info_dic['file_size']))










