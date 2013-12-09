#coding:utf-8
from flask_wtf import Form
from wtforms import TextField, TextAreaField, SelectField, PasswordField
from wtforms import validators


class MyForm(Form):
    username = TextField(u'username', validators=[validators.required()])
    mobile = TextAreaField(u'mobile', validators=[validators.optional()])
    degree = SelectField(u'degree',
                         validators=[validators.optional()],
                         choices=[('administrator', u'卡中心管理员'), ('manager', u'经理'), ('operator', u'专员')])
    type = SelectField(u'type',
                         validators=[validators.optional()],
                         choices=[('center', u'卡中心'), ('branch', u'分行')])
    password = PasswordField(u'password',
                         validators=[validators.optional()])
    
