from django.conf.urls import url
from monitor import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^detail_report/', views.detail_report, name='detail_report'),
    url(r'^response_report/', views.response_report, name='response_report'),
    url(r'^response_content/', views.response_content, name='response_content'),
    url(r'^aggregate_list/', views.aggregate_list, name='aggregate_list'),
    url(r'^agency_aggregate_num/', views.agency_aggregate_num, name='agency_aggregate_num'),
    url(r'^agency_error_type/', views.agency_error_type, name='agency_error_type'),
    url(r'^agency_machine_statistic/', views.agency_machine_statistic, name='agency_machine_statistic'),
    url(r'^cases_list/', views.cases_list, name='cases_list'),
    url(r'^case_view/', views.case_view, name='case_view'),
    url(r'^upload_case/', views.upload_case, name='upload_case'),
    url(r'^delete_case/', views.delete_case, name='delete_case'),
    url(r'^test_operate/', views.test_operate, name='test_operate'),
    url(r'^run_test/', views.run_test, name='run_test'),
    url(r'^once_refresh_cookie/', views.once_refresh_cookie, name='once_refresh_cookie'),
    url(r'^task_refresh_cookie/', views.task_refresh_cookie, name='task_refresh_cookie'),
    url(r'^task_run_test/', views.task_run_test, name='task_run_test'),
]

