from datetime import datetime

from flask import render_template, flash, redirect, url_for
from flask import request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm
from app.models import User, Post


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    user = current_user
    form = PostForm()
    if form.validate_on_submit():
        post = Post(userid=user.id, body=form.post.data)
        db.session.add(post)
        db.session.commit()
        flash("Your post is updated")
        return redirect(url_for("index"))

    posts = user.followed_posts()\
        .paginate(page, app.config['POSTS_PER_PAGE'], False)\

    prev_url = None
    if posts.has_prev:
        prev_url = url_for('index', page=posts.prev_num)

    next_url = None
    if posts.has_next:
        next_url = url_for('index', page=posts.next_num)

    return render_template("index.html", title="Welcome", user=user, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@app.route("/explore")
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
        .order_by(Post.timestamp.desc()) \
        .paginate(page, app.config['POSTS_PER_PAGE'], False)\

    return render_template("index.html", title="Explore", user=current_user, posts=posts.items)


@app.route("/user/<username>", methods=["GET", "POST"])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    user = current_user

    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        user.username = form.username.data
        user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for("user", username=user.username))
    elif request.method == 'GET':
        form.username.data = user.username
        form.about_me.data = user.about_me

    return render_template("edit_profile.html", form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = "/index"

        return redirect(next_page)

    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        flash("Congratulation, you are now registered member")
        return redirect(url_for("index"))

    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
