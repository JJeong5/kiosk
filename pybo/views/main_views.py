from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from pybo.models import Order
from pybo import db
from datetime import datetime, timedelta

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
        # 현재 시간
        current_time = datetime.utcnow()
        
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
            picnic=picnic_quantity,
            order_time=current_time
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

@bp.route('/get_order_status/<int:order_id>')
def get_order_status(order_id):
    order = Order.query.get(order_id)
    if order:
        # 현재 시간
        current_time = datetime.utcnow()
        # 주문 시간과 현재 시간을 비교하여 주문 상태를 업데이트
        if current_time - order.order_time >= timedelta(seconds=5):
            order.status = '조리중'
            db.session.commit()
            
        if current_time - order.order_time >= timedelta(seconds=15):
            order.status = '조리 완료'
            db.session.commit()
        return jsonify({'status': order.status})
    return jsonify({'status': '주문을 찾을 수 없음'}), 404