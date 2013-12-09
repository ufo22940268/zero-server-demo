#coding:utf-8
from flask import Blueprint, render_template, flash, request

from appname import cache, mongo
from appname.forms import MyForm
from appname.common_util import *

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    data = cursor_to_dict(mongo.db.operator.find())
    # import pdb; pdb.set_trace()
    return render_template('index.html', operators = data)


@main.route('/wtform', methods=['GET', 'POST'])
def wtform():
    form = MyForm()

    if request.method == 'GET':
        return render_template('wtform_example.html', form=form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            mongo.db.operator.insert(form.data)
            flash(u'提交成功', 'success')
        else:
            flash(u'表单验证失败!', 'danger')
        return render_template('wtform_example.html', form=form)
