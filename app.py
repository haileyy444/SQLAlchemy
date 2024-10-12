"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_ECHO'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route('/')
def home():
        # Home Page
        return redirect("/users")


@app.route('/users')
def users_directory():
        # directory of users
        users = User.query.order_by(User.last_name, User.first_name).all()
        print(current_app.jinja_env.list_templates())
        return render_template("users/directory.html", users=users)


@app.route('/users/new', methods=["GET"])
def add_users_form():
        # add users form
        return render_template("users/new.html")

@app.route('/users/new', methods=["POST"])
def add_users():
        # add user post request
        new_user = User(
                first_name = request.form['first_name'], 
                last_name = request.form['last_name'], 
                image_url = request.form['image_url'] or None)
        
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")




@app.route('/users/<int:user_id>')
def user_inspect(user_id):
        # inspect user from directory - more info page
        user = User.query.get_or_404(user_id)
        return render_template("users/inspect.html", user=user)



@app.route('/users/<int:user_id>/edit')
def edit_user_inspect(user_id):
        # edits inspected user from directory - more info page (form)
        user = User.query.get_or_404(user_id)
        return render_template("users/edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
        # add user post request
        user = User.query.get_or_404(user_id)
        user.first_name = request.form['first_name'], 
        user.last_name = request.form['last_name'], 
        user.image_url = request.form['image_url'] or None
        
        db.session.add(user)
        db.session.commit()
        return redirect("/users")

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
        # delete user post request
        user = User.query.get_or_404(user_id)
        
        db.session.delete(user)
        db.session.commit()
        return redirect("/users")