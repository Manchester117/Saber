# -*- coding: utf-8 -*-
__author__ = 'Peng.Zhao'


def verify_function(self, resp_content):
    """
    :description: 根据测试用例当中verify,封装的验证方法
    :param resp_content:
    :return:
    """
    index = self.__class__.index
    # 如果接口验证列表不为None并且返回也不为None,则进行验证判断
    if self.verify_list[index] is not None and resp_content is not None:
        resp_content = resp_content.replace('\r\n', '')
        for verify_item in self.verify_list[index]:
            if verify_item[0] == 'isContain':
                self.assertIn(verify_item[1], resp_content)
            elif verify_item[0] == 'isTrue':
                self.assertTrue(verify_item[1])
            elif verify_item[0] == 'isEqual':
                self.assertEqual(verify_item[1], resp_content)
            elif verify_item[0] == 'isNotContain':
                self.assertNotIn(verify_item[1], resp_content)
            elif verify_item[0] == 'isFalse':
                self.assertFalse(verify_item[1])
            elif verify_item[0] == 'isNotEqual':
                self.assertNotEqual(verify_item[1], resp_content)
            else:
                raise AssertionError('无效的验证方法!')
