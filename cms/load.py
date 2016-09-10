# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from forms import ContactForm
from PIL import Image
from views import judgeadmin, adminskip, adminselect, adminupdate
# from usblog.settings import MEDIA_ROOT
from client.models import Blogs, BlogsClassification, ColumnClass
import os
basePath = os.path.dirname(os.path.dirname(__file__))


@csrf_exempt
@judgeadmin
def index(req):
    blogs = Blogs.objects.order_by("-createTime")
    return render_to_response('index.html', {'blogs': blogs})


@csrf_exempt
@judgeadmin
def update(req):
    """"""
    if req.method == 'POST':
        try:
            if '' == req.POST["id"]:
                blogs = []
            else:
                blogs = Blogs.objects.filter(id=req.POST["id"])
            blogHead = req.POST["blogHead"]
            blogContent = req.POST["blogContent"]
            introduction = req.POST["introduction"]
            classificationId = req.POST["blogsClassification"]
            columnClassId = req.POST["columnClass"]
            columnClass = ColumnClass.objects.get(id=columnClassId)
            blogsClassification = BlogsClassification.objects.get(
                id=classificationId)
            # 保存图片
            reqfile = req.FILES.get('blogPic', False)
            if reqfile:
                pictureUrl = "cms/static/cms/images/blogPic/" + blogHead + ".jpg"
                #
                # 生产环境中长传文件时所需要修改的文件路径
                # pictureUrl = "static/cms/images/blogPic/" + blogHead + ".jpg"
                picturePath = os.path.join(basePath, pictureUrl)
                img = Image.open(reqfile)
                img.thumbnail((700, 700), Image.ANTIALIAS)  # 对图片进行等比缩放
                img.save(picturePath, "png")  # 保存图片
            else:
                #
                # 生产环境中长传文件时所需要修改的文件路径
                # pictureUrl = "static/cms/images/1.jpg"  # 选择默认图片
                pictureUrl = "cms/static/cms/images/1.jpg"  # 选择默认图片
            
            pictureUrl = pictureUrl[3:]
            #
            # 生产环境中长传文件时所需要修改的文件路径
            # pictureUrl = "/" + pictureUrl
            # 修改博客
            if len(blogs) != 0:
                blogs.update(blogHead=blogHead, blogContent=blogContent, introduction=introduction,
                             blogsClassification=blogsClassification, columnClass=columnClass)
                if reqfile:
                    blogs.update(blogPic=pictureUrl)
                return HttpResponse(2)
            # 新建博客
            blog = Blogs(blogHead=blogHead, blogContent=blogContent, introduction=introduction, blogPic=pictureUrl,
                         blogsClassification=blogsClassification, columnClass=columnClass)
            blog.save()
            return HttpResponse(1)
        except Exception as err:
            print err
            return HttpResponse(0)
    else:
        if 'update' in req.GET:  # 更新博客
            blog = Blogs.objects.get(id=req.GET['update'])
            classifications = []
            columnClass = [blog.columnClass]
            classifications.append(blog.blogsClassification)
            blogColumnClass = ColumnClass.objects.filter(
                isShow=True).order_by("-createTime")
            for item in blogColumnClass:
                if item == blog.columnClass:
                    continue
                columnClass.append(item)
            blogClassifications = BlogsClassification.objects.filter(
                isShow=True).order_by("-createTime")
            for item in blogClassifications:
                if item == blog.blogsClassification:
                    continue
                classifications.append(item)
            return render_to_response('addblogs.html', {'blog': blog, "classifications": classifications, "columnClass": columnClass})
        if 'delete' in req.GET:  # 删除博客
            try:
                Blogs.objects.get(id=req.GET['delete']).delete()
                return HttpResponse("<script type='text/javascript'>alert('删除成功');window.location.href='blogsList';</script>")
            except Exception as err:
                print err
                return HttpResponse("<script type='text/javascript'>alert('删除失败');window.location.href='blogsList';</script>")
        classifications = BlogsClassification.objects.filter(
            isShow=True).order_by("-createTime")
        columnClass = ColumnClass.objects.filter(
            isShow=True).order_by("-createTime")
        return render_to_response('addblogs.html', {"classifications": classifications, "columnClass": columnClass})


@csrf_exempt
@judgeadmin
def blogsList(req):
    """信息列表"""
    blogs = Blogs.objects.order_by("-createTime")[:10]
    return render_to_response('blogsList.html', {'blogs': blogs})


@csrf_exempt
@judgeadmin
def logout(req):
    """
    管理员退出
    """
    response = HttpResponse(
        "<script type='text/javascript'>alert('管理员退出');window.location.href='/client'</script>")
    # 清理cookie里保存username
    response.delete_cookie('adminID')
    return response


@csrf_exempt
@judgeadmin
def classification(req):
    """分类管理"""
    if req.method == 'POST':
        try:
            classificationName = req.POST["classificationName"]
            isShow = req.POST["isShowRadio"]
            classificationId = req.POST["classificationId"]
            print isShow, classificationName, classificationId
            if -1 == int(classificationId):
                classification = BlogsClassification(
                    classificationName=classificationName, isShow=isShow)
                res = "添加成功！"
            else:
                classification = BlogsClassification.objects.get(
                    id=classificationId)
                classification.classificationName = classificationName
                classification.isShow = isShow
                res = "修改成功！"
            classification.save()
        except Exception as err:
            print err
            res = "操作失败，请重试！"
        finally:
            return HttpResponse(
                "<script type='text/javascript'>alert('" + res + "');window.location.href='classification'</script>")
    else:
        if 'delete' in req.GET:
            classification = BlogsClassification.objects.get(id=req.GET[
                                                             "delete"])
            classification.delete()
            return HttpResponse("<script type='text/javascript'>alert('删除成功！');window.location.href='classification'</script>")
        classifictions = BlogsClassification.objects.order_by(
            "-createTime")[:10]
        return render_to_response('classification.html', {"classifictions": classifictions})


@csrf_exempt
@judgeadmin
def column(req):
    """栏目管理"""
    if req.method == 'POST':
        try:
            columnName = req.POST["columnName"]
            isShow = req.POST["isShowRadio"]
            columnId = req.POST["columnId"]
            context = req.POST["context"]
            if -1 == int(columnId):
                columnClass = ColumnClass(
                    columnName=columnName, isShow=isShow, context=context)
                res = "添加成功！"
            else:
                columnClass = ColumnClass.objects.get(
                    id=columnId)
                columnClass.columnName = columnName
                columnClass.isShow = isShow
                columnClass.context = context
                res = "修改成功！"
            columnClass.save()
        except Exception as err:
            print err
            res = "操作失败，请重试！"
        finally:
            return HttpResponse(
                "<script type='text/javascript'>alert('" + res + "');window.location.href='column'</script>")
    else:
        if 'delete' in req.GET:
            columnClass = ColumnClass.objects.get(id=req.GET["delete"])
            columnClass.delete()
            return HttpResponse("<script type='text/javascript'>alert('删除成功！');window.location.href='column'</script>")
        columnClass = ColumnClass.objects.order_by(
            "-createTime")[:10]
        return render_to_response('columnList.html', {"columnClass": columnClass})
