import os
from bs4 import BeautifulSoup, Tag


def get_report_note(report_full_name):
    pass_num = 0
    error_num = 0
    failure_num = 0

    with open(report_full_name, encoding='UTF-8') as f:
        report_content = f.read()
    soup = BeautifulSoup(report_content, 'lxml')
    report_status_num = soup.select('div.heading > p.attribute')

    # [1:-1]为了只取通过/失败/错误
    report_status_str_array = report_status_num[3].text.split('，')[1:-1]

    for status_item in report_status_str_array:
        if '通过' in status_item:
            pass_num = int(status_item.split(' ')[1])
        if '错误' in status_item:
            error_num = int(status_item.split(' ')[1])
        if '失败' in status_item:
            failure_num = int(status_item.split(' ')[1])

    report_aggregate_num = {
        'pass_num': pass_num,
        'error_num': error_num,
        'failure_num': failure_num
    }
    return report_aggregate_num


def get_report_detail_info(save_report_full_name, host_client, host_key_ip, batch_run_time):
    with open(save_report_full_name, encoding='UTF-8') as f:
        report_content = f.read()

    soup = BeautifulSoup(report_content, 'lxml')
    report_status_num = soup.select('div.heading > p.attribute')

    report_create_time_str_array = report_status_num[1].text.split(' ')
    create_time = report_create_time_str_array[-1]
    create_date = report_create_time_str_array[-2]
    # print(create_date, create_time)

    # [1:-1]为了只取通过/失败/错误
    report_status_str_array = report_status_num[3].text.split('，')[1:-1]
    pass_num = 0
    error_num = 0
    failure_num = 0
    for status_item in report_status_str_array:
        if '通过' in status_item:
            pass_num = int(status_item.split(' ')[1])
        if '错误' in status_item:
            error_num = int(status_item.split(' ')[1])
        if '失败' in status_item:
            failure_num = int(status_item.split(' ')[1])

    is_error = False
    if failure_num + error_num > 0:
        is_error = True

    # 获取报告名称
    report_name = save_report_full_name.split(os.sep)[-1]
    # 获取报告路径
    report_path = os.sep.join(save_report_full_name.split(os.sep)[:-1])
    report_record = {
        'report_name': report_name,
        'report_path': report_path,
        'report_comp': host_client,
        'create_date': create_date,
        'create_time': create_time,
        'host_ip': host_key_ip,
        'is_error': is_error,
        'pass_num': pass_num,
        'error_num': error_num,
        'failure_num': failure_num,
        'batch_run_time': batch_run_time
    }
    return report_record


def get_report_item(save_report_full_name):
    with open(save_report_full_name, encoding='UTF-8') as f:
        report_content = f.read()

    item_dict = dict()
    error_dict = dict()

    soup = BeautifulSoup(report_content, 'lxml')
    item_list = soup.select('tr')
    for item in item_list:
        if 'class' in item.attrs:
            if 'passClass' in item.attrs['class']:
                item_dict[item.td.string] = 0
            if 'errorClass' in item.attrs['class']:
                item_dict[item.td.string] = 1
                # 捕捉带有Error的异常信息,通过兄弟节点获取异常信息 (前方高能预警!!!)
                error_item_dict = dict()
                # 获取当前节点的兄弟节点
                for error_item in item.next_siblings:
                    # 判断元素是不是Tag类型,如果是则进行边界判断,避免打印别的模块的异常信息
                    if isinstance(error_item, Tag):
                        # 在遍历报告是如果已经读取到最后一行的tr,则break.
                        if 'id' in error_item.attrs and error_item.attrs['id'] == 'total_row':
                            break
                        # 在遍历报告时如果样式出现3个中任意1个.则break,代表一条用例中的所有功能项已经遍历完毕
                        if error_item.attrs['class'][0] in ['passClass', 'errorClass', 'failClass']:
                            break
                        # 如果样式是空的,则判断后面有没有pre标签,如果有则将异常信息保存.
                        if error_item.attrs['class'][0] == 'none':
                            error_item_name = error_item.select('.testcase')[0].text
                            if len(error_item.select('div.collapse pre')) != 0:
                                error_item_content = error_item.select('div.collapse pre')[0].text
                                if 'Bad Gateway' in error_item_content:
                                    error_item_dict[error_item_name] = 1
                                elif 'Not Found for url' in error_item_content:
                                    error_item_dict[error_item_name] = 2
                                elif 'Read timed out' in error_item_content:
                                    error_item_dict[error_item_name] = 3
                                else:
                                    error_item_dict[error_item_name] = 4    # 未知错误

                error_dict[item.td.string] = error_item_dict

            if 'failClass' in item.attrs['class']:
                item_dict[item.td.string] = 2
    return item_dict, error_dict


if __name__ == '__main__':
    # get_report_item()
    pass

