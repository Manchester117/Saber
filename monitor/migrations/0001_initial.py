# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aggregate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_run_time', models.DateTimeField(verbose_name='运行时间')),
                ('create_date', models.DateField(verbose_name='生成日期')),
                ('is_error', models.BooleanField(default=False, verbose_name='是否有错')),
                ('pass_total_num', models.IntegerField(default=0, verbose_name='成功总量')),
                ('error_total_num', models.IntegerField(default=0, verbose_name='错误总量')),
                ('time_out_total_num', models.IntegerField(default=0, verbose_name='超时总量')),
                ('failure_total_num', models.IntegerField(default=0, verbose_name='失败总量')),
            ],
            options={
                'ordering': ['-batch_run_time'],
            },
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_folder_path', models.CharField(max_length=300, verbose_name='用例路径')),
                ('case_name', models.CharField(max_length=300, verbose_name='用例名称')),
                ('case_time', models.DateTimeField(verbose_name='上传时间')),
            ],
            options={
                'ordering': ['-case_name'],
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=300, verbose_name='模块名称')),
                ('record_date', models.DateField(verbose_name='记录日期')),
                ('error_flag', models.IntegerField(verbose_name='服务错误标志位')),
            ],
            options={
                'ordering': ['-report'],
            },
        ),
        migrations.CreateModel(
            name='Item_Error',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=300, verbose_name='模块名称')),
                ('item_name', models.CharField(max_length=300, verbose_name='条目名称')),
                ('error_type_flag', models.IntegerField(verbose_name='错误类型')),
                ('record_date', models.DateField(verbose_name='记录时间')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Item')),
            ],
            options={
                'ordering': ['-item'],
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_name', models.CharField(max_length=200, verbose_name='报告名称')),
                ('report_path', models.CharField(max_length=400, verbose_name='报告路径')),
                ('report_comp', models.CharField(max_length=50, verbose_name='报告应用')),
                ('create_date', models.DateField(verbose_name='生成日期')),
                ('create_time', models.TimeField(verbose_name='生成时间')),
                ('host_ip', models.CharField(max_length=16, verbose_name='IP地址')),
                ('is_error', models.BooleanField(default=False, verbose_name='是否有错')),
                ('pass_num', models.IntegerField(default=0, verbose_name='成功数量')),
                ('error_num', models.IntegerField(default=0, verbose_name='错误数量')),
                ('time_out_num', models.IntegerField(default=0, verbose_name='超时数量')),
                ('failure_num', models.IntegerField(default=0, verbose_name='失败数量')),
                ('batch_run_time', models.DateTimeField(verbose_name='运行时间')),
                ('aggregate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Aggregate')),
            ],
            options={
                'ordering': ['-aggregate'],
            },
        ),
        migrations.CreateModel(
            name='Response_Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=16, verbose_name='服务器IP')),
                ('model_name', models.CharField(max_length=300, verbose_name='模块名称')),
                ('item_name', models.CharField(max_length=300, verbose_name='条目名称')),
                ('url', models.CharField(max_length=1024, verbose_name='请求URL')),
                ('resp_content', models.TextField(verbose_name='请求返回内容')),
                ('resp_duration', models.CharField(max_length=16, verbose_name='响应时间')),
                ('req_time', models.DateTimeField(verbose_name='请求发起时间')),
                ('status_code', models.CharField(max_length=4, verbose_name='返回状态码')),
                ('is_timeout', models.BooleanField(default=False, verbose_name='是否超时')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Report')),
            ],
            options={
                'ordering': ['-report'],
            },
        ),
        migrations.AddField(
            model_name='item',
            name='report',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitor.Report'),
        ),
    ]
