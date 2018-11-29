# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import unittest
from copy import deepcopy
from monitor.Saber.EngineModule import PackingTestCase
from monitor.Saber.EngineModule import TestFunWrapper


def create_test_case_class_for_file(test_tuple, host_ip):
    """
    :description: 创建测试用例类(兼容XML/Excel)
    :param test_tuple: 获取单个测试数据文件的名称和数据
    :return: 返回测试类
    """
    # 载入参数,根据测试用例中的item,分别获取4个列表
    title_list, req_data_list, corr_list, wait_seconds_list, verify_list = PackingTestCase.packing_test_case(test_tuple[1])
    # 创建方法字典
    test_member_dict = dict()
    # 这里必须使用深度复制,因为生成了多个类,而多个类会引用同一个属性,导致关联出现问题.
    test_member_dict['resp_status_list'] = deepcopy(list())
    test_member_dict['case_name'] = deepcopy(test_tuple[0])
    test_member_dict['title_list'] = deepcopy(title_list)
    test_member_dict['req_data_list'] = deepcopy(req_data_list)
    # 测试类的corr_list必须使用深度复制,否则会出现第一台机运行正常,后续机器运行出错.
    test_member_dict['corr_list'] = deepcopy(corr_list)
    test_member_dict['wait_seconds_list'] = deepcopy(wait_seconds_list)
    test_member_dict['verify_list'] = deepcopy(verify_list)
    test_member_dict['server_ip'] = deepcopy(host_ip)
    # 定义测试类的静态变量,用于流程型用例数据的读取
    test_member_dict['index'] = 0
    # 加入测试方法
    for test_case_title in title_list:
        test_member_dict[test_case_title] = TestFunWrapper.test_wrapper_fun

    host_ip_str = '_'.join(host_ip.split("."))
    # 获取类名
    class_name = host_ip_str + '_' + test_tuple[0]

    # 创建测试类
    single_test_class = type(class_name, (unittest.TestCase,), test_member_dict)
    return single_test_class
