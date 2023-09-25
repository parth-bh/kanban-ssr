from .database import db


class User(db.Model):
    __tablename__ = 'user'
    email = db.Column(db.String, unique=True, nullable=False)
    user_name = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, nullable=False)

    main_data = db.relationship('MainData')

    list_details = db.relationship('ListDetails')

class ListDetails(db.Model):
    __tablename__ = "list_details"
    list_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    list_name = db.Column(db.String)  
    user_name = db.Column(db.String, db.ForeignKey('user.user_name'))

    main_data = db.relationship('MainData')

class MainData(db.Model):
    __tablename__ = 'main_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=True)
    content = db.Column(db.String)
    deadline = db.Column(db.String)
    start_date = db.Column(db.String)
    completion_date = db.Column(db.String)
    mark_as_complete = db.Column(db.Boolean, nullable=False)

    user_name = db.Column(db.String, db.ForeignKey('user.user_name'))
    list_id = db.Column(db.String, db.ForeignKey('list_details.list_id'))    

#db.create_all()