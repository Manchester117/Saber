import os
import re
import zipfile


def report_compress(report_path):
    # 对报告进行压缩
    report_folder = report_path.split(os.sep)[-1]
    report_folder_zip_path = os.path.abspath(os.path.join('monitor', 'static', 'zip'))
    f = zipfile.ZipFile(report_folder_zip_path + os.sep + report_folder + '.zip', 'w', zipfile.ZIP_DEFLATED)
    # 获取被压缩文件下的所有报告
    report_list = os.listdir(report_path)
    for report in report_list:
        f.write(report_path + os.sep + report)
    # 获取报告绝对路径
    zip_report_full_path = os.path.abspath(f.filename)
    f.close()
    return zip_report_full_path


def report_filter(report_path):
    # 读取报告,并进行过滤
    with open(report_path, 'r', encoding='UTF-8') as f:
        content = f.read()
    # 去掉异常信息
    content = re.sub('<pre>.*?</pre>', '', content, flags=re.DOTALL)
    # 去掉JS
    # re.DOTALL为多行匹配
    content = re.sub('<script language="javascript" type="text/javascript">.*?</script>', '', content, flags=re.DOTALL)
    # print(content)
    report_name = 'lite_' + report_path.split(os.sep)[-1]
    lite_report_folder_path = os.path.abspath(os.path.join('monitor', 'static', 'lite'))
    lite_report_path = lite_report_folder_path + os.sep + report_name
    # 将过滤后的报告写入文件
    with open(lite_report_path, 'w+', encoding='UTF-8') as f:
        f.write(content)
    return lite_report_path


if __name__ == '__main__':
    report_compress('../../static/report/result_2017-04-14_10-55-00.html')

