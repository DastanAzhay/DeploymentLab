
# Task 2
from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy

# Task 21
app = Flask(__name__)

# Task 24
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Task 22
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)


# Task 23
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)


# Task 30
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# Task 2
@app.route('/')
def hello():
    return "Hello World!"


# Task 3
@app.route('/json-string')
def json_string():
    return '{"message": "Hello"}'


# Task 4
@app.route('/jsonify')
def json_example():
    return jsonify({"message": "Hello with jsonify"})


# Task 5
@app.route('/user/<name>')
def user_name(name):
    return f"Hello, {name}"


# Task 6
users_memory = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]


# Task 18
@app.before_request
def log_request():
    print(f"{request.method} {request.path}")


# Task 7 + Task 25
@app.route('/users', methods=['GET'])
def get_users():
    # using database instead of memory
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email}
        for u in users
    ])


# Task 8 + Task 9
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404)
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })


# Task 28 + Task 29
@app.route('/users/filter', methods=['GET'])
def filter_users():
    active = request.args.get('active')
    limit = request.args.get('limit', type=int)
    offset = request.args.get('offset', type=int)

    query = User.query

    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    users = query.all()

    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email}
        for u in users
    ])


# Task 10 + Task 11 + Task 12 + Task 13 + Task 26 + Task 27
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    if not data or 'username' not in data:
        return jsonify({"error": "username required"}), 400

    try:
        user = User(
            username=data['username'],
            email=data.get('email', '')
        )
        db.session.add(user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "database error"}), 500

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    }), 201


# Task 14
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        abort(404)

    if not data or 'username' not in data:
        return jsonify({"error": "username required"}), 400

    user.username = data['username']
    user.email = data.get('email', user.email)

    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })


# Task 17
@app.route('/users/<int:user_id>', methods=['PATCH'])
def patch_user(user_id):
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        abort(404)

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    db.session.commit()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email
    })


# Task 15 + Task 16
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)

    if not user:
        abort(404)

    db.session.delete(user)
    db.session.commit()

    return '', 204


# Task 19
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404


# Task 20
@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500


# Task 24 (create DB)
with app.app_context():
    db.create_all()


# Run app
if __name__ == '__main__':
    app.run(debug=True)