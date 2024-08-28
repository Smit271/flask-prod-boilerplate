from app.extension import db


class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<TestModel {self.name}>'

    def __str__(self):
        return f'TestModel(name={self.name})'
