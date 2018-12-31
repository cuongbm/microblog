from datetime import datetime

from flask import render_template, flash, redirect, url_for, g
from flask import request, current_app
from flask_login import current_user, login_required

from app import db
from app.main.forms import PostForm, SearchForm
from app.models import User, Post
from app.main import bp


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
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
        return redirect(url_for("main.index"))

    posts = user.followed_posts()\
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)\

    prev_url = None
    if posts.has_prev:
        prev_url = url_for('main.index', page=posts.prev_num)

    next_url = None
    if posts.has_next:
        next_url = url_for('main.index', page=posts.next_num)

    return render_template("index.html", title="Welcome", user=user, posts=posts.items, form=form, next_url=next_url, prev_url=prev_url)


@bp.route("/explore")
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query\
        .order_by(Post.timestamp.desc()) \
        .paginate(page, current_app.config['POSTS_PER_PAGE'], False)\

    prev_url = None
    if posts.has_prev:
        prev_url = url_for('main.explore', page=posts.prev_num)

    next_url = None
    if posts.has_next:
        next_url = url_for('main.explore', page=posts.next_num)

    return render_template("index.html", title="Explore", user=current_user, posts=posts.items, next_url=next_url, prev_url=prev_url)


@bp.route("/user/<username>", methods=["GET", "POST"])
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page,
                               current_app.config['POSTS_PER_PAGE'])

    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', posts=posts,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user_popup.html', user=user)