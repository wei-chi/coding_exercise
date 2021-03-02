import os
import unittest
import sys

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask.cli import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
db_user = os.getenv("MYSQL_USER")
db_password = os.getenv("MYSQL_PASSWORD")
db_database = os.getenv("MYSQL_DATABASE")

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{db_user}:{db_password}@db:3306/{db_database}"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Task(db.Model):
    __tablename__ = "task"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    status = db.Column(db.Boolean)


@app.route("/tasks/")
def get_tasks():
    tasks = Task.query.all()
    return jsonify({
        "result": [
            {"id": task.id, "name": task.name, "status": int(task.status)}
            for task in tasks
        ]
    })


@app.route("/task/", methods=["POST"])
def create_task():
    name = request.form.get("name")
    task = Task(name=name, status=0)
    db.session.add(task)
    db.session.commit()
    return jsonify({"result": {"name": name, "status": 0, "id": task.id}}), 201


@app.route("/task/<id>/", methods=["PUT"])
def update_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    name = request.form.get("name")
    status = request.form.get("status")
    task.name = name
    task.status = bool(status)
    db.session.commit()
    return jsonify({"name": name, "status": int(status), "id": task.id})


@app.route("/task/<id>/", methods=["DELETE"])
def delete_task(id):
    task = Task.query.filter_by(id=id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    return Response(status=200, mimetype="application/json")


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.errors or result.failures:
        sys.exit(1)


if __name__ == "__main__":
    app.run()
