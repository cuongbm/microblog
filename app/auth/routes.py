from flask import url_for, flash, render_template, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app import db
from app.auth import bp
from app.auth.forms import RegistrationForm, LoginForm, EditProfileForm
from app.models import User


@bp.route("/register", methods=["GET", "POST"])
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

@bp.route("/edit_profile", methods=["GET", "POST"])
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


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = "/index"

        return redirect(next_page)

    return render_template("login.html", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
