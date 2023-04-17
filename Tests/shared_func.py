import time
import operator
from typing import Any
import pytest
from _pytest.mark import ParameterSet


def xfail_mark(parameters_list: Any, failed_param: Any, reason: str) -> list:
    '''
    Function allows to mark the test with particular parameter with XFAIL mark,
    when we expect the test to fail for somme reason. E.x. a known bug.

    :parameters_list: the list of elements to be passed as test parameters
    :failed_param: test parameter from the parameter_list, to be marked with XFAIL
    :reason: the reason test fails with this param, can be Jira issue(bug) number
    '''
    param_list: list = []
    for item in parameters_list:
        if item == failed_param:
            item = pytest.param(item, marks=pytest.mark.xfail(reason=reason))
        elif not isinstance(item, ParameterSet):
            item = pytest.param(item)
        param_list.append(item)
    return param_list


def wait_for(value: Any, timeout: int, period: int, target_func: Any, args: tuple = (), kwargs: dict = {}, operator_func: Any = operator.eq) -> Any:
    ''' Waiting for particular target function result
    :param value: target_func result we wait for
    :param timeout: maximum time to wait for target_func result
    :param period: define interval for calling the targe_func
    :param target_func: define target function to be called
    :param *args: tuple, arguments which could be passed to target_func
    '''
    t_start = time.time()
    kwargs = kwargs or dict()
    while (time.time() - t_start) < timeout:
        out = target_func(*args, **kwargs)
        if operator_func(out, value):
            return out
        time.sleep(period)
    else:
        raise AssertionError(
            f'Expected value {value} was not received from target function calling within given '
            f'timeout {timeout}. Received value: {out}'
        )


# check if length of target function result equals expected value
# could be used as operator_func in wait_for
def compare_result_len(target_func_result, value):
    return len(target_func_result) == value
