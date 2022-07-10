# -*- coding: utf-8 -*-
'''
第一步:选取pdf第一页，通过左&右半页页面截取和上&下半页页面截取，两种方式切割pdf中的页面并将提取到的信息保留到txt文档中
'''
# 导入需要的第三方库
from IPython.display import Image
import fitz
import os
import re


def get_tel(text, info_dic):
    # 设置记录tel的标记
    tel_mark = 0
    if 14 >= len(re.findall('\d', text, re.DOTALL)) > 9:
        # 剔除掉name和mail后计算长度
        mail_len = len(re.findall('(\S+?@.*?.com)', text))
        if len(re.findall('(\S+?@.*?.com)', text)) != 0:
            mail_len = len(re.findall('(\S+?@.*?.com)', text)[0])
        actual_tel_len = len(re.findall('\w', text, re.DOTALL))-mail_len
        if actual_tel_len < 50:
            temp_str = re.sub('\.|/|:', '', text, re.DOTALL)
            tel_li = re.findall('(\)|\(|-|\d|\.|\+)', temp_str, re.DOTALL)
            tel = []
            for i in tel_li:
                tel.append(" ") if len(i) == 0 else tel.append(i)
            tel = "".join(tel).strip('-')
            info_dic['tel'] = tel
            tel_mark = 1
    return tel_mark


