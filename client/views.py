# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from forms import ContactForm
from models import Blogs, Admin, ColumnClass
import os

basePath = os.path.dirname(os.path.dirname(__file__))


@csrf_exempt
def index(req):
    # filter(isRecommend='true').
    blogs = Blogs.objects.order_by("-createTime")[:10]
    admin = Admin.objects.all()
    if len(admin) == 0:
        administrator = Admin(adminAccount="wen", adminPassword="123456", adminJob="学生",
                              adminTelephone="15131601294", adminEmail="w_angzhiwen@163.com", adminPortrait="安徽灵壁")
        administrator.save()
        admin = administrator
    return render_to_response('_index.html', {'blogs': blogs, 'admin': admin[0]})


@csrf_exempt
def login(req):
    """
    管理员登录
    """
    if req.method == 'POST':
        uf = ContactForm(req.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            admin = Admin.objects.filter(adminAccount=username)
            if admin.exists():
                adminPad = admin[0].adminPassword
                if password == adminPad:
                    response = HttpResponseRedirect('/cms')
                    response.set_cookie('adminID', admin[0].id)
                    return response
                else:
                    return HttpResponse("<script type='text/javascript'>alert('密码错误！');window.location.href='login';</script>")
            else:
                return HttpResponse("<script type='text/javascript'>alert('用户名不存在！');window.location.href='login';</script>")
        return HttpResponse("<script type='text/javascript'>alert('用户名或密码不能为空！');window.location.href='login';</script>")
    else:
        # 如果请求的方式为get，那么判断是不是已经登录，已经登录则直接进入更新模块
        adminId = req.COOKIES.get('adminID', -1)
        admin = Admin.objects.filter(id=adminId)
        if admin.exists():
            return HttpResponseRedirect('/cms')
        else:
            uf = ContactForm()
            return render_to_response('login.html', {'uf': uf})


@csrf_exempt
def say(req):
    blog = Blogs.objects.filter(columnClass=ColumnClass.objects.get(
        columnName="随走随停")).filter(isShow=True).order_by("-createTime")
    return render_to_response('say.html', {"say": blog})


@csrf_exempt
def share(req):
    blogs = Blogs.objects.filter(columnClass=ColumnClass.objects.get(
        columnName="常篇哒论")).filter(isShow=True).order_by("-createTime")[:10]
    return render_to_response('share.html', {"blogs": blogs})


@csrf_exempt
def lookblog(req):
    blog = Blogs.objects.get(id=req.GET["id"])
    return render_to_response('lookBlog.html', {"blog": blog})
