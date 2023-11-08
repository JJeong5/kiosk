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
    
    # 초기 재고 다시 설정
    initial_stock['coffee'] = 100
    initial_stock['greentea'] = 100
    initial_stock['bananamilk'] = 100
    initial_stock['picnic'] = 100
    
    return redirect(url_for('main.order_list'))

# 주문 취소 라우트
@bp.route('/cancel_order/<int:order_id>', methods=['DELETE'])
def cancel_order(order_id):
    order = Order.query.get(order_id)
    if order:
        # 취소된 주문에 포함된 각 항목의 재고를 증가시킵니다.
        initial_stock['coffee'] += order.coffee
        initial_stock['greentea'] += order.greentea
        initial_stock['bananamilk'] += order.bananamilk
        initial_stock['picnic'] += order.picnic

        # 주문 삭제
        db.session.delete(order)
        db.session.commit()
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'error'}), 404
    
# 주문 접수 라우트
@bp.route('/accept_order/<int:order_id>', methods=['POST'])
def accept_order(order_id):
    order = Order.query.get(order_id)
    if order:
        # 주문 상태를 '조리 중'으로 업데이트
        order.status = '조리 중'
        db.session.commit()
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'error'}), 404

# 주문 완료 라우트
@bp.route('/complete_order/<int:order_id>', methods=['POST'])
def complete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        # 주문 상태를 '조리 완료'로 업데이트
        order.status = '조리 완료'
        db.session.commit()
        return jsonify({'result': 'success'})
    else:
        return jsonify({'result': 'error'}), 404