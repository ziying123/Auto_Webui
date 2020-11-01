#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
# import tools.
import base64
import pytest
import allure
from py._xmlgen import html
from selenium import webdriver
from tools.logger import logger
from config.conf import SCREENSHOT_DIR
from common.basic.inspect import inspect_element
from tools.times import datetime_strftime

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

driver = None
# driver = webdriver.Chrome()


@pytest.fixture(scope='session', autouse=True)
def drivers(request):
    global driver
    if driver is None:
        driver = webdriver.Chrome()
        driver.maximize_window()
    inspect_element()

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


@pytest.fixture(scope="class")
def fix_class_level():
    logger.info('*' * 25 + "类下的用例开始执行" + '*' * 25 + '\n')
    yield
    logger.info('*' * 25 + "类下的用例结束" + '*' * 25)
    # send_report()  # 发送邮件


@pytest.fixture(scope='function')
def fix_function_level():
    logger.info('='*17 + "单个函数用例开始执行" + '='*17)
    yield
    logger.info('='*17 + "单个函数用例结束执行" + '='*17 + '\n')


@pytest.fixture(scope='module')
def fix_module_level():
    logger.info('='*17 + "单个模块用例开始执行" + '='*17)
    yield
    logger.info('='*17 + "单个模块用例结束执行" + '='*17 + '\n')


@pytest.fixture(scope='session')
def fix_session_level():
    logger.info('='*17 + "单个会话用例开始执行" + '='*17)
    yield
    logger.info('='*17 + "单个会话用例结束执行" + '='*17 + '\n')


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    当测试失败的时候，自动截图，展示到html报告中
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot()
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
        report.description = str(item.function.__doc__)
        report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")


@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def _capture_screenshot():
    '''
    截图保存为base64
    '''
    now_time = datetime_strftime("%Y%m%d%H%M%S")
    if not os.path.exists(SCREENSHOT_DIR):
        os.makedirs(SCREENSHOT_DIR)
    screen_path = os.path.join(SCREENSHOT_DIR, "{}.png".format(now_time))
    driver.save_screenshot(screen_path)
    allure.attach.file(screen_path, "测试失败截图...{}".format(
        now_time), allure.attachment_type.PNG)
    with open(screen_path, 'rb') as f:
        imagebase64 = base64.b64encode(f.read())
    return imagebase64.decode()
