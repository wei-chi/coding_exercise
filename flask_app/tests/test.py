from flask_testing import TestCase

from main import app
from main import db
from main import Task


class MyTest(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        self.app = app
        return app

    def setUp(self):
        db.init_app(self.app)
        db.create_all()
        db.session.add(Task(name="have breakfast", status=0))
        db.session.add(Task(name="have lunch", status=0))
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class TaskTest(MyTest):
    def test_get_tasks(self):
        response = self.client.get("/tasks/")
        self.assert_status(response, 200)
        self.assertEquals(
            response.json,
            {"result": [{"id": 1, "name": "have breakfast", "status": 0}, {"id": 2, "name": "have lunch", "status": 0}]}
        )

    def test_create_task(self):
        response = self.client.post("/task/", data=dict(name="have dinner"))
        self.assert_status(response, 201)
        self.assertEquals(
            response.json,
            {"result": {"id": 3, "name": "have dinner", "status": 0}}
        )

    def test_update_task(self):
        response = self.client.put("/task/2/", data=dict(name="coding", status=1))
        self.assert_status(response, 200)
        self.assertEquals(
            response.json,
            {"id": 2, "name": "coding", "status": 1}
        )

    def test_delete_task(self):
        response = self.client.delete("/task/2/")
        self.assert_status(response, 200)
        response = self.client.delete("/task/3/")
        self.assert_status(response, 404)
