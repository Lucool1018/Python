# -*- coding: utf-8 -*-
'''
第三步：提取信息存储到excel中
'''
# 导入需要的库
import re
import os
from difflib import SequenceMatcher
import xlsxwriter


# 写入到 excel文件中
def write_data(all_info_li):
    wkfile = xlsxwriter.Workbook(r"C:\Users\Lu_Cool\Desktop\result.xlsx")
    sheet = wkfile.add_worksheet()
    # del sheet
    # 写入表头
    head_li = ['issuer']
    for i in range(1, 6):
        head_li.append('name' + str(i))
        head_li.append('mail' + str(i))
        head_li.append('tel' + str(i))
        head_li.append('seniority' + str(i))
        head_li.append('qualification' + str(i))
    for index, head in enumerate(head_li):
        sheet.write(0, index, head)
    # 写入数据
    for row in range(len(all_info_li)):
        # 写入 name和 mail
        name_col, mail_col, tel_col, seniority_col, qualification_col = 1, 2, 3, 4, 5
        # 写入文件名
        sheet.write(row+1, 0, all_info_li[row][0])
        for info in all_info_li[row][1:]:
            # 写入 name
            sheet.write(row+1, name_col, list(info.values())[1])
            name_col += 5
            # 写入 mail
            sheet.write(row+1, mail_col, list(info.values())[2])
            mail_col += 5
            # 写入 tel
            sheet.write(row+1, tel_col, list(info.values())[3])
            tel_col += 5
            # 写入 seniority
            sheet.write(row+1, seniority_col, list(info.values())[4])
            seniority_col += 5
            # 写入 qualification
            sheet.write(row+1, qualification_col, list(info.values())[0])
            qualification_col += 5
    # 文件存储
    wkfile.close()

# 获得列表中相似度最高的的字符串
def get_max_str(ration_li):
    # ration_li = [0.2, 0.3]
    # 获得相似度最高的字符串
    for index, i in enumerate(ration_li):
        if ration_li[0] < ration_li[index]:
            ration_li[0] = ration_li[index]
    return index


# 相似度检验
def cul_similarity(info):
    # info = info_li[7]
    # 得到 mail前的 name
    temp_str =  re.findall('(\S+?)@.*?.com', info, re.DOTALL)
    if len(temp_str) != 0:
        # 格式化字符串
        temp_str = re.sub('\.|-|_', '', temp_str[0], re.DOTALL)
        ration_li = []
        for info1 in info_li:
            # info1 = info_li[6]
            # name = map(lambda x: re.sub("{}|-|:|,\s(.*?)".format(x), "", info, re.DOTALL), seniority)
            # 去掉职称等信息
            for m in seniority:
                info1 = info1.replace(m, '')
            for n in qualification:
                # n = 'CFA'
                info1 = info1.replace(n, '')
            name = re.sub('\d|:|-|,|\n', '', info1, re.DOTALL).strip(' ')
            # 相似度计算
            similarity = SequenceMatcher(lambda x: x in '. ', temp_str, name.lower())
            # similarity = SequenceMatcher(lambda t: t in ".- ", 'JinMing Liu', 'jliu')
            ration_li.append(similarity.ratio())
            # 判断：相似度超过百分之五十并且不包含.com
            conditions1 = [
                similarity.ratio() > 0.5,
                re.findall('(.com)', info1, re.DOTALL) != ['.com'],
                # similarity.ratio() == max(ration_li)
                ]
            # print(similarity.ratio(), info1)
            # print(similarity.ratio(), temp_str, "*"*30, name)
            if all(conditions1):
                # 2.拿到真实的 name
                # 去除前后多余的字符串和数字
                # name = re.sub("[\)-\(]", "", name, re.DOTALL)
                # name = 'Christopher J. Purtill 215-665-6601 \n'
                name = re.findall("(['\w\s\.]+)[\W|\D|/]", name+' ', re.DOTALL)
                if len(name) == 1:
                    info_dic['name'] = name[0]
                # 将分割开的部分再次进行相似度比对
                else:
                    ration_li2 = []
                    for part_name in name:
                        pass
                        similarity = SequenceMatcher(lambda x: x in '. ', temp_str, part_name.lower())
                        # similarity = SequenceMatcher(lambda t: t in ".- ", 'JinMing Liu', 'jliu')
                        ration_li2.append(similarity.ratio())
                    info_dic['name'] = name[get_max_str(ration_li2)]
                return True
    else:
        pass


