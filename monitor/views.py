import json
import os
from datetime import datetime, timedelta, time

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from monitor.Saber.GetNewCookie import GetUserCookie
from monitor.Saber.VIKRunModule.RunTestControl import run_multiple_test
from monitor.models import Aggregate, Report, Item, Item_Error, Case, Response_Status

# 任务计划对象-全局变量(真不想定义这个全局变量)
test_run_schedule = None
refresh_cookie_run_schedule = None


def index(request):
    aggregate_id = request.GET.get('aggregate_id')

    status_c_list = list()
    status_b_list = list()
    status_h_list = list()
    status_j_list = list()
    status_w_list = list()
    status_m_list = list()
    status_r_list = list()

    get_last_item_sql = '''
                            SELECT *
                            FROM monitor_report
                            WHERE aggregate_id = (
                                SELECT id 
                                FROM monitor_aggregate
                                ORDER BY id DESC LIMIT 1
                            )
                        '''
    if aggregate_id is not None:
        get_last_item_sql = 'SELECT * FROM monitor_report WHERE aggregate_id = {0}'.format(aggregate_id)
    report_collect = Report.objects.raw(get_last_item_sql)
    if report_collect is None:
        return render(request, template_name='index.html')
    else:
        for report in report_collect:
            aggregate_id = report.aggregate_id      # 获取汇总报告id
            if report.report_comp == 'C端':
                status_c_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
            if report.report_comp == 'B端':
                status_b_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
            if report.report_comp == 'H端':
                status_h_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
            if report.report_comp == 'J端':
                status_j_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
            if report.report_comp == 'W端':
                status_w_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
            if report.report_comp == 'M端':
                status_m_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
            if report.report_comp == 'R端':
                status_r_list.append({
                    'report_id': report.id,
                    'report_name': report.report_name,
                    'host_ip': report.host_ip,
                    'error_num': report.error_num,
                    'time_out_num': report.time_out_num,
                    'failure_num': report.failure_num,
                    'pass_num': report.pass_num,
                    'time': datetime.strftime(report.create_date, "%Y-%m-%d") + ' ' + time.strftime(report.create_time,
                                                                                                    "%H:%M:%S")
                })
    return render(request, template_name='index.html', context={
        'aggregate_id': aggregate_id,
        'status_c_list': status_c_list,
        'status_b_list': status_b_list,
        'status_h_list': status_h_list,
        'status_j_list': status_j_list,
        'status_w_list': status_w_list,
        'status_m_list': status_m_list,
        'status_r_list': status_r_list
    })


def detail_report(request):
    aggregate_id = request.GET.get('aggregate_id')
    report_id = request.GET.get('report_id')
    report_name = request.GET.get('report_name')
    # 通过报告名称在库中查找报告路径
    report_query = Report.objects.filter(report_name=report_name)
    report_path = None
    for report in report_query:
        # 查找路径
        report_path = report.report_path
    if report_path is not None:
        report_path = report_path.split(os.sep)[-1]
    else:
        # 如果路径为空
        return render(request, template_name='detail_report.html')
    return render(request, template_name='detail_report.html', context={
        'aggregate_id': aggregate_id,
        'report_name': report_name,
        'report_id': report_id,
        'report_full_name': report_path + os.sep + report_name
    })


def response_report(request):
    aggregate_id = request.GET.get('aggregate_id')
    report_id = request.GET.get('report_id')
    report_name = request.GET.get('report_name')
    # 从DB中查找当前报告的超时记录
    response_query = Response_Status.objects.filter(report_id=report_id)
    response_info_list = list()
    for query_info in response_query:
        query_item_dict = dict()
        query_item_dict['id'] = query_info.id
        query_item_dict['model_name'] = query_info.model_name
        query_item_dict['item_name'] = query_info.item_name
        query_item_dict['url'] = query_info.url
        query_item_dict['resp_duration'] = query_info.resp_duration
        query_item_dict['req_time'] = query_info.req_time.strftime("%Y-%m-%d %H:%M:%S")
        query_item_dict['status_code'] = query_info.status_code
        query_item_dict['is_timeout'] = '是' if query_info.is_timeout is True else '否'
        response_info_list.append(query_item_dict)
    return render(request, template_name='response_report.html', context={
        'aggregate_id': aggregate_id,
        'report_name': report_name,
        'report_id': report_id,
        'response_info_list': response_info_list
    })


def response_content(request):
    aggregate_id = request.GET.get('aggregate_id')
    resp_status_id = request.GET.get('resp_status_id')
    resp_query = Response_Status.objects.get(id=resp_status_id)
    resp_content = resp_query.resp_content
    return render(request, template_name='response_content.html', context={
        'aggregate_id': aggregate_id,
        'resp_content': resp_content
    })