# content_split = get_split_rst(0)
# 处理切割后信息的列表和数值的函数
def get_splitinfo(content_split):
    # 定义存储信息的空字典和空列表以及值
    info_dic = {
        'mail': '',
        'tel': ''
        }
    split_rst, temp_index_li, temp_li = [], [], []
    tel_num, mail_num, start_index, stop_mark = 0, 0, 0, 0
    mail_mark, info_mark = 0, 0
    # 剔除掉无效字符【-】
    for temp_str in content_split:
        temp_str = re.sub('[/}\|{]', '-', temp_str, re.DOTALL)
        temp_li.append(temp_str)
        content_split = temp_li
    # 判断信息是否完整
    for text in content_split:
        # 判断是否有mail
        mail = re.findall('(\S+?@.*?\.com)', text, re.DOTALL)
        if len(mail) != 0:
            # 如果该列表中仅有一个mail
            if 0 < len(mail[0]) <= 50:
                info_dic['mail'] = mail[0]
                # 设置记录 mail的标记
                mail_mark = 1
                break
    for text in content_split:
        # 判断是否含有tel
        tel_mark = get_tel(text, info_dic)
        if tel_mark == 1:
            break
    # 当字典的键全不为空时标记为 1表示该截取方式获取到了内容
    if [mail_mark, tel_mark] == [1, 1]:
        info_mark = 1
    # 没有匹配时查找是否存在“Analysis by”或仅含有tel
    if info_mark != 1:
        # 是否存在“Analysis by”
        for text in content_split:
            if re.findall('Analysis by', text, re.DOTALL):
                info_mark = 2
                split_rst.append([text])
        if info_mark == 2:
            return info_mark, split_rst
        # 是否仅含有tel
        if tel_mark == 1:
            info_mark = 3
    for index_1, split_text in enumerate(content_split):
        # 若标记值为0，则表示当前页面没有匹配到信息
        if info_mark == 0:
            break
        # content_split = content_split[0:1]
        # 当存在 mail时，以每一个以.com为分割点分割，分割结果存储在列表中
        if list(info_dic.values())[0] != "":
            # print(index_1, split_text)
            # 定位 mail的位置
            # split_text = 
            if re.findall('(\S+?@.*?\.com)', split_text, re.DOTALL):
                # print(split_text)
                # 记录 mail一共出现的次数
                mail_num += 1
                # 从开始位置切割到 mail所在位置，并将切割结果添加到 append_li中
                append_li = content_split[start_index:index_1+1]
                # x = ['CREDIT SUISSE FIRST BOSTON CORPORATION ', 'Equity Research Americas ', ' ', 'Industry: Business Services ', ' ', 'Michael E. Hoffman 212/325 3123 michael.hoffman@csfb.com ']
                # print(append_li)
                # 记录当前 mail所在的位置
                temp_index_li.append(index_1)
                # 切割后的内容超过 6行，则进行再次切割，去掉冗余信息
                if len(append_li) >= 12:
                    # 仅保留 7行
                    if content_split[index_1-12: index_1+1] not in split_rst:
                        split_rst.append(content_split[index_1-12: index_1+1])
                # 切割后的结果小于6行，则直接存储到列表中
                else:
                    if content_split[start_index: index_1+1] not in split_rst:
                        split_rst.append(content_split[start_index: index_1+1])
                # 记录前一次切割的位置
                start_index = index_1+1
                # print(split_rst)
            # 要求切割结果不为空列表
            if split_rst != []:
                # 遍历切割结果，判断当前切割的结果中是否邮箱数量和tel数量相同
                for rsts in split_rst:
                    for rst in rsts:
                        if 10 <= len(re.findall('\d', rst, re.DOTALL)) <= 12:
                            # 记录 tel一共出现的次数
                            tel_num += 1
                # 当二者不相等时，重复进行多遍历一行信息，再次判断，直到全部遍历完成或者两者相等
                if tel_num != mail_num:
                    # 从未切割的行中搜索 tel
                    for index_2, rest_info in enumerate(content_split[start_index:]):
                        # 判断是否检索到 tel
                        if 10 <= len(re.findall('\d', rest_info, re.DOTALL)) <= 12:
                            # 记录 tel一共出现的次数
                            tel_num += 1
                        if tel_num == mail_num:
                            # 将 tel存储到列表中
                            split_rst[-1].extend(content_split[start_index:start_index+index_2+1])
                            stop_mark = 1
                            break
    for index_1, split_text in enumerate(content_split):
        # 当不存在 mail时，但能够匹配到 tel的时候，以每一个以tel为分割点分割前后五行并存储在列表中
        conditions = [
            list(info_dic.values())[0] == "",
            20 >= len(info_dic["tel"]) > 9,
            stop_mark == 0
            ]
        # 定位tel所在的位置
        if all(conditions):
            # print(index_1, split_text)
            # 从开始位置切割到 tel所在位置，并将切割结果添加到 append_li中
            append_li = content_split[start_index:index_1+1]
            # 记录当前 tel所在的位置
            temp_index_li.append(index_1)
            # 切割后的内容超过 6行，则进行再次切割，去掉冗余信息
            if len(append_li) >= 6:
                # 仅保留 7行
                if content_split[index_1-6: index_1+1] not in split_rst:
                    split_rst.append(content_split[index_1-6: index_1+1])
            # 切割后的结果小于6行，则直接存储到列表中
            else:
                if content_split[start_index: index_1+1] not in split_rst:
                    split_rst.append(content_split[start_index: index_1+1])
            # 记录前一次切割的位置
            start_index = index_1+1
    return info_mark, split_rst


# 截取屏幕
def get_split_rst(put_str):
    # put_str=0
    if put_str == 0:
        start_args, end_args, up_args, down_args = 0, 0.45, 0, 1   # 得到左边的页面
    elif put_str == 1:
        start_args, end_args, up_args, down_args = 0.55, 1, 0, 1   # 得到右边的页面
    elif put_str == 2:
        start_args, end_args, up_args, down_args = 0, 1, 0, 0.45   # 得到上边的页面
    elif put_str == 3:
        start_args, end_args, up_args, down_args = 0, 1, 0.55, 1   # 得到下边的页面
    # 截取屏幕
    clip = fitz.Rect(rect.width*start_args, rect.height*up_args,
                     rect.width*end_args, rect.height*down_args)
    pix_1 = page.getPixmap(matrix=mat, alpha=False, clip=clip)
    # 展示截取的部分
    Image(pix_1.getImageData())
    # 获取截取屏幕中的信息
    content = page.getText(clip=clip)
    # 将获取到的信息进行分割
    return content.splitlines()


