#coding:utf-8
from flask import Blueprint, render_template, flash, request

from appname import cache, mongo
from appname.forms import MyForm
from appname.common_util import *
from bson import ObjectId    

main = Blueprint('main', __name__)


def convert_to_lable(data):
    d = data.get('degree')
    if d == 'administrator':
        data['degree'] = u'卡中心管理员'
    elif d == 'manager':
        data['degree'] = u'经理'
    else:
        data['degree'] = u'专员'
        
    d = data.get('type')
    if d == 'center':
        data['type'] = u'卡中心'
    else:
        data['type'] = u'分行'

    d = data.get('state')
    if not d:
        data['state'] = 0
    data['uid'] = str(data['_id']['$oid'])
    return data
        
@main.route('/')
@cache.cached(timeout=1000)
def home():
    data = cursor_to_dict(mongo.db.operator.find())
    data = [convert_to_lable(x) for x in data]
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
        
@main.route('/update_operator_status', methods=['POST'])
def update_operator_status():
    id = ObjectId(request.form['id'])
    state = request.form['state']
    mongo.db.operator.update({'_id': id}, {'$set': {'state': int(state)}})
    return '', 200
