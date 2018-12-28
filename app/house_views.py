import os
import datetime

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from app.models import House, Area, Facility, HouseImage, User, Order
from utils import status_code
from utils.functions import login_status
from utils.settings import MEDIA_PATH

blue_house = Blueprint('house', __name__)


@blue_house.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@blue_house.route('/myhouse/', methods=['GET'])
@login_status
def myhouse():
    return render_template('myhouse.html')


@blue_house.route('/newhouse/', methods=['GET'])
@login_status
def newhouse():
    return render_template('newhouse.html')


@blue_house.route('/search/', methods=['GET'])
def search():
    return render_template('search.html')


@blue_house.route('/detail/', methods=['GET'])
def detail():
    return render_template('detail.html')


@blue_house.route('/get_area/', methods=['GET'])
def get_area():
    area = Area.query.all()
    data = {}
    for a in area:
        a = a.to_dict()
        data[a['id']] = a['name']
    return jsonify(data)


@blue_house.route('/get_facility/', methods=['GET'])
def get_facility():
    facility = Facility.query.all()
    data = {}
    i = 1
    for f in facility:
        data[i] = f.to_dict()
        i += 1
    return jsonify(data)


@blue_house.route('/add_house/', methods=['POST'])
@login_status
def add_house():
    user_id = int(session['user_id'])
    title = request.form.get('title')
    price = request.form.get('price')
    area = request.form.get('area_id')
    address = request.form.get('address')
    room_count = request.form.get('room_count')
    acreage = request.form.get('acreage')
    unit = request.form.get('unit')
    capacity = request.form.get('capacity')
    beds = request.form.get('beds')
    deposit = request.form.get('deposit')
    min_days = request.form.get('min_days')
    max_days = request.form.get('max_days')
    if not all([title, price, area, address, room_count, acreage, unit, capacity, beds, deposit, min_days, max_days]):
        return jsonify(status_code.HOUSE_ERROR_INFO_IS_NULL)
    house = House()
    house.user_id = user_id
    house.title = title
    house.price = price
    house.area_id = area
    house.address = address
    house.room_count = room_count
    house.acreage = acreage
    house.unit = unit
    house.capacity = capacity
    house.beds = beds
    house.deposit = deposit
    house.min_days = min_days
    house.max_days = int(max_days)

    facilitys = request.form.getlist('facility')

    for f in facilitys:
        facility = Facility.query.filter(Facility.id == f).first()
        house.facilities.append(facility)

    house.add_update()
    data = {
        'code': 200,
        'house_id': house.id
    }
    return jsonify(data)


@blue_house.route('/house_image/', methods=['PATCH'])
@login_status
def house_image():
    image = request.files.get('house_image')
    path = os.path.join(MEDIA_PATH, image.filename)
    image.save(path)
    id = request.form.get('house_id')
    house = House.query.filter(House.id == id).first()
    index_image = house.index_image_url
    if not index_image:
        house.index_image_url = image.filename
        house.add_update()
    else:
        h_image = HouseImage()
        h_image.house_id = id
        h_image.url = image.filename
        h_image.add_update()
    return jsonify(status_code.SUCCESS)


@blue_house.route('/get_image/<int:id>/', methods=['GET'])
def get_image(id):
    data = {}
    house = House.query.filter(House.id == id).first()
    image = house.index_image_url
    data[image] = image
    house_image = HouseImage.query.filter(HouseImage.house_id == id).all()
    if house_image:
        for i in house_image:
            image2 = i.url
            data[image2] = image2
    return jsonify(data)


@blue_house.route('/get_myhouse/', methods=['GET'])
def get_myhouse():
    house = House.query.all()
    i = 1
    data = {}
    for h in house:
        data[i] = h.to_dict()
        i += 1
    return jsonify(data)


@blue_house.route('/detail/<int:id>/', methods=['GET'])
def detail1(id):
    try:
        user_id = session['user_id']
    except:
        user_id = None
    house = House.query.filter(House.id == id).first()
    house_image = HouseImage.query.filter(HouseImage.house_id == id).all()
    image = []
    for i in house_image:
        url = i.url
        image.append(url)
    image.append(house.index_image_url)
    facility = []
    facilitys = house.facilities
    for f in facilitys:
        f = f.to_dict()
        facility.append(f)
    id = house.user_id
    data = {
        'code': 200,
        'house': house.to_full_dict(),
        'image': image,
        'facility': facility
    }
    if user_id == id:
        data['code'] = 1016
    return jsonify(data)


@blue_house.route('/login_status/', methods=['GET'])
def get_index():
    try:
        user_id = session['user_id']
    except:
        return jsonify(status_code.LOGIN_STATUS_NOT_LOGIN)
    user = User.query.filter(User.id == user_id).first()
    data = {
        'code': 1013,
        'username': user.name,
        'phone': user.phone
    }
    return jsonify(data)


@blue_house.route('/swiper/', methods=['GET'])
def swiper():
    all_houses = House.query.all()
    houses = all_houses[-1:-6:-1]
    house = []
    for h in houses:
        house.append(h.to_dict())
    data = {
        'code': 200,
        'house': house
    }
    return jsonify(data)


@blue_house.route('/search/<aid>/<sd>/<ed>/<sk>/', methods=['GET'])
def search1(aid, sd, ed, sk):
    data = {}
    i = 1
    sd = datetime.datetime.strptime(sd, '%Y-%m-%d')
    ed = datetime.datetime.strptime(ed, '%Y-%m-%d')
    # 过滤区域信息
    hlist = House.query.filter(House.area_id == aid)
    # 查询不满足条件的房屋id
    order1 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= ed)
    order2 = Order.query.filter(Order.begin_date <= sd, Order.end_date >= sd)
    order3 = Order.query.filter(Order.begin_date >= sd, Order.begin_date <= ed)
    order4 = Order.query.filter(Order.begin_date >= sd, Order.end_date <= ed)
    house_ids1 = [order.house_id for order in order1]
    house_ids2 = [order.house_id for order in order2]
    house_ids3 = [order.house_id for order in order3]
    house_ids4 = [order.house_id for order in order4]

    house_ids = list(set(house_ids1 + house_ids2 + house_ids3 + house_ids4))
    # 最终展示的房屋信息
    houses = hlist.filter(House.id.notin_(house_ids))

    if sk == 'booking':
        houses = houses.order_by('order_count')
    elif sk == 'price-inc':
        houses = houses.order_by('price')
    elif sk == 'price-des':
        houses = houses.order_by('-price')
    else:
        houses = houses.order_by('-id')
    if not houses:
        return jsonify(status_code.SEARCH_STATUS_IS_NOT_FIND)
    for h in houses:
        data[i] = h.to_full_dict()
        i += 1
    return jsonify({'code': 200, 'data': data})

























