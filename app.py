"""Blogly application."""

from flask import Flask, request, redirect, render_template, current_app
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from sqlalchemy.orm import joinedload

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





# admin stuff
@app.route('/')
def home():
        # Home Page
        # posts = Post.query.order_by(Post.post_date.desc()).limit(5).all()
        posts = Post.query.options(joinedload(Post.author)).all()
        return render_template("posts/directory.html", posts=posts)


@app.errorhandler(404)
def error(e): 
        return render_template('error.html'), 404








# users directory
@app.route('/users')
def users_directory():
        # directory of users
        print(current_app.jinja_env.list_templates())
        users = User.query.order_by(User.last_name, User.first_name).all()
        
        return render_template("users/directory.html", users=users)
                               





# adding a user
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







# specific user and capabilities
@app.route('/users/<int:user_id>')
def user_inspect(user_id):
        # inspect user from directory - more info page
        user = User.query.get_or_404(user_id)
        return render_template("users/show.html", user=user)

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




# Posts
@app.route('/users/<int:user_id>/posts', methods=["GET"])
def get_posts(user_id):
        
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(poster=user_id).all()
        print(posts)
        return render_template("posts/userposts.html", posts=posts, user=user)

# adding a post
@app.route('/users/<int:user_id>/posts/new')
def new_post_get(user_id):
        
        user = User.query.get_or_404(user_id)
        return render_template("posts/new.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post_post(user_id):
        
        user = User.query.get_or_404(user_id)
        new_post = Post(post_title=request.form['post_title'], post_text=request.form['post_text'], poster = user.id)

        db.session.add(new_post)
        db.session.commit()

        return redirect( f"/users/{user_id}" )



# specific  posts
@app.route('/posts/<int:post_id>')
def inspect_post(post_id):
        # inspect post  more info page
        post = Post.query.get_or_404(post_id)
        return render_template("posts/show.html", post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
        # inspect post  more info page
        post = Post.query.get_or_404(post_id)
        return render_template("posts/edit.html", post=post)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
        # inspect post  more info page
        post = Post.query.get_or_404(post_id)
        post_title = request.form["post_title"]
        post_text = request.form["post_text"]

        post.post_title = post_title
        post.post_text = post_text

        try:
            db.session.add(post)
            db.session.commit()
        except Exception as e:
                db.session.rollback()
                print(f"Error updating post: {e}")
                return "Error updating post", 500

        return redirect(f"/users/{post.author.id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
        # inspect post  more info page
        post = Post.query.get_or_404(post_id)

        db.session.delete(post)
        db.session.commit()
        
        return redirect(f"/")