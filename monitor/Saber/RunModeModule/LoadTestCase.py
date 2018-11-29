# -*- coding: utf-8 -*-

__author__ = 'Peng.Zhao'

import os
from monitor.Saber.ReadTestCaseXml import ReadXmlData


def load_test_case_for_xml():
    """
    :description: 载入测试用例XML
    :return: 返回所有测试数据结构
    """
    # 定义测试用例列表用于存放xml
    xml_list = []

    # 获取当前TestCase的路径(xml)
    test_case_path = os.path.join(os.path.abspath('.'), 'monitor', 'static', 'testcase')

    # 获取当前TestCase中的文件列表(xml)
    test_case_xml_list = os.listdir(test_case_path)

    # 过滤其他文件,将xml文件放置到列表中
    if len(test_case_xml_list) > 0:
        for test_xml in test_case_xml_list:
            # 如果文件后缀是.xml,那么就把这个文件放置到列表当中
            if test_xml.startswith('Test_') and test_xml.endswith('.xml'):
                xml_absolute_path = test_case_path + "/" + test_xml
                xml_list.append(xml_absolute_path)
    else:
        print("没有需要执行的测试用例(xml)")
    # 返回所有测试数据
    total_test_list = ReadXmlData.get_total_test_data(xml_list)
    # print(json.dumps(total_test_list, ensure_ascii=False))
    return total_test_list


if __name__ == '__main__':
    load_test_case_for_xml()
