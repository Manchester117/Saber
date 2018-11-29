# -*- coding: utf-8 -*-
from monitor.Saber.EmailNotice.CreateMailHTML import create_mail_template

__author__ = 'Peng.Zhao'

import os
import smtplib
import configparser
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from monitor.Saber.LogModule import LogConfigure
from monitor.Saber.ReportHandler.ReportHandler import report_compress


def read_config(conf_path):
    """
    :description: 读取配置文件,并返回配置文件解析
    :param conf_path:
    :return:
    """
    file_path_name = conf_path
    parse = configparser.ConfigParser()
    parse.read(file_path_name, encoding='UTF-8')
    return parse


def send_email_html_content(parse_info, host_check_status_dict):
    """
    :description: 编辑邮件正文,并且发送邮件
    :param parse_info: 邮箱配置信息
    :param host_check_status_dict: 错误数量和通过数量
    :return:
    """
    LogConfigure.logging.info('开始发送邮件')
    # 确定报告存放路径
    # report_folder_path = os.path.abspath('monitor/static/report')
    report_folder_path = os.path.join(os.path.abspath('.'), 'monitor', 'static', 'report')

    host = parse_info.get('smtp_host_info', 'host')
    port = parse_info.getint('smtp_host_info', 'port')

    username = parse_info.get('sender_info', 'username')
    password = parse_info.get('sender_info', 'password')

    sender = parse_info.get('email_info', 'sender')
    receiver = parse_info.get('email_info', 'receiver')
    subject = parse_info.get('email_info', 'subject')

    # 定义邮件框架
    msg = MIMEMultipart()

    # 添加邮件附件
    # last_report_folder = select_last_report_folder(report_folder_path)
    # 获取报告的绝对路径
    # report_full_path = report_folder_path + os.sep + last_report_folder
    # 对文件进行压缩
    # zip_report_full_path = report_compress(report_full_path)

    # 将压缩的报告文件夹,上传为邮件附件
    # report_attach = open(zip_report_full_path, 'rb')
    # mst_attach = MIMEText(report_attach.read(), 'base64', _charset='UTF-8')
    # mst_attach['Content-Type'] = 'application/octet-stream'
    # mst_attach['Content-Disposition'] = 'attachment; filename=' + zip_report_full_path.split(os.sep)[-1]
    # msg.attach(mst_attach)
    # 生成的HTML报告
    doc = create_mail_template(host_check_status_dict)

    # 添加邮件正文(HTML)
    mst_text = MIMEText(doc.getvalue(), _subtype='html', _charset='UTF-8')
    # print(doc.getvalue())
    msg.attach(mst_text)

    flag = True
    # 判断当前所有服务器是否有错
    for client_key, client_value in host_check_status_dict.items():
        for host_item in client_value:
            if host_item['status']['error'] > 0 or host_item['status']['failure'] > 0:
                flag = False
                break

    # 添加邮件标题
    if flag:
        msg['Subject'] = Header(subject, 'UTF-8')
    else:
        msg['Subject'] = Header('Error!!!-' + subject, 'UTF-8')
    msg['From'] = sender
    msg['To'] = receiver
    # 给多个人发送需要使用列表
    receiver_list = receiver.split(',')

    if port == 465:
        # 测试使用,使用SSL
        smtp = smtplib.SMTP_SSL(host=host, port=port)
    else:
        # 线上运行,不使用SSL
        smtp = smtplib.SMTP(host=host, port=port)

    smtp.login(username, password)
    smtp.sendmail(sender, receiver_list, msg.as_string())
    smtp.quit()
    LogConfigure.logging.info('邮件发送成功')


def select_last_report_folder(file_path):
    # 选择文件夹中最新的一个子文件夹
    report_list = os.listdir(file_path)
    report_list = sorted(report_list)
    return report_list[-1]


def send_report(configure_path, host_check_status_dict):
    p_info = read_config(configure_path)
    send_email_html_content(p_info, host_check_status_dict)


if __name__ == '__main__':
    path = os.path.abspath('../../static/report')
    print(select_last_report_folder(path))
    pass
