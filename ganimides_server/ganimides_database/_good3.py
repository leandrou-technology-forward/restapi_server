from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

class User(BaseModel):
    id = db.Column(UUID(), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nullabe=False, unique=True)
    password = db.Column(db.String())
    _default_fields = ["username"]
    _hidden_fields = ["password"]

@app.route("/api/users")
def users():
    return json.dumps([user.to_dict() for user in User.query.all()])

@app.route("/api/users/<string:user_id>", methods=['PUT'])
def users_update(user_id):
    user = User.query.get(user_id)
    form = UserForm.from_json(request.get_json())
    if not form.validate():
        return jsonify(errors=form.errors), 400
    user.from_dict(**form.data)
    db.session.commit()
    return jsonify(user=user.to_dict())
if __name__ == "__main__":
    app.run()