def aggregate_filter(aggregate_from_db, aggregate_id, create_date, is_error):
    if is_error == '':
        # 如果'是否出错'字段为空则只是用前面两个条件进行搜索
        if aggregate_id is '' and create_date is '':
            aggregate_from_db = Aggregate.objects.filter()
        elif aggregate_id is not '' and create_date is '':
            aggregate_from_db = Aggregate.objects.filter(id=aggregate_id)
        elif aggregate_id is '' and create_date is not '':
            aggregate_from_db = Aggregate.objects.filter(create_date=create_date)
        elif aggregate_id is not '' and create_date is not '':
            aggregate_from_db = Aggregate.objects.filter(id=aggregate_id, create_date=create_date)
    else:
        # 如果'是否出错'字段不为空,则使用全部条件进行搜索
        if aggregate_id is '' and create_date is '':
            aggregate_from_db = Aggregate.objects.filter(is_error=is_error)
        elif aggregate_id is not '' and create_date is '':
            aggregate_from_db = Aggregate.objects.filter(id=aggregate_id, is_error=is_error)
        elif aggregate_id is '' and create_date is not '':
            aggregate_from_db = Aggregate.objects.filter(create_date=create_date, is_error=is_error)
        elif aggregate_id is not '' and create_date is not '':
            aggregate_from_db = Aggregate.objects.filter(id=aggregate_id, create_date=create_date, is_error=is_error)
    return aggregate_from_db


def aggregate_list(request):
    page_no = request.GET.get('page_no')
    aggregate_id = request.POST.get('aggregate_id')
    create_date = request.POST.get('create_date')
    is_error = request.POST.get('is_error')

    # 默认获得第一页的数据
    if page_no is None:
        page_no = 1
    # 如果得到None字符串,需要检查get方式下是否能获取参数
    if aggregate_id is None:
        aggregate_id = request.GET.get('report_id')
        # 如果get方式下获取的是None,用空字符串代替
        if aggregate_id is None:
            aggregate_id = ''
    if create_date is None:
        create_date = request.GET.get('create_date')
        if create_date is None:
            create_date = ''
    if is_error is None:
        is_error = request.GET.get('is_error')
        if is_error is None:
            is_error = ''

    aggregate_from_db = None
    # 根据'是否出错'分成三种情况调用方法
    if is_error == 'true':
        aggregate_from_db = aggregate_filter(aggregate_from_db, aggregate_id, create_date, True)
    elif is_error == 'false':
        aggregate_from_db = aggregate_filter(aggregate_from_db, aggregate_id, create_date, False)
    elif is_error == '' or is_error is None:
        aggregate_from_db = aggregate_filter(aggregate_from_db, aggregate_id, create_date, '')

    # 分页(每一页显示多少报告)
    paginator = Paginator(aggregate_from_db, 15)
    # 获取总共多少页
    num_pages = paginator.num_pages

    try:
        aggregates_list = paginator.page(page_no)
    except PageNotAnInteger:
        # 如果页码不是整型数字
        aggregates_list = paginator.page(1)
    except EmptyPage:
        # 如果页码超出了记录范围,则返回最后一页
        aggregates_list = paginator.page(paginator.num_pages)

    return render(request, template_name='reports_list.html', context={
        'aggregates_list': aggregates_list,
        'page_no': page_no,
        'num_pages': num_pages,
        # 搜索条件
        'aggregate_id': aggregate_id,
        'create_date': create_date,
        'is_error': is_error
    })


def agency_date_fetch(agency_type, end_date_str, begin_date_str):
    if end_date_str is '' or begin_date_str is '':
        # 字符串转日期
        end_date = datetime.today()
        # 日期减法,获取7天前日期
        begin_date = end_date - timedelta(days=6)
        # 日期转字符串
        begin_date_str = begin_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

    query_sql = '''
        SELECT id, create_date, SUM(pass_num) pass_num, SUM(error_num) error_num, SUM(failure_num) failure_num
        FROM monitor_report
        WHERE create_date BETWEEN {0} AND {1}
        AND report_comp = {2} 
        GROUP BY create_date;
    '''.format("'" + begin_date_str + "'", "'" + end_date_str + "'", "'" + agency_type + "'")

    return query_sql, begin_date_str, end_date_str


