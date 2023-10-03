from flask import Blueprint, render_template, request, redirect, url_for
from pybo.models import Order
from pybo import db

bp = Blueprint('main', __name__, url_prefix='/')

# 초기 재고 설정
initial_stock = {'coffee': 100, 'greentea': 100, 'bananamilk': 100, 'picnic': 100}

@bp.route('/')
def index():
    # 주문 페이지 표시
    stock = {item: initial_stock[item] for item in initial_stock}
    return render_template('order.html', stock=stock)

@bp.route('/order', methods=['POST'])
def order():
    if request.method == 'POST':
        # 주문 정보 받기
        coffee_quantity = int(request.form['coffee'])
        greentea_quantity = int(request.form['greentea'])
        bananamilk_quantity = int(request.form['bananamilk'])
        picnic_quantity = int(request.form['picnic'])

        # 주문을 처리하고 주문 목록에 추가
        new_order = Order(
            coffee=coffee_quantity,
            greentea=greentea_quantity,
            bananamilk=bananamilk_quantity,
            picnic=picnic_quantity
        )
        db.session.add(new_order)
        db.session.commit()

        # 재고 감소
        initial_stock['coffee'] -= coffee_quantity
        initial_stock['greentea'] -= greentea_quantity
        initial_stock['bananamilk'] -= bananamilk_quantity
        initial_stock['picnic'] -= picnic_quantity

        return redirect(url_for('main.order_list'))
    
@bp.route('/order_list')
def order_list():
    # 주문 목록 표시
    orders = Order.query.all()
    return render_template('order_list.html', orders=orders)

@bp.route('/reset_order_list', methods=['POST'])
def reset_order_list():
    # 주문 목록 초기화
    db.session.query(Order).delete()
    db.session.commit()
    return redirect(url_for('main.order_list'))