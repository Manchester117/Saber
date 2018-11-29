import os  # 这里很坑--如果从外部调用Django ORM需要设定os.environ()/django.setup()

from monitor.Saber.WriteReportToDB.calculate_resp import calculate_resp_time

os.environ['DJANGO_SETTINGS_MODULE'] = 'Saber.settings'

import django  # 这里更坑

django.setup()

import datetime
from monitor.Saber.WriteReportToDB.spider_report import get_report_detail_info, get_report_item, get_report_note
from monitor.models import Aggregate, Report, Item, Item_Error, Response_Status


def save_report_batch_aggregate(save_report_list, batch_run_time):
    # 统计的通过,错误,失败的总数
    pass_total_num = 0
    error_total_num = 0
    time_out_total_num = 0
    failure_total_num = 0

    # 统计本次测试的所有数据
    for report in save_report_list:
        report_statistics_num = get_report_note(report['save_report_full_name'])
        pass_total_num += report_statistics_num['pass_num']
        error_total_num += report_statistics_num['error_num']
        # 统计本次测试中所有的超时数量
        time_out_total_num += calculate_resp_time(report['class_resp_status_list'])
        failure_total_num += report_statistics_num['failure_num']

    is_error = False
    if error_total_num + failure_total_num > 0:
        is_error = True

    report_aggregate_info = {
        'batch_run_time': batch_run_time,
        'create_date': datetime.datetime.now().strftime('%Y-%m-%d'),
        'is_error': is_error,
        'pass_total_num': pass_total_num,
        'error_total_num': error_total_num,
        'time_out_total_num': time_out_total_num,
        'failure_total_num': failure_total_num
    }
    # 保存汇总数据
    aggregate = Aggregate.objects.create(**report_aggregate_info)
    aggregate.save()

    # 保存报告数据
    for report in save_report_list:
        report_info = {
            'save_report_full_name': report['save_report_full_name'],
            'host_client': report['host_client'],
            'host_key_ip': report['host_key_ip'],
            'batch_run_time': report['batch_run_time'],
        }
        save_report_info(aggregate, report_info, report['class_resp_status_list'])


def save_report_info(aggregate, report_info, resp_status_list):
    # 获取最新的报告信息
    report_record = get_report_detail_info(report_info['save_report_full_name'],
                                           report_info['host_client'],
                                           report_info['host_key_ip'],
                                           report_info['batch_run_time'])
    # 给要存储的报告信息添加外键
    report_record['aggregate_id'] = aggregate.id
    # print(report_record)
    # 统计本次报告中测试用例超时数量
    model_time_out_num = 0
    for resp_status in resp_status_list:
        model_time_out_num += resp_status['is_timeout']
    report_record['time_out_num'] = model_time_out_num

    # 定义最新报告,并存入DB
    report = Report.objects.create(**report_record)
    report.save()

    # 获取报告日期
    record_date = report_record['create_date']
    # 将报告中的内容保存到Item表
    save_report_item(report, report_info['save_report_full_name'], record_date)

    save_response_status(report, resp_status_list)


def save_response_status(report, resp_status_list):
    for resp_status in resp_status_list:
        resp_status['report_id'] = report.id
        resp_status_info = Response_Status.objects.create(**resp_status)
        resp_status_info.save()


def save_report_item(report, save_report_full_name, record_date):
    item_dict, error_dict = get_report_item(save_report_full_name)
    for model_name, error_flag in item_dict.items():
        # print(model_name.split('.')[-1], error_flag)
        report_item = {
            'model_name': model_name.split('.')[-1],
            'record_date': record_date,
            'error_flag': error_flag,
            'report_id': report.id  # 外键关联保存
        }

        item = Item.objects.create(**report_item)
        item.save()

        # 保存Error的item
        if model_name in error_dict:
            save_error_item(item, error_dict[model_name], record_date)


def save_error_item(item, error_item_dict, record_date):
    # 保存错误的测试条目,并保存错误类型
    for error_item_key, error_item_value in error_item_dict.items():
        error_item = {
            'model_name': item.model_name,
            'item_name': error_item_key,
            'error_type_flag': error_item_value,
            'record_date': record_date,
            'item_id': item.id  # 外键关联保存
        }

        item_error = Item_Error.objects.create(**error_item)
        item_error.save()


# 写入数据库测试
# if __name__ == '__main__':
#     now_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
#     save_report_title(os.path.join(os.path.abspath('.'), 'monitor', 'static', 'report', now_time))