def agency_aggregate_num(request):
    agency_type = request.POST.get('agency_type')
    end_date_str = request.POST.get('end_date_str')
    begin_date_str = request.POST.get('begin_date_str')

    if agency_type is None:
        agency_type = 'B端'
    if end_date_str is None:
        end_date_str = ''
    if begin_date_str is None:
        begin_date_str = ''
    # 对每个端以天为单位做通过/错误/失败的汇总
    query_sql, begin_date_str, end_date_str = agency_date_fetch(agency_type, end_date_str, begin_date_str)

    create_date_list = list()
    sum_pass_list = list()
    sum_error_list = list()
    sum_failure_list = list()

    for collection in Report.objects.raw(query_sql):
        create_date_list.append(datetime.strftime(collection.create_date, '%Y-%m-%d'))
        sum_pass_list.append(int(collection.pass_num))
        sum_error_list.append(int(collection.error_num))
        sum_failure_list.append(int(collection.failure_num))

    return render(request, template_name='agency_aggregate_chart.html', context={
        'create_date_list': json.dumps(create_date_list),
        'sum_pass_list': json.dumps(sum_pass_list),
        'sum_error_list': json.dumps(sum_error_list),
        'sum_failure_list': json.dumps(sum_failure_list),
        # 搜索条件
        'agency_type': agency_type,
        'end_date_str': end_date_str,
        'begin_date_str': begin_date_str
    })


def agency_error_type(request):
    end_date_str = request.POST.get('end_date_str')
    begin_date_str = request.POST.get('begin_date_str')

    if end_date_str is None:
        end_date_str = ''
    if begin_date_str is None:
        begin_date_str = ''

    if end_date_str is '' or begin_date_str is '':
        # 字符串转日期
        end_date = datetime.today()
        # 日期减法,获取7天前日期
        begin_date = end_date - timedelta(days=6)
        # 日期转字符串
        begin_date_str = begin_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')
    # 统计每一端的错误数量
    query_sql = '''
        SELECT 
          item_error.id, 
          report.report_comp, 
          item_error.error_type_flag, 
          COUNT(item_error.error_type_flag) error_type_flag_value
        FROM monitor_item_error item_error
        LEFT JOIN monitor_item item ON item.id = item_error.item_id
        LEFT JOIN monitor_report report ON report.id = item.report_id
        WHERE item_error.record_date BETWEEN {0} AND {1}
        GROUP BY report.report_comp, item_error.error_type_flag;
    '''.format("'" + begin_date_str + "'", "'" + end_date_str + "'")

    agency_list = ['B端', 'C端', 'H端', 'J端', 'W端', 'M端', 'R端']
    list_502 = [0] * 6
    list_404 = [0] * 6
    list_timeout = [0] * 6
    unknown_error_list = [0] * 6

    for agency_index in range(len(agency_list)):
        for error_item in Item_Error.objects.raw(query_sql):
            if agency_list[agency_index] == error_item.report_comp:
                if error_item.error_type_flag == 1:
                    list_502[agency_index] = error_item.error_type_flag_value
                if error_item.error_type_flag == 2:
                    list_404[agency_index] = error_item.error_type_flag_value
                if error_item.error_type_flag == 3:
                    list_timeout[agency_index] = error_item.error_type_flag_value
                if error_item.error_type_flag == 4:
                    unknown_error_list[agency_index] = error_item.error_type_flag_value

    return render(request, template_name='agency_error_type_chart.html', context={
        'agency_list': json.dumps(agency_list),
        'list_502': json.dumps(list_502),
        'list_404': json.dumps(list_404),
        'list_timeout': json.dumps(list_timeout),
        'unknown_error_list': json.dumps(unknown_error_list),
        # 搜索条件
        'end_date_str': end_date_str,
        'begin_date_str': begin_date_str
    })


def agency_machine_statistic(request):
    agency_type = request.POST.get('agency_type')
    end_date_str = request.POST.get('end_date_str')
    begin_date_str = request.POST.get('begin_date_str')

    if agency_type is None:
        agency_type = 'B端'
    if end_date_str is None:
        end_date_str = ''
    if begin_date_str is None:
        begin_date_str = ''

    if end_date_str is '' or begin_date_str is '':
        # 字符串转日期
        end_date = datetime.today()
        # 日期减法,获取7天前日期
        begin_date = end_date - timedelta(days=6)
        # 日期转字符串
        begin_date_str = begin_date.strftime('%Y-%m-%d')
        end_date_str = end_date.strftime('%Y-%m-%d')

    query_sql = '''
        SELECT 
            id, host_ip, 
            SUM(pass_num) pass_total_num, 
            SUM(error_num) error_total_num, 
            SUM(failure_num) failure_num
        FROM monitor_report
        WHERE create_date BETWEEN {0} AND {1}
        AND report_comp = {2}
        GROUP BY host_ip 
    '''.format("'" + begin_date_str + "'", "'" + end_date_str + "'", "'" + agency_type + "'")

    machine_ip_list = list()
    machine_pass_list = list()
    machine_error_list = list()
    machine_failure_list = list()
    for machine in Report.objects.raw(query_sql):
        machine_ip_list.append(machine.host_ip)
        machine_pass_list.append(int(machine.pass_total_num))
        machine_error_list.append(int(machine.error_total_num))
        machine_failure_list.append(int(machine.failure_num))

    return render(request, template_name='agency_machine_statistics.html', context={
        'machine_ip_list': json.dumps(machine_ip_list),
        'machine_pass_list': json.dumps(machine_pass_list),
        'machine_error_list': json.dumps(machine_error_list),
        'machine_failure_list': json.dumps(machine_failure_list),
        # 搜索条件
        'agency_type': agency_type,
        'begin_date_str': begin_date_str,
        'end_date_str': end_date_str
    })


