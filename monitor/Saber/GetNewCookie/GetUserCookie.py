import os
import re
import requests
from monitor.Saber.LogModule import LogConfigure


def get_new_cookie():
    c_cookie = requests.get('http://webapi.xxxx.cn/api/SeekerToken', params={'userid': '8420579'})
    # print('C端Cookie:', c_cookie.text)
    LogConfigure.logging.info('获取C端Cookie: ' + c_cookie.text)

    h_cookie = requests.get('http://webapi.xxxx.cn/api/HunterToken', params={'userid': '42135'})
    # print('H端Cookie:', h_cookie.text)
    LogConfigure.logging.info('获取H端Cookie: ' + h_cookie.text)

    b_cookie = requests.get('http://webapi.xxxx.cn/api/usertoken/GetRecruiterToken', params={'userid': '58208', 'accountName': 'highpin_ci@126.com'})
    # print('B端Cookie:', b_cookie.text)
    LogConfigure.logging.info('获取B端Cookie: ' + b_cookie.text)

    # 去掉获取token的所有引号
    c_cookie = c_cookie.text[1: -1]
    h_cookie = h_cookie.text[1: -1]
    b_cookie = b_cookie.text[1: -1]
    return c_cookie, h_cookie, b_cookie


def search_cookie(case_path):
    # TestCase中匹配Cookie的正则表达式
    c_cookie_regex = '_o_c_n_=(.*?)&amp;'
    h_cookie_regex = 'htk=(.*?)&amp;'
    b_cookie_regex = 'RecruiterAccount=(.*?)&amp;'

    c_cookie, h_cookie, b_cookie = get_new_cookie()
    for root, dirs, files in os.walk(case_path):
        for file in files:
            if file.endswith('.xml'):
                if file.startswith('Test_C端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, c_cookie, c_cookie_regex)
                if file.startswith('Test_H端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, h_cookie, h_cookie_regex)
                if file.startswith('Test_B端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, b_cookie, b_cookie_regex)
                if file.startswith('Test_J端_B端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, b_cookie, b_cookie_regex)
                if file.startswith('Test_J端_H端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, h_cookie, h_cookie_regex)
                if file.startswith('Test_J端_C端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, c_cookie, c_cookie_regex)
                if file.startswith('Test_W端_B端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, b_cookie, b_cookie_regex)
                if file.startswith('Test_W端_H端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, h_cookie, h_cookie_regex)
                if file.startswith('Test_W端_C端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, c_cookie, c_cookie_regex)
                if file.startswith('Test_M端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, c_cookie, c_cookie_regex)
                if file.startswith('Test_R端'):
                    file_path = os.path.join(root, file)
                    modify_cookie(file_path, h_cookie, h_cookie_regex)


def modify_cookie(xml, new_cookie, cookie_regex):
    # 读取文件(标志位设置为读写)
    with open(xml, 'r', encoding='UTF-8') as f:
        xml_lines = f.readlines()
        # 以下标方式检查每一行用例
        for index in range(0, len(xml_lines)):
            # 用正则表达式匹配要替换的cookie
            pattern = re.search(cookie_regex, xml_lines[index])
            # 如果匹配成功,进行替换操作,并将原来的cookie行删除,插入新的cookie行
            if pattern is not None:
                # 正则匹配,定位原有cookie
                old_cookie = pattern.group(1)
                # 进行替换
                new_xml_line = xml_lines[index].replace(old_cookie, new_cookie)
                # 删除旧的cookie行
                xml_lines.remove(xml_lines[index])
                # 插入新的cookie行
                xml_lines.insert(index, new_xml_line)
        f.close()
    # 以写方式打开,直接清空文件,再执行写入操作
    with open(xml, 'w', encoding='UTF-8') as f:
        # 写入新的测试用例
        f.writelines(xml_lines)
        f.close()
    print('Modify XML Complete! -', f.name)


if __name__ == '__main__':
    search_cookie('')

