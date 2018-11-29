from django.db import models

# Create your models here.


class Aggregate(models.Model):
    batch_run_time = models.DateTimeField('运行时间')
    create_date = models.DateField('生成日期')
    is_error = models.BooleanField('是否有错', default=False)
    pass_total_num = models.IntegerField('成功总量', default=0)
    error_total_num = models.IntegerField('错误总量', default=0)
    time_out_total_num = models.IntegerField('超时总量', default=0)
    failure_total_num = models.IntegerField('失败总量', default=0)

    def __str__(self):
        return self.batch_run_time

    class Meta:
        ordering = ['-batch_run_time']


class Report(models.Model):
    aggregate = models.ForeignKey(Aggregate, on_delete=models.CASCADE)
    report_name = models.CharField('报告名称', max_length=200)
    report_path = models.CharField('报告路径', max_length=400)
    report_comp = models.CharField('报告应用', max_length=50)
    create_date = models.DateField('生成日期')
    create_time = models.TimeField('生成时间')
    host_ip = models.CharField('IP地址', max_length=16)
    is_error = models.BooleanField('是否有错', default=False)
    pass_num = models.IntegerField('成功数量', default=0)
    error_num = models.IntegerField('错误数量', default=0)
    time_out_num = models.IntegerField('超时数量', default=0)
    failure_num = models.IntegerField('失败数量', default=0)
    batch_run_time = models.DateTimeField('运行时间')

    def __str__(self):
        return self.report_name

    class Meta:
        # 表示按照运行时间逆序倒排
        ordering = ['-aggregate']


class Item(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    model_name = models.CharField('模块名称', max_length=300)
    record_date = models.DateField('记录日期')
    error_flag = models.IntegerField('服务错误标志位')

    def __str__(self):
        return self.model_name

    class Meta:
        ordering = ['-report']  # 按照外键倒排


class Item_Error(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    model_name = models.CharField('模块名称', max_length=300)
    item_name = models.CharField('条目名称', max_length=300)
    error_type_flag = models.IntegerField('错误类型')
    record_date = models.DateField('记录时间')

    def __str__(self):
        return self.item_name

    class Meta:
        ordering = ['-item']    # 按照外键倒排


class Response_Status(models.Model):
    report = models.ForeignKey(Report, on_delete=models.CASCADE)
    ip = models.CharField('服务器IP', max_length=16)
    model_name = models.CharField('模块名称', max_length=300)
    item_name = models.CharField('条目名称', max_length=300)
    url = models.CharField('请求URL', max_length=1024)
    resp_content = models.TextField('请求返回内容')
    resp_duration = models.CharField('响应时间', max_length=16)
    req_time = models.DateTimeField('请求发起时间')
    status_code = models.CharField('返回状态码', max_length=4)
    is_timeout = models.BooleanField('是否超时', default=False)

    def __str__(self):
        return self.ip

    class Meta:
        ordering = ['-report']  # 按照外键倒排


class Case(models.Model):
    case_folder_path = models.CharField('用例路径', max_length=300)
    case_name = models.CharField('用例名称', max_length=300)
    case_time = models.DateTimeField('上传时间')

    def __str__(self):
        return self.case_name

    class Meta:
        ordering = ['-case_name']   # 按照用例名称排序