def cases_list(request):
    page_no = request.GET.get('page_no')
    case_name = request.POST.get('case_name')

    # 默认获得第一页的数据
    if page_no is None:
        page_no = 1

    # 如果Post提交的表单数据中case_name的值为None,则检查Get提交的case_name
    if case_name is None:
        case_name = request.GET.get('case_name')
        # 如果Get提交的case_name依然为None,则将case_name置为''
        if case_name is None:
            case_name = ''

    if case_name != '' and case_name is not None:
        # 使用__contains进行模糊搜索
        case_from_db = Case.objects.filter(case_name__contains=case_name)
    else:
        case_from_db = Case.objects.filter()

    # 分页(每一页显示多少用例)
    paginator = Paginator(case_from_db, 10)
    # 获取总共多少页
    num_pages = paginator.num_pages

    try:
        case_list = paginator.page(page_no)
    except PageNotAnInteger:
        # 如果页码不是整型数字
        case_list = paginator.page(1)
    except EmptyPage:
        # 如果页码超出了记录范围,则返回最后一页
        case_list = paginator.page(paginator.num_pages)

    return render(request, template_name='cases_list.html', context={
        'case_list': case_list,
        'page_no': page_no,
        'num_pages': num_pages,
        'case_name': case_name  # 搜索条件
    })


def case_view(request):
    case_id = request.GET.get("case_id")
    page_no = request.GET.get("page_no")
    case_name = request.GET.get('case_name')

    view_case = Case.objects.filter(id=case_id)
    case_full_path = ''
    for case_info in view_case:
        path = case_info.case_folder_path
        name = case_info.case_name
        case_full_path = path + os.sep + name
    with open(case_full_path, 'r', encoding='UTF-8') as f:
        case_lines_content = f.readlines()
    case_content = ''
    for case_line in case_lines_content:
        case_content = case_content + case_line

    return render(request, template_name='view_case.html', context={
        'case_content': case_content,
        'page_no': page_no,
        'case_name': case_name  # 搜索条件
    })


def upload_case(request):
    upload_case_file = request.FILES.get('upload_case')
    # 用例上传路径
    case_folder_path = os.path.dirname(__file__) + '/static/testcase'
    # 利用绝对路径确定保存位置
    with open(case_folder_path + os.sep + upload_case_file.name, 'wb+') as destination:
        for chunk in upload_case_file.chunks():
            destination.write(chunk)
    # 获取上传时间
    # case_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    case_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    case_record = {'case_folder_path': case_folder_path, 'case_name': upload_case_file.name, 'case_time': case_time}
    # 将报告写入到数据库
    case = Case.objects.create(**case_record)
    case.save()
    # 页面重定向
    return redirect('/monitor/cases_list/')


def delete_case(request):
    case_id = request.GET.get('case_id')
    # 根据ID查找用例
    del_case = Case.objects.get(id=case_id)

    test_case_folder_path = os.path.join(os.path.dirname(__file__), 'static', 'testcase')
    test_case_list = os.listdir(test_case_folder_path)

    del_flag = None
    for test_case in test_case_list:
        # 如果在testcase文件夹中能找到这个文件,则进行删除操作
        if del_case.case_name == test_case:
            os.remove(os.path.join(test_case_folder_path, test_case))
            # 删除数据库中的记录
            del_flag = del_case.delete()
    # 如果用例已经在文件夹中删除,但是库中还留有记录,那么直接删除库中的记录
    if del_flag is None:
        del_case.delete()
    # 显示删除标志位 -- 调试使用
    # print(del_flag[0])

    return redirect('/monitor/cases_list/')


