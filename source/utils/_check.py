#coding:utf8
"""
Purpose: 提供检查相关方法
    * check_parameters 和 check_parameter: 检查请求是否包括需要的参数
"""
from flask import request

from source.lib.exceptions import *

# Done: 检验 post 方法中 request 的参数有效
def _check_parameter(arg):
    """检测请求的单个参数
    
    如果 arg 在请求参数中，返回 True， 否则返回 RequestParameterMissing 异常 
    """
    assert arg in request.args or arg in request.form, \
        RequestParameterMissing("`{arg}` not in request parameters".format(arg=arg))
    
    result = {arg: request.args.get(arg) or request.form.get(arg)}
    return result


def check_parameters(*args):
    """检测请求参数
    """
    result = {}
    for arg in args:
        if isinstance(arg, str):
            result.update(_check_parameter(arg))
        else:
            raise TypeError("args is not supported")
    
    return result