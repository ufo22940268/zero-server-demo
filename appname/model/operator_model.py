#coding: utf-8
import os

from flask import Flask
from flask_assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.cache import Cache
import flask.ext.admin
from flask.ext.admin.form import Select2Widget
from flask.ext.pymongo import PyMongo
from flask.ext.babelex import Babel
from wtforms import form, fields

from appname.models import db
from flask.ext.admin.contrib.sqla import filters

class OperatorForm(form.Form):
    username = fields.TextField(u'用户名')
    password = fields.PasswordField(u'密码')
    region = fields.SelectField(u'分行', choices=[(u'分行', u'分行'),(u'卡中心', u'卡中心')])
    degree = fields.SelectField(u'职级', choices=[(u'卡中心管理员', u'卡中心管理员'), (u'经理', u'经理'), (u'专员', u'专员')])
    type = fields.SelectField(u'类别', choices=[(u'优惠', u'优惠'),(u'分期', u'分期')])
    state = fields.SelectField(u'状态', choices=[(u'转岗', u'转岗'),(u'离职', u'离职')])

from flask.ext.admin.contrib.pymongo import ModelView, filters
class OperatorView(ModelView):
    column_list = ('region', 'type', 'degree', 'username', 'mobile', 'state')
    column_labels = {'region': u'区域', 'type': u'类型', 'degree': u'职位', 'username': u'用户', 'mobile': u'手机号码', 'state': u'状态'}

    column_sortable_list = ('type', 'state', 'username')

    # Full text search
    column_searchable_list = ('username', 'username')

    # Column filters
    column_filters = (filters.FilterLike('username', u'用户名'),
                      filters.FilterEqual('state', u'状态'))
    form = OperatorForm
