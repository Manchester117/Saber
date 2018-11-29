# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import os
import datetime
from collections import OrderedDict
from monitor.Saber.VIKRunModule.VIKRunner import run_test
from monitor.Saber.WriteReportToDB import handle_model
from monitor.Saber.RunModeModule import LoadTestCase
from monitor.Saber.LogModule import LogConfigure
from monitor.Saber.EmailNotice import SendEmail


def read_host_file():
    """
    :description: 遍历存放Host文件的文件夹,并将Host文件内容存放在字典当中
    :return: 存放Host文件内容的字典
    """
    # 测试使用
    # host_folder_base_path = os.path.abspath('../../static/host_configure')
    # 获取Host文件的绝对路径
    host_folder_base_path = os.path.abspath(os.path.join('monitor', 'static', 'host_configure'))
    # 获取路径下存放Host的子文件夹
    host_folder_list = os.listdir(host_folder_base_path)
    # 初始化有序字典
    host_dict = OrderedDict()
    # 通过遍历获取Host文件内容
    for host_folder in host_folder_list:
        host_folder_path = os.sep.join([host_folder_base_path, host_folder])
        host_client_dict = OrderedDict()
        host_file_list = os.listdir(host_folder_path)
        for host_file in host_file_list:
            file_path = os.sep.join([host_folder_path, host_file])
            with open(file_path, 'r', encoding='UTF-8') as f:
                host_client_dict[host_file] = f.readlines()
        host_dict[host_folder] = host_client_dict
    # 返回Host的内容(有序字典),Host文件名称
    return host_dict


def switch_host_for_windows(host_file_content):
    """
    :description: 切换Windows下的Hosts文件
    :param host_file_content:
    :return:
    """
    # 读取当前Host文件
    current_host_conf_file = open('C:\Windows\System32\drivers\etc\hosts', 'w+')
    current_host_conf_file.truncate()  # 清空原来的Host
    # 重写当前的Host文件
    current_host_conf_file.writelines(host_file_content)
    current_host_conf_file.close()
    LogConfigure.logger.info('已经切换Windows的Host文件')


def switch_host_for_linux(host_file_content):
    """
    :description: 切换Linux下的Hosts文件
    :param host_file_content:
    :return:
    """
    # 读取当前Host文件
    current_host_conf_file = open('/etc/hosts', 'w+')
    current_host_conf_file.truncate()  # 清空原来的Host
    # 重写当前的Host文件
    current_host_conf_file.writelines(host_file_content)
    current_host_conf_file.close()
    # 重启网络服务(调用Linux命令)
    # subprocess.call(['/etc/init.d/network', 'restart'])
    LogConfigure.logger.info('已经切换Linux的Host文件')


def create_report_folder(batch_run_time):
    # 获取当前时间当做报告保存目录
    now_time_folder = batch_run_time.strftime('%Y-%m-%d_%H-%M-%S')
    # 建立存放报告目录
    save_report_path = os.path.join(os.path.abspath('.'), 'monitor', 'static', 'report', now_time_folder)
    os.mkdir(save_report_path)

    return save_report_path


def compose_test_case():
    # 载入测试用例
    total_test_list = LoadTestCase.load_test_case_for_xml()
    # 定义各端的测试用例列表
    c_list = list()
    b_list = list()
    h_list = list()
    j_list = list()
    w_list = list()
    m_list = list()
    r_list = list()
    for test_case_dict in total_test_list:
        for test_case_key, test_case_value in test_case_dict.items():
            # 判断用例属于哪个端,并把对应某端用例加入到对应列表中
            if test_case_key.startswith('C端_'):
                c_list.append(test_case_dict)
            if test_case_key.startswith('B端_'):
                b_list.append(test_case_dict)
            if test_case_key.startswith('H端_'):
                h_list.append(test_case_dict)
            if test_case_key.startswith('J端_'):
                j_list.append(test_case_dict)
            if test_case_key.startswith('W端_'):
                w_list.append(test_case_dict)
            if test_case_key.startswith('M端_'):
                m_list.append(test_case_dict)
            if test_case_key.startswith('R端_'):
                r_list.append(test_case_dict)
    # 将列表合并成字典
    total_test_case_dict = dict()
    total_test_case_dict['C_Client'] = c_list
    total_test_case_dict['B_Client'] = b_list
    total_test_case_dict['H_Client'] = h_list
    total_test_case_dict['J_Client'] = j_list
    total_test_case_dict['W_Client'] = w_list
    total_test_case_dict['M_Client'] = m_list
    total_test_case_dict['R_Client'] = r_list

    return total_test_case_dict


