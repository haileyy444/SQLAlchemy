from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMG = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default = DEFAULT_IMG)

    posts = db.relationship("Post", backref="author", cascade="all, delete-orphan")

    @property
    def full_name(self): 
        return f"{self.first_name} {self.last_name}"
    


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.Text, nullable=False)    
    post_text = db.Column(db.Text, nullable=False)
    poster = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)   
    post_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


    # user = db.relationship("User", backref=db.backref("posts", lazy=True))
    
    @property
    def friendly_date(self): 
        return self.post_date.strftime("%a %b %-d %Y, %-I:%M %p")


def connect_db(app): 
    db.app = app
    db.init_app(app)
