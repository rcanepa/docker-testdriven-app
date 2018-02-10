from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc
from project import db
from project.api.models import User


users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_error_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }

    if not post_data:
        return jsonify(response_error_object), 400
    username = post_data.get('username')
    email = post_data.get('email')

    if not username:
        return jsonify(response_error_object), 400

    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!',
            }
            return jsonify(response_object), 201
        else:
            return jsonify({
                'status': 'fail',
                'message': 'Sorry, that email already exists.'
            }), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_error_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details."""
    user_not_found_response = {
        'status': 'fail',
        'message': 'User does not exist',
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(user_not_found_response), 404
        else:
            return jsonify({
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }), 200
    except ValueError as e:
        return jsonify(user_not_found_response), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users."""
    return jsonify({
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    }), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)
