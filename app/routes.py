from werkzeug.urls import url_parse

from app import app, db
from flask import render_template, flash, redirect, url_for
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user, login_required
from flask import request
from app.models import User


@app.route("/")
@app.route("/index")
@login_required
def index():
    user = current_user
    posts = [
        {
            "author": {'username': 'john'},
            "body": "test body 1"
        },
        {
            "author": {'username': 'peter'},
            "body": "test body 2"
        }
    ]
    title = ""
    return render_template("index.html", title=title,  user=user, posts=posts)


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
        login_user(user,remember=form.remember_me.data)

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

    return render_template("register.html",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

