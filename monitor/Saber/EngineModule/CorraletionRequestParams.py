# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'

import re
from monitor.Saber.LogModule import LogConfigure


def corr_match(self, resp_cont):
    """
    :description: 如果当前请求中的关联匹配不为空,则进行关联匹配替换,将关联匹配替换为关联值,并且替换找到的关联值
    :param resp_cont: 请求返回值
    :return:
    """
    if self.corr_list[self.__class__.index] is not None:
        corr_params = self.corr_list[self.__class__.index]
        # 在当前请求中遍历关联值
        for key, value in corr_params.items():
            match_obj = re.search(corr_params[key], resp_cont)
            if match_obj is not None:
                target_param = match_obj.group(1)
                # 在原数据结构中对关联值进行替换
                corr_params[key] = target_param
                # 对URL参数进行过滤
                corr_replace_url(self, corr_params, key)
                # 执行参数过滤
                true_req_params_list = corr_filter_dict(self)
                # 执行参数替换
                corr_replace_dict(corr_params, key, true_req_params_list)


def corr_replace_url(self, corr_params, key):
    """
    :description: 如果有后续请求的URL有关联值,则进行替换
    :param corr_params: 原数据结构中的关联匹配字典
    :param key: 关联匹配字典的key
    :return:
    """
    index = self.__class__.index
    original_param = '{' + key + '}'
    for req_item in self.req_data_list[index:]:
        if key in req_item['url']:
            req_item['url'] = req_item['url'].replace(original_param, corr_params[key])


def corr_filter_dict(self):
    """
    :description: 对后续请求的参数进行过滤,过滤掉None,将不为None的请求字典加入到列表当中
    :return: 返回请求列表
    """
    # 定义参数过滤列表
    true_req_params_list = []
    index = self.__class__.index
    # 将参数进行过滤,过滤掉为None的参数,并加入到列表中
    for req_item in self.req_data_list[index:]:
        if req_item['getParams'] is not None:
            true_req_params_list.append(req_item['getParams'])
        if req_item['postParams'] is not None:
            true_req_params_list.append(req_item['postParams'])
        if req_item['json'] is not None:
            true_req_params_list.append(req_item['json'])
    return true_req_params_list


def corr_replace_dict(corr_params, key, true_req_params_list):
    """
    :description: 对get,post,json请求数据进行替换
    :param corr_params: 原数据结构中的关联匹配字典--已经替换完成
    :param key: 要替换关联值的key
    :param true_req_params_list: 请求参数的列表
    :return:
    """
    # 执行参数替换
    for req_params_item in true_req_params_list:
        for req_params_key, req_params_value in req_params_item.items():
            # 如果关联的值是字符串,则用以下逻辑进行替换关联值
            if isinstance(req_params_item[req_params_key], str):
                if key in req_params_item[req_params_key]:
                    req_params_item[req_params_key] = corr_params[key]
            # 如果关联的值是数字,还需要进一步改进代码