def judge_time_out(host_check_dict):
    # 当前机器的超时数量
    total_timeout_num = 0
    # 设置每个请求是否超时,并把每个请求的响应状态放到列表中
    class_resp_status_list = list()
    for resp_status_list in host_check_dict['class_resp_status_list']:
        for resp_status in resp_status_list:
            # 设定超时阀值4000
            if resp_status['resp_duration'] > 4000:
                resp_status['is_timeout'] = 1  # 已超时
                total_timeout_num += 1  # 如果超时,数量+1
            else:
                resp_status['is_timeout'] = 0  # 未超时
            class_resp_status_list.append(resp_status)
    return total_timeout_num, class_resp_status_list


def run_test_control(host_dict):
    # 获取当前时区的当前时间
    batch_run_time = datetime.datetime.now()
    # 创建存放报告文件夹,并获取文件夹的路径
    save_report_path = create_report_folder(batch_run_time)

    # 将测试用例按照各端进行归类
    total_test_case_dict = compose_test_case()
    # 定义保存每个HOST检查结果的列表,用于邮件发送
    host_check_status_dict = dict()
    # 定义保存至数据库的信息列表
    save_report_list = list()
    # 修改当前系统的Host,并运行测试
    for host_key_client, host_value in host_dict.items():
        host_client_dict = host_dict[host_key_client]
        host_check_status_dict[host_key_client] = list()
        for host_key_ip, host_value_content in host_client_dict.items():
            # 筛选用例C_Client/H_Client/B_Client/W_Client/J_Client/M_Client,并运行测试(传递报告存放路径),前提条件是用例列表的长度不能为0
            if len(total_test_case_dict[host_key_client]) != 0:
                # 切换Host-Linux
                switch_host_for_linux(host_client_dict[host_key_ip])
                # 切换Host-Windows
                # switch_host_for_windows(host_client_dict[host_key_ip])
                LogConfigure.logger.info('切换Hosts: {}'.format(host_key_ip))
                # 运行测试
                host_check_dict = run_test(total_test_case_dict[host_key_client], save_report_path, host_key_ip)
                # 测试用例归类
                host_client = None
                if host_key_client == 'C_Client': host_client = 'C端'
                if host_key_client == 'B_Client': host_client = 'B端'
                if host_key_client == 'H_Client': host_client = 'H端'
                if host_key_client == 'J_Client': host_client = 'J端'
                if host_key_client == 'W_Client': host_client = 'W端'
                if host_key_client == 'M_Client': host_client = 'M端'
                if host_key_client == 'R_Client': host_client = 'R端'

                # 统计超市个数和返回状态
                total_timeout_num, class_resp_status_list = judge_time_out(host_check_dict)

                # 将超时数量插入到邮件模板的数据结构当中
                host_check_dict['status']['timeout'] = total_timeout_num
                # 将运行结果加入到列表中,用于发送邮件
                host_check_status_dict[host_key_client].append(host_check_dict)
                # 建立保存至数据库的记录
                save_report_list.append({
                    'save_report_path': save_report_path,
                    'save_report_full_name': host_check_dict['report_full_name'],
                    'host_client': host_client,
                    'host_key_ip': host_key_ip,
                    'batch_run_time': batch_run_time,
                    'class_resp_status_list': class_resp_status_list
                })

    # 将记录保存至数据库
    handle_model.save_report_batch_aggregate(save_report_list, batch_run_time)
    return host_check_status_dict


def run_multiple_test():
    """
    :description: 运行测试,并切换HOST,保存至数据库,发送邮件
    :return:
    """
    # 获取Host文件内容,以及Host文件名称
    host_dict = read_host_file()
    host_check_status_dict = run_test_control(host_dict)
    # 发送邮件
    SendEmail.send_report(os.path.join(os.path.abspath('.'), 'monitor', 'Saber', 'mail_configure.conf'), host_check_status_dict)
    # 移除日志Handler,避免日志写入到一个文件中,下次运行时写入新的日志文件.
    # LogConfigure.logger.getLogger('').removeHandler(LogConfigure.file_handler)


if __name__ == '__main__':
    run_multiple_test()
