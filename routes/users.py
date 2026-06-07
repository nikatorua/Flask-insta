from flask import Blueprint, render_template, redirect, url_for, flash, Response, abort
from flask_login import login_required, current_user
from models import User, Post, db
from forms import ProfileForm

users_bp = Blueprint('users', __name__)


@users_bp.route('/user/<int:user_id>/avatar')
def avatar(user_id):
    user = User.query.get_or_404(user_id)
    if not user.profile_pic_data:
        abort(404)
    return Response(user.profile_pic_data, mimetype=user.profile_pic_mimetype or 'image/jpeg')


@users_bp.route('/users')
@login_required
def list_users():
    users = User.query.order_by(User.username).all()
    return render_template('users/list.html', users=users)


@users_bp.route('/user/<int:user_id>')
@login_required
def profile(user_id):
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.created_at.desc()).all()
    return render_template('users/profile.html', user=user, posts=posts)


@users_bp.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = ProfileForm(obj=current_user)
    if form.validate_on_submit():
        current_user.bio = form.bio.data
        f = form.profile_pic.data
        if f and getattr(f, 'filename', None):
            current_user.profile_pic_data = f.read()
            current_user.profile_pic_mimetype = f.mimetype or 'image/jpeg'
        db.session.commit()
        flash('პროფილი განახლდა!', 'success')
        return redirect(url_for('users.profile', user_id=current_user.id))
    return render_template('users/edit_profile.html', form=form)
