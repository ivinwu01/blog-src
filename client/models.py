# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class ColumnClass(models.Model):
    """栏目类型"""
    columnName = models.CharField(max_length=32)
    isShow = models.BooleanField(default=1)
    createTime = models.DateTimeField(auto_now_add=True)
    context = models.CharField(max_length=32)

    class Meta:
        verbose_name = u"栏目类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.columnName


class BlogsClassification(models.Model):
    """分类"""
    classificationName = models.CharField(max_length=32)
    isShow = models.BooleanField(default=1)
    createTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.classificationName

    class Meta:
        verbose_name = u"分类"
        verbose_name_plural = verbose_name


class Blogs(models.Model):
    """博客文章"""
    columnClass = models.ForeignKey(ColumnClass)
    blogsClassification = models.ForeignKey(
        BlogsClassification, blank=True, null=True)
    blogHead = models.CharField(max_length=100)
    blogPic = models.CharField(max_length=100, blank=True, null=True)
    blogContent = models.TextField(blank=True, null=True)
    introduction = models.CharField(max_length=300)  # 简介
    isRecommend = models.BooleanField(default=1)  # 是否推荐
    isShow = models.BooleanField(default=1)
    createTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.blogHead

    class Meta:
        verbose_name = u"博客文章"
        verbose_name_plural = verbose_name


class Comments(models.Model):
    """评论信息"""
    commentsContent = models.TextField(blank=True, null=True)
    blogs = models.ForeignKey(Blogs)
    peopleName = models.CharField(max_length=20, blank=True)
    peopleEmail = models.CharField(max_length=32, blank=True)
    isShow = models.BooleanField(default=1)
    createTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.peopleEmail

    class Meta:
        verbose_name = u"评论信息"
        verbose_name_plural = verbose_name


class Admin(models.Model):
    """管理员信息"""
    adminAccount = models.CharField(max_length=32)
    adminPassword = models.CharField(max_length=32)
    adminJob = models.CharField(max_length=50, blank=True)
    adminTelephone = models.CharField(max_length=12, blank=True)
    adminEmail = models.CharField(max_length=32, blank=True)
    adminPortrait = models.CharField(max_length=32, blank=True)  # 身份
    createTime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.adminAccount

    class Meta:
        verbose_name = u"管理员信息"
        verbose_name_plural = verbose_name
