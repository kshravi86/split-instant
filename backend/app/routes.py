from flask import Blueprint, request, jsonify
from app import db
from app.models import Group, Expense, User, Settlement
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('routes', __name__)

@bp.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    print(data)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    participant_ids = data.get('participant_ids', [])
    participants = User.query.filter(User.id.in_(participant_ids)).all()
    participants.append(user)
    
    new_group = Group(name=data['name'], participants=participants)
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'Group created successfully', 'group_id': new_group.id}), 201

@bp.route('/groups', methods=['GET'])
@jwt_required()
def get_groups():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    groups = user.groups.all()
    return jsonify([{'id': group.id, 'name': group.name} for group in groups])

@bp.route('/groups/<int:group_id>/expenses', methods=['POST'])
@jwt_required()
def add_expense(group_id):
    data = request.get_json()
    user_id = get_jwt_identity()
    
    expense = Expense(
        title=data['title'],
        amount=data['amount'],
        paid_by_id=user_id,
        group_id=group_id
    )
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully', 'expense_id': expense.id}), 201

@bp.route('/groups/<int:group_id>/expenses', methods=['GET'])
@jwt_required()
def get_expenses(group_id):
    expenses = Expense.query.filter_by(group_id=group_id).all()
    return jsonify([{'id': exp.id, 'title': exp.title, 'amount': str(exp.amount)} for exp in expenses])

@bp.route('/groups/<int:group_id>/settlements', methods=['POST'])
@jwt_required()
def add_settlement(group_id):
    data = request.get_json()
    user_id = get_jwt_identity()

    settlement = Settlement(
        from_user_id=user_id,
        to_user_id=data['to_user_id'],
        amount=data['amount'],
        group_id=group_id
    )
    db.session.add(settlement)
    db.session.commit()
    return jsonify({'message': 'Settlement recorded successfully', 'settlement_id': settlement.id}), 201
