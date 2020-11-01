#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import re
import pytest
import allure
from tools.logger import logger
from common.basic.readconfig import ini
from page_object.searchpage import SearchPage


@allure.feature("测试百度模块")
class TestSearch:
    @pytest.fixture(scope='function', autouse=True)
    def open_baidu(self, drivers):
        """打开百度"""
        search = SearchPage(drivers)
        search.get_url(ini.url)

    @allure.story("搜索selenium结果用例")
    def test_001(self, drivers):
        """搜索"""
        search = SearchPage(drivers)
        search.input_search("selenium")
        search.click_search()
        result = re.search(r'selenium', search.get_source)
        logger.info(result)
        assert result

    @allure.story("测试搜索候选用例")
    def test_002(self, drivers):
        """测试搜索候选"""
        search = SearchPage(drivers)
        search.input_search("selenium")
        logger.info(list(search.imagine))
        # assert all(["selenium" in i for i in search.imagine])
        assert not all(["selenium" in i for i in search.imagine])


@pytest.mark.usefixtures("fix_class_level")
class TestSearch:
    @pytest.mark.smoke
    def test_bb(self):
        logger.info("测试int和str ")
        try:
            a = '1'
            assert 1 in a
        except AssertionError:
            logger.exception('测试int和str 失败！！')
            raise
        else:
            logger.info("测试int和str 通过！！")


if __name__ == '__main__':
    pytest.main(['TestCase/test_search.py', '--alluredir=Outputs/allure'])
    os.system('allure serve Outputs/allure')
