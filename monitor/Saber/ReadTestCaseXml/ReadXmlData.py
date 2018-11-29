# -*- coding: utf-8 -*-

__author__ = 'Peng.Zhao'

from lxml import etree
import json


def get_total_test_data(xml_list):
    """
    :description: 获取所有的xml文件的测试数据
    :return: 返回所有数据
    """
    total_test_list = []
    for xml in xml_list:
        # xml_file = open(xml, mode='r', encoding='UTF-8')
        # xml_line = xml_file.readlines()
        # for line in range(0, len(xml_line)):
        #     print(line.decode('UTF-8'))
        doc = etree.ElementTree(file=xml)
        xml_root = doc.getroot()
        single_test = get_single_test_data(xml_root)
        total_test_list.append(single_test)
    # print(json.dumps(total_test_list, ensure_ascii=False))
    # print(total_test_list)
    return total_test_list


def get_single_test_data(xml_root):
    """
    :description: 从xml中获取TestSuite
    :return: 返回单条测试suite
    """
    test_suite_dict = dict()
    test_suite_dict[xml_root.get('name')] = list()
    for child in xml_root:
        if child.tag == 'TestCase':
            test_case = get_test_case_data(child)
            test_suite_dict[xml_root.get('name')].append(test_case)
    # print(json.dumps(test_suite_dict, ensure_ascii=False))
    # print(test_suite_dict)
    return test_suite_dict


def get_test_case_data(test_case):
    """
    :description: 从xml中获取数据拼凑成dict
    :return: 返回单条测试用例
    """
    test_case_dict = dict()
    for leaf in test_case:
        if leaf.tag == 'title':
            test_case_dict['title'] = leaf.text
        if leaf.tag == 'data':
            test_case_dict['data'] = get_request_data(leaf)
        if leaf.tag == 'corrParams':
            test_case_dict['corrParams'] = get_correlation_data(leaf)
        if leaf.tag == 'waitSeconds':
            test_case_dict['waitSeconds'] = get_wait_seconds(leaf)
        if leaf.tag == 'verify':
            test_case_dict['verify'] = get_verify_data(leaf)
    return test_case_dict


def get_request_data(leaf_request_data):
    """
    :description: 从xml中获取请求的数据
    :return: 返回请求数据的dict
    """
    request_data = dict()
    for item in leaf_request_data.iter():
        if item.tag == 'url' or item.tag == 'method':
            request_data[item.tag] = item.text
        if item.tag == 'json':
            if item.text is not None:
                # 加入strip删除'\n'
                # 需要将json字符串转为字典(使用eval)
                json_data = eval(item.text.strip())
                request_data[item.tag] = json_data
            else:
                request_data[item.tag] = None
        if item.tag == 'getParams' or item.tag == 'postParams' or item.tag == 'headers' or item.tag == 'cookies':
            param_dict = dict()
            for param in item.iter():
                if param.text is not None:
                    # 替换xml中的'&amp;',并去掉两边的空白字符
                    param_content = param.text.replace('&amp;', '&')
                    # 如果节点的key不为None则把参数放到param_dict当中
                    if param.get('name') is not None:
                        param_dict[param.get('name')] = param_content.strip()
            if param_dict.__len__() == 0:
                param_dict = None
            request_data[item.tag] = param_dict
    return request_data


def get_correlation_data(leaf_corr_data):
    """
    :description: 从xml中获取需要关联的正则表达式
    :return: 返回关联的dict
    """
    corr_data = dict()
    for item in leaf_corr_data.iter():
        if item.text is not None and item.get('name') is not None:
            corr_data[item.get('name')] = item.text.strip()
    if corr_data.__len__() == 0:
        corr_data = None
    return corr_data


def get_wait_seconds(leaf_wait_seconds):
    """
    :description: 从xml中获取每一步的暂停时间
    :return: 返回暂停时间
    """
    return leaf_wait_seconds.text


def get_verify_data(leaf_verify_data):
    """
    :description: 从xml中获取需要验证的数据
    :return: 返回验证list
    """
    verify_data = list()
    for item in leaf_verify_data:
        if item in leaf_verify_data.iter():
            check_tuple = (item.get('name'), item.text.strip())
            verify_data.append(check_tuple)
    if verify_data.__len__() == 0:
        verify_data = None
    return verify_data


