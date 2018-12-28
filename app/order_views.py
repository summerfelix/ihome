import datetime

from flask import Blueprint, render_template, jsonify, request, session

from app.models import House, Order
from utils import status_code
from utils.functions import login_status

blue_order = Blueprint('order', __name__)


@blue_order.route('/orders/', methods=['GET'])
@login_status
def order():
    return render_template('orders.html')


@blue_order.route('/lorders/', methods=['GET'])
@login_status
def lorders():
    return render_template('lorders.html')


@blue_order.route('/booking/', methods=['GET'])
def booking():
    return render_template('booking.html')


@blue_order.route('/booking_house/<int:id>/', methods=['GET'])
def booking_house(id):
    house = House.query.filter(House.id == id).first()
    return jsonify({'code': 200, 'house': house.to_dict()})


@blue_order.route('/create_order/', methods=['POST'])
@login_status
def create_order():
    try:
        user_id = session['user_id']
    except:
        user_id = None
    if not user_id:
        return jsonify(status_code.LOGIN_STATUS_NOT_LOGIN)
    house_id = request.form.get('house_id')
    house = House.query.filter(House.id == house_id).first()
    price = house.price
    max_days = house.max_days
    sd = request.form.get('sd')
    ed = request.form.get('ed')
    sd = datetime.datetime.strptime(sd, '%Y-%m-%d')
    ed = datetime.datetime.strptime(ed, '%Y-%m-%d')
    if ed <= sd:
        return jsonify(status_code.BOOKING_STATUS_DATE_ERROR)
    days = (ed - sd).days
    if max_days != 0 and days > max_days:
        return jsonify(status_code.BOOKING_STATUS_MAX_DAYS_ERROR)
    amount = price * days
    order = Order()
    order.house_id = house_id
    order.user_id = user_id
    order.begin_date = sd
    order.end_date = ed
    order.days = days
    order.house_price = price
    order.amount = amount
    order.status = 'WAIT_ACCEPT'
    order.add_update()
    return jsonify(status_code.SUCCESS)


@blue_order.route('/my_orders/', methods=['GET'])
@login_status
def my_orders():
    user_id = session['user_id']
    orders = Order.query.filter(Order.user_id == user_id).all()
    data = {}
    i = 1
    if not orders:
        return jsonify(status_code.ORDER_STATUS_NOT_FOUND)
    status = {
        "WAIT_ACCEPT": '待接单',
        "WAIT_PAYMENT": '待支付',
        "PAID": '已支付',
        "WAIT_COMMENT": '待评价',
        "COMPLETE": '已完成',
        "CANCELED": '已取消',
        "REJECTED": '已拒单'
    }
    for order in orders:
        data[i] = order.to_dict()
        i += 1
    for d in data:
        for key, val in status.items():
            if data[d]['status'] == key:
                data[d]['status'] = val
    return jsonify(data)


@blue_order.route('/l_orders/', methods=['GET'])
@login_status
def l_orders():
    user_id = session['user_id']
    house = House.query.filter(House.user_id == user_id).all()
    orders = []
    for h in house:
        house_id = h.id
        order = Order.query.filter(Order.house_id == house_id).first()
        if order:
            orders.append(order)
    if not orders:
        return jsonify(status_code.LORDER_STATUS_NOT_FOUND)
    data = {}
    i = 1
    for o in orders:
        data[i] = o.to_dict()
        i += 1
    status = {
        "WAIT_ACCEPT": '待接单',
        "WAIT_PAYMENT": '待支付',
        "PAID": '已支付',
        "WAIT_COMMENT": '待评价',
        "COMPLETE": '已完成',
        "CANCELED": '已取消',
        "REJECTED": '已拒单'
    }
    for d in data:
        for key, val in status.items():
            if data[d]['status'] == key:
                data[d]['status'] = val
    return jsonify(data)


@blue_order.route('/comment/', methods=['POST'])
@login_status
def comment():
    id = request.form.get('id')
    content = request.form.get('content')
    order = Order.query.filter(Order.id == id).first()
    order.comment = content
    order.status = 'COMPLETE'
    order.add_update()
    return jsonify(status_code.SUCCESS)


@blue_order.route('/accept/', methods=['POST'])
@login_status
def accept():
    id = request.form.get('id')
    order = Order.query.filter(Order.id == id).first()
    order.status = 'WAIT_COMMENT'
    order.add_update()
    return jsonify(status_code.SUCCESS)


@blue_order.route('/reject/', methods=['POST'])
@login_status
def reject():
    id = request.form.get('id')
    content = request.form.get('content')
    order = Order.query.filter(Order.id == id).first()
    order.comment = content
    order.status = 'REJECTED'
    order.add_update()
    return jsonify(status_code.SUCCESS)
