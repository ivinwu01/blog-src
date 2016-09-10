# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from client.models import Admin
import os
import time


def judgeadmin(test):
    """
    判断是否登录，后台操作的全局判断，用作装饰器
    :param test:
    :return:
    """
    def infun(req, *args, **kwargs):
        if req.COOKIES.get('adminID', '') == '':
            return HttpResponseRedirect('/client')
        else:
            adid = Admin.objects.filter(id=req.COOKIES.get('adminID', ''))
            if adid.count() == 0:
                return HttpResponse("<script type='text/javascript'>alert('该用户不存在');window.location.href='/client';</script>")
            else:
                ret = test(req, *args, **kwargs)
                return ret
    return infun


def adminskip(func):
    """
    跳转异常装饰器
    """
    def infun(req, *args, **kwargs):
        basePath = os.path.dirname(os.path.dirname(__file__))
        logPath = os.path.join(basePath, "index/log/skip.txt")
        log_file = open(logPath, "a")
        try:
            ret = func(req, *args, **kwargs)
        except Exception as err:
            log_file.writelines(str(time.strftime('%Y/%m/%d %H:%M:%S')) + "\tview:" +
                                func.__name__ + "\nerror:[" + str(err) + "]\ndoc:" + func.__doc__ + "\n")
            return render_to_response('404.html')
        finally:
            log_file.close()
        return ret
    return infun


def adminselect(func):
    """
    查找异常装饰器
    """
    def infun(req, *args, **kwargs):
        basePath = os.path.dirname(os.path.dirname(__file__))
        logPath = os.path.join(basePath, "index/log/select.txt")
        log_file = open(logPath, "a")
        try:
            ret = func(req, *args, **kwargs)
        except Exception as err:
            log_file.writelines(str(time.strftime('%Y/%m/%d %H:%M:%S')) + "\tview:" +
                                func.__name__ + "\nerror:[" + str(err) + "]\ndoc:" + func.__doc__ + "\n")
            return render_to_response('404.html')
        finally:
            log_file.close()
        return ret
    return infun


def adminupdate(func):
    """
    增删改异常装饰器
    """
    def infun(req, *args, **kwargs):
        basePath = os.path.dirname(os.path.dirname(__file__))
        logPath = os.path.join(basePath, "index/log/update.txt")
        log_file = open(logPath, "a")
        try:
            ret = func(req, *args, **kwargs)
        except Exception as err:
            log_file.writelines(str(time.strftime('%Y/%m/%d %H:%M:%S')) + "\tview:" +
                                func.__name__ + "\nerror:[" + str(err) + "]\ndoc:" + func.__doc__ + "\n")
            return render_to_response('404.html')
        finally:
            log_file.close()
        return ret
    return infun
