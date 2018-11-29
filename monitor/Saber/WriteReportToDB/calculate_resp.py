def calculate_resp_time(class_resp_status_list):
    report_response_status_num = 0
    for resp_status in class_resp_status_list:
        report_response_status_num += resp_status['is_timeout']
    return report_response_status_num
