# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import os
import json
import datetime
import unittest
import HTMLTestReportCN
from monitor.Saber.EngineModule import CreateTestCaseModule


def run_test(test_list, save_report_path, host_ip):
    """
    :description: 使用xml运行测试
    :param test_list: 载入的测试用例(列表)
    :param save_report_path: 报告存放路径
    :param host_ip: 访问HOST的IP
    """
    # print(json.dumps(test_list, ensure_ascii=False))
    # 定义所有测试类的列表
    class_resp_status_list = list()
    # 定义所有文件的TestSuite
    test_suite_for_all_file = unittest.TestSuite()
    for test_file_dict in test_list:
        # 定义单个文件的TestSuite
        test_suite_for_single_file = unittest.TestSuite()
        # 遍历每个文件
        for test_key, test_value in test_file_dict.items():
            # 定义每一个文件的的TestSuite
            test_suite_for_file = unittest.TestSuite()
            # 根据文件生成测试用例类
            test_file_class = CreateTestCaseModule.create_test_case_class_for_file((test_key, test_value), host_ip)
            # 将测试类加入到列表当中
            class_resp_status_list.append(test_file_class.resp_status_list)
            # 遍历每个类的测试步骤
            for test_file_case in test_value:
                # 取步骤的title当做测试方法名,并将这个测试方法加入到Test_Suite当中
                test_suite_for_file.addTest(test_file_class(test_file_case['title']))
            # 将每个文件的TestSuite加入到单个的TestSuite当中
            test_suite_for_single_file.addTests(test_suite_for_file)
        # 将每个文件的TestSuite加入整个TestSuite当中
        test_suite_for_all_file.addTests(test_suite_for_single_file)
    # 获取当前时间
    now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    # 建立报告完整路径
    file_name = 'Result_' + host_ip + '_' + now_time + '.html'
    report_full_name = save_report_path + os.sep + file_name
    with open(report_full_name, 'wb') as file_open:
        # 定义报告内容输出
        runner = HTMLTestReportCN.HTMLTestRunner(stream=file_open, title='测试结果', tester=host_ip)
        # 运行测试
        result = runner.run(test_suite_for_all_file)

    # 注意文件路径
    if result is not None:
        # 获取测试的状态参数
        success_count = result.success_count
        error_count = result.error_count
        failure_count = result.failure_count
        return {
            'ip': host_ip,
            'status': {'success': success_count, 'error': error_count, 'failure': failure_count},
            'time': now_time,
            'flag': True,
            'report_full_name': report_full_name,
            'report_name': file_name,
            'class_resp_status_list': class_resp_status_list
        }
    else:
        return {'flag': False}