fail_li, all_info_li = [], []
# 读取文件名
files = os.listdir(r"C:\Users\Lu_Cool\Desktop\txt")
# 遍历txt文档
for issuer in files:
    # files = files[6:7]
    # 获得 issuer
    issuer_name = re.sub('.txt', '', issuer, re.DOTALL)
    path = r"C:\Users\Lu_Cool\Desktop\txt\\" + issuer
    # 存储信息的列表
    info_issuer_li = [issuer_name]
    # 读取文件
    # path = r"C:\Users\Lu_Cool\Desktop\txt\American Water Works Co Inc -Janney Montgomery Scott.txt"
    with open(path, 'r', encoding='utf-8') as fp:
        info_li = fp.readlines()
    # 定义记录信息的字典
    info_dic = {
            # 记录是否获取了证书（CFA、CPA等）
            'qualification': 'None',
            'name': "",
            'mail': "",
            'tel': "",
            # 记录是什么级别的分析师
            'seniority': "None"
            }
    seniority = ['Sr Research Analyst', 'Senior Analyst', 'Associate Analyst', 'Research Analyst', 'Associate', 'Analysts', 'Analyst']
    qualification = ['CFA', 'CA', 'CPA', 'PhD']
    # 遍历 info_lower_li获取 name
    for info in info_li:
        # info = info_li[5]
        # 1.拿到邮件
        mail = re.findall('(\S+?@.*?.com)', info, re.DOTALL)
        if len(mail) != 0:
            # 如果该列表中仅有一个mail
            # if len(mail) == 1:
            if 0 < len(mail[0]) <= 50:
                info_dic['mail'] = mail[0]
            # 如果该列表中有两个及两个以上的mail
            # if len(mail) > 1:
                # mail = get_max_str()
                # name = 
                # qualification = 
                # seniority = 
                # tel = 
        # 2.拿到 邮箱中的 name
        # 正常情况
        rst = cul_similarity(info)
        # print(name, 2)
        # print(1)
        # 特殊格式（只适用于某一类）情况
        if rst == None:
            match_str = re.findall('\s(.*?)@', " "+info, re.DOTALL)
            if len(match_str) == 1:
                # 判断 mail，name以及tel是否在一行
                if len(match_str[0]) >= 25:
                    tel_len = len("".join(re.findall('\d+', match_str[0], re.DOTALL)))
                    if tel_len != 0:
                        # 去掉数字后再减去mail的长度后测量长度,如果大于10表明在同一行
                        mail_name = re.findall('(\S+?)@.*?.com', info, re.DOTALL)
                        if len(match_str[0])-len(mail_name[0])-tel_len > 10:
                            # 拿到 邮箱中的 前半部分用来匹配
                            temp_str = re.findall('(\S+?)@', " "+info, re.DOTALL)
                            new_str = re.sub('{}|\d|-|\)|\(|:'.format(temp_str[0]), '', match_str[0], re.DOTALL).strip(' ')
                            pop_str = re.findall('[,\s\.\w]+(\W+)', new_str, re.DOTALL)
                            # 真实的 name
                            name = re.sub(pop_str[0], '', new_str, re.DOTALL).strip(' ')
                            info_dic['name'] = name
                            # print(name, 2)
                    else:
                        # 再减去mail的长度后测量长度
                        if len(match_str[0])-len(mail_name[0]) > 10:
                            # 拿到 邮箱中的 前半部分用来匹配
                            temp_str = re.findall('(\S+?)@', " "+info, re.DOTALL)
                            new_str = re.sub(temp_str[0], '', match_str[0], re.DOTALL).strip(' ')
                            pop_str = re.findall('[,\s\.\w]+(\W+)', new_str, re.DOTALL)
                            # 真实的name
                            name = re.sub(pop_str[0], '', new_str, re.DOTALL).strip(' ')
                            # 相似度检验
                            info_dic['name'] = name
                            # print(name, 3)
                            # info_dic['name'] = 'Joseph Garcia, CFA\n'
        # 3.获取 qualification
        for i in qualification:
            if i in info:
                info_dic['qualification'] = i
                break
        # 4.获取 tel
        # info = info_li[-2]
        if 14 >= len(re.findall('\d', info, re.DOTALL)) >= 9:
            # 剔除掉name和mail后计算长度
            mail_len = len(re.findall('(\S+?@.*?.com)', info))
            if len(re.findall('(\S+?@.*?.com)', info)) != 0:
                mail_len = len(re.findall('(\S+?@.*?.com)', info)[0])
            if len(re.findall('\w', info, re.DOTALL))-mail_len < 50:
                temp_str = re.sub('\.|/|:', '', info, re.DOTALL)
                 # tel_li = re.findall('(\)|\(|-|\d|\.|\+)', info, re.DOTALL)
                tel_li = re.findall('(\)|\(|-|\d|\.|\+)', temp_str, re.DOTALL)
                tel = []
                for i in tel_li:
                    tel.append(" ") if len(i) == 0 else tel.append(i)
                tel = "".join(tel).strip('-')
                info_dic['tel'] = tel
        # 5.获取 seniority
        for i in seniority:
            if i in info:
                info_dic['seniority'] = i
                break
        # 判断该 info_dic是否信息提取完全
        conditions2 = [
            len(info_dic['mail']) != 0,
            len(info_dic['name']) != 0,
            len(info_dic['tel']) != 0
            ]
        # 满足上述条件时添加到到总列表中
        if all(conditions2):
            info_issuer_li.append(info_dic)
            # 清除数据继续检索
            info_dic = {
                'qualification': 'None',
                'name': "",
                'mail': "",
                'tel': "",
                'seniority': "None"
                }
            # 记录获取name的当前位置
            # position = index
    print(info_issuer_li)
    if len(info_issuer_li) == 1:
        # 存储失败的文件
        fail_li.append(info_issuer_li[0])
    # 全部信息汇总
    all_info_li.append(info_issuer_li)

# 写入到excel中
write_data(all_info_li)