# 得到输出结果并存储为txt文档
def save_info(args=0):
    # 左右分割页面来匹配
    if args == 0:
        # 选取左半边页面
        info_mark = get_splitinfo(get_split_rst(0))[0]
        lr_split_rst = get_splitinfo(get_split_rst(0))[1]
        # 如果标记值为0则表明页面获取到的信息残缺或未获取到信息
        if info_mark == 0:
            # 选取右半边页面
            info_mark = get_splitinfo(get_split_rst(1))[0]
            lr_split_rst = get_splitinfo(get_split_rst(1))[1]
        #  写入到 txt文件中
        with open(lr_path + "\\{}.txt".format(issuer_name), 'w+', encoding='utf-8') as fp:
            for words in lr_split_rst:
                fp.write('-'*10+'\n')
                for word in words:
                    fp.write(word+'\n')
    # 上下分割页面来匹配
    elif args == 1:
        # 选取上半边页面
        info_mark = get_splitinfo(get_split_rst(2))[0]
        ud_split_rst = get_splitinfo(get_split_rst(2))[1]
        if info_mark == 0:
            # 选取下半边页面
            info_mark = get_splitinfo(get_split_rst(3))[0]
            ud_split_rst = get_splitinfo(get_split_rst(3))[1]
        #  写入到 txt文件中
        with open(ud_path + "\\{}.txt".format(issuer_name), 'w+', encoding='utf-8') as fp:
            for words in ud_split_rst:
                fp.write('-'*10+'\n')
                for word in words:
                    fp.write(word+'\n')
    return info_mark


if __name__ == '__main__':
    # 存储整个年份信息的列表
    fail_li = []
    for year in range(2003, 2004):
        # 设置根目录
        join_path = r"E:\课题\wrongfile"
        # 切割后的 txt存储地址
        txt_savepath = join_path + '_txt'
        # 如果存储 txt的文件夹不存在就创建一个
        if os.path.exists(txt_savepath) is False:
            os.mkdir(txt_savepath)
        # 读取原文件夹中的 pdf
        files = os.listdir(join_path + "\\{}".format(year))
        # 创建左右切割和上下切割结果的文件夹
        lr_path = txt_savepath + '\\{}\\txt_left&right'.format(year)
        ud_path = txt_savepath + '\\{}\\txt_up&down'.format(year)
        all_path = txt_savepath + '\\{}\\txt_all'.format(year)
        if os.path.exists(lr_path) is False:
            os.mkdir(lr_path)
        if os.path.exists(ud_path) is False:
            os.mkdir(ud_path)
        if os.path.exists(all_path) is False:
            os.mkdir(all_path)
        for num, file_name in enumerate(files[9:10]):
            # 获得不含有后缀的文件名
            issuer_name = re.sub('.pdf', '', file_name, re.DOTALL)
            # 拼接出文件地址
            temp_path = join_path + "\\{}\\".format(year) + file_name
            pdfDoc = fitz.open(temp_path)
            # 遍历所有页面
            for i in range(pdfDoc.pageCount)[0:1]:
            # for i in range(pdfDoc.pageCount)[0:1]:
                info_mark_li = []
                # i = 16
                page = pdfDoc[i]
                # 参数 1表示放大 1倍
                mat = fitz.Matrix(1, 1)
                rect = page.rect
                # args = 0 时匹配左右页面，= 1 时匹配上下页面
                try:
                    for args in range(2):
                        # 分割页面来匹配
                        info_mark_li.append(save_info(args))
                    # print(info_mark_li)
                    if all(info_mark_li) == 0 and i+1 == pdfDoc.pageCount:
                        # 当前页面不存在 tel和 mail，需要遍历所有页面，此处提示并添加到解析错误的列表中
                        fail_li.append(issuer_name)
                        print('{}年{}中信息匹配失败'.format(year, issuer_name, i+1))
                    # 如果匹配到信息就停止遍历后面的页面
                    if any(info_mark_li) >= 1:
                        print('{}年{}在第{}页中信息匹配成功'.format(year, issuer_name, i+1))
                        break
                except:
                    # 将爬取失败的文件名进行存储
                    fail_li.append(issuer_name)







