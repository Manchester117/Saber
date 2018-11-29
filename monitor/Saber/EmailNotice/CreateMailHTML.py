# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

from yattag import Doc


def create_mail_template(host_check_status_dict):
    b_status_list = host_check_status_dict['B_Client']
    c_status_list = host_check_status_dict['C_Client']
    h_status_list = host_check_status_dict['H_Client']
    j_status_list = host_check_status_dict['J_Client']
    w_status_list = host_check_status_dict['W_Client']
    m_status_list = host_check_status_dict['M_Client']
    r_status_list = host_check_status_dict['R_Client']

    doc, tag, text = Doc().tagtext()

    with tag('html'):
        with tag('head'):
            with tag('meta', ('http-equiv', 'Content-Type'), ('content', 'text/html; charset=UTF-8')):
                pass
        with tag('body'):
            with tag('table', ('width', '1640'), ('border', '0'), ('align', 'center'), ('cellpadding', '0'),
                     ('cellspacing', '0'),
                     ('style', 'font-size:12px;font-family:SimSun;border:1px solid rgb(153,153,153);')):
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:60px;line-height:60px;font-size: 28px;padding-left: 20px;border-bottom:2px solid #000;')):
                        text('巡检结果')
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('C端')
                    create_server_table_template(tag, text, c_status_list)
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('H端')
                    create_server_table_template(tag, text, h_status_list)
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('J端')
                    create_server_table_template(tag, text, j_status_list)
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('W端')
                    create_server_table_template(tag, text, w_status_list)
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('B端')
                    create_server_table_template(tag, text, b_status_list)
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('M端')
                    create_server_table_template(tag, text, m_status_list)
                with tag('tr'):
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        text('R端')
                    create_server_table_template(tag, text, r_status_list)
                with tag('tr'):  # 空出一行
                    with tag('td', ('colspan', '6'), ('style',
                                                      'height:40px;line-height:40px;font-size: 22px;padding-left: 20px;border-bottom:1px solid #d8d8d8;font-weight: bold;')):
                        pass
    return doc


def create_server_table_template(tag, text, status_list):
    with tag('tr'):
        for status in status_list:
            with tag('td', ('style', 'padding-left: 20px;padding-top:20px;')):
                with tag('table', ('cellpadding', '0'), ('cellspacing', '0'),
                         ('style', 'border:1px solid #ccc;')):
                    with tag('tbody'):
                        with tag('tr'):
                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                     ('style',
                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                text('服务IP:')
                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                     ('style',
                                      'color:#ff6600;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                with tag('a', ('href',
                                               'http://monitor.highpin.cn/monitor/detail_report/?report_name={0}'.format(
                                                   status['report_name']))):
                                    text(status['ip'])
                        with tag('tr'):
                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                     ('style',
                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                text('系统错误:')
                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                     ('style',
                                      'color:red;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                text(status['status']['error'])
                        with tag('tr'):
                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                     ('style',
                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                text('请求超时:')
                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                     ('style',
                                      'color:Orange;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                text(status['status']['timeout'])
                        with tag('tr'):
                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                     ('style',
                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                text('验证失败:')
                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                     ('style',
                                      'color:#6d6d00;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                text(status['status']['failure'])
                        with tag('tr'):
                            with tag('td', ('height', '30'), ('width', '80'), ('align', 'left'),
                                     ('style',
                                      'color:#646464;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;padding-left: 10px;')):
                                text('测试通过:')
                            with tag('td', ('height', '30'), ('width', '120'), ('align', 'left'),
                                     ('style',
                                      'color:green;font-size:14px;border-top:1px solid #efeee7;border-bottom:1px solid #efeee7;font-weight:bold;')):
                                text(status['status']['success'])


if __name__ == '__main__':
    doc = create_mail_template()
    print(doc.getvalue())
