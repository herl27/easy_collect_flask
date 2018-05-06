from app import db
from datetime import datetime

class Teacher(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    is_admin = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64), index=True)
    id_card = db.Column(db.String(64), index=True, unique=True)
    race = db.Column(db.String(64))
    origin = db.Column(db.String(64))
    tel = db.Column(db.String(64))
    course = db.Column(db.String(64))
    is_header_teacher = db.Column(db.Boolean())
    working_date = db.Column(db.Date())
    create_time = db.Column(db.DateTime())
    change_time = db.Column(db.DateTime())

    @property
    def sex(self):
        return "男" if int(self.id_card[-2:-1]) % 2 else "女" 

    @property
    def birthday(self):
        return datetime.strptime(self.id_card[6:14],'%Y%m%d')

    def __repr__(self):
        return '<Teacher %r>' % self.name
