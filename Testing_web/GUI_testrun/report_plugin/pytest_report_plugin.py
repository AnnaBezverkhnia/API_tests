import pytest
from py.xml import html
from hippy.hip.api.system import ApiSystem
from hippy.hip.device import HipDevice
from datetime import datetime


def pytest_html_report_title(report):
    ''' modifying the title  of html report'''
    report.title = "Testrun Results"


def pytest_configure(config):
    dut = HipDevice(address=config.getoption('--dut'))
    dut_info = ApiSystem(dut).get_info()
    config._metadata['DUT'] = config.getoption('--dut')
    config._metadata['DUT Firmware'] = f'{dut_info["swVersion"]} {dut_info["buildType"]}'
    config._metadata['DUT Model'] = dut_info['variant']


@pytest.hookimpl(trylast=True)
def pytest_html_results_table_header(cells):
    #  removing old table headers
    #  adding new headers
    cells.insert(3, html.th("Time", class_="sortable time", col="time"))
    cells.insert(4, html.th("Description", col="description"))
    cells.pop()


@pytest.hookimpl(trylast=True)
def pytest_html_results_table_row(report, cells):
    cells.insert(3, html.td(datetime.now(), class_="col-time"))
    cells.insert(4, html.td(report.description))
    cells.pop()



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