def test_operate(request):
    return render(request, template_name='test_operate.html', context={})


def run_test(request):
    run_multiple_test()  # 运行测试(按Host运行)
    return render(request, template_name='test_operate.html', context={})


class SingletonDecorator:
    """
    单例模式装饰类
    """

    def __init__(self, parameter):
        self.parameter = parameter
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.parameter(*args, **kwargs)
        return self.instance


class RefreshCookieScheduleTask:
    """
    声明测试运行的任务计划类
    """
    refresh_cookie_schedule = BackgroundScheduler()


refresh_cookie_scheduler_obj = SingletonDecorator(RefreshCookieScheduleTask)


def task_refresh_cookie(request):
    """
    更新Cookie的计划任务
    :param request:
    :return:
    """
    cron_list = None
    task_flag = json.loads(request.body.decode())
    if 'run_cron' in task_flag:
        cron_str = task_flag['run_cron'].strip()
        if cron_str != '':
            cron_list = cron_str.split(' ')
        else:
            cron_list = ['*', '10', '0', '*', '*', '*']
    global refresh_cookie_run_schedule  # 使用全局变量
    if refresh_cookie_run_schedule is None:
        if task_flag['run_flag'] == 'start_run':
            refresh_cookie_run_schedule = refresh_cookie_scheduler_obj().refresh_cookie_schedule
            refresh_cookie_run_schedule.add_job(
                refresh_cookie,  # 任务方法
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5],
                id='schedule_refresh_cookie'
            )
            refresh_cookie_run_schedule.start()
    else:
        # 如果计划任务已经启动,有两个分支.
        # 1.修改当前任务的执行周期
        # 2.停止当前任务
        if task_flag['run_flag'] == 'start_run':
            refresh_cookie_run_schedule.resume()  # 计划任务恢复-对应任务暂停
            refresh_cookie_run_schedule.reschedule_job(
                job_id='schedule_refresh_cookie',
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5]
            )
        elif task_flag['run_flag'] == 'stop_run':
            refresh_cookie_run_schedule.pause()  # 计划任务暂停

    return render(request, template_name='test_operate.html', context={})


def once_refresh_cookie(request):
    '''
    :description: 立即更新cookie
    :param request: 
    :return: 
    '''
    refresh_cookie()
    return render(request, template_name='test_operate.html', context={})


def refresh_cookie():
    """
    调用更新Cookie方法
    :return:
    """
    print('Refresh_Cookie ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print(os.path.join(os.path.dirname(__file__), 'static', 'testcase'))
    GetUserCookie.search_cookie(os.path.join(os.path.dirname(__file__), 'static', 'testcase'))


class TestScheduleTask:
    """
    声明测试运行的任务计划类
    """
    test_schedule = BackgroundScheduler()


test_scheduler_obj = SingletonDecorator(TestScheduleTask)


def task_run_test(request):
    """
    执行测试的计划任务
    :param request:
    :return:
    """
    cron_list = None
    # Ajax传过来的json是二进制字符串,需要用decode()转成字符串
    task_flag = json.loads(request.body.decode())
    if 'run_cron' in task_flag:
        cron_str = task_flag['run_cron'].strip()
        if cron_str != '':
            cron_list = cron_str.split(' ')
        else:
            # 如果为空则默认以每隔20分钟运行一次的规则运行
            cron_list = ['*', '*/20', '*', '*', '*', '*']
    global test_run_schedule  # 使用全局变量
    if test_run_schedule is None:
        # 如果计划任务还没有启动,则启动计划任务
        if task_flag['run_flag'] == 'start_run':
            test_run_schedule = test_scheduler_obj().test_schedule
            test_run_schedule.add_job(
                start_test,  # 任务方法
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5],
                id='schedule_test'
            )
            test_run_schedule.start()
    else:
        # 如果计划任务已经启动,有两个分支.
        # 1.修改当前任务的执行周期
        # 2.停止当前任务
        if task_flag['run_flag'] == 'start_run':
            test_run_schedule.resume()  # 计划任务恢复-对应任务暂停
            test_run_schedule.reschedule_job(
                job_id='schedule_test',
                trigger='cron',
                second=cron_list[0],
                minute=cron_list[1],
                hour=cron_list[2],
                day=cron_list[3],
                week=cron_list[4],
                month=cron_list[5]
            )
        elif task_flag['run_flag'] == 'stop_run':
            test_run_schedule.pause()  # 计划任务暂停

    return render(request, template_name='test_operate.html', context={})


def start_test():
    """
    调用测试方法
    :return:
    """
    print('定时操作_Task_Test ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    run_multiple_test()  # 运行测试(按Host运行)
