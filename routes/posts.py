from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, Response
from flask_login import login_required, current_user
from models import Post, Like, Comment, db
from forms import PostForm, CommentForm

posts_bp = Blueprint('posts', __name__)


def _read_image(file_field):
    f = file_field.data
    if not f or not getattr(f, 'filename', None):
        return None, None
    return f.read(), f.mimetype or 'image/jpeg'


@posts_bp.route('/post/<int:post_id>/image')
def image(post_id):
    post = Post.query.get_or_404(post_id)
    if not post.image_data:
        abort(404)
    return Response(post.image_data, mimetype=post.image_mimetype or 'image/jpeg')


@posts_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        img_data, img_mime = _read_image(form.image)
        if not img_data:
            flash('სურათი სავალდებულოა.', 'danger')
            return render_template('posts/create.html', form=form)
        post = Post(
            title=form.title.data,
            description=form.description.data,
            image_data=img_data,
            image_mimetype=img_mime,
            user_id=current_user.id
        )
        db.session.add(post)
        db.session.commit()
        flash('პოსტი გამოქვეყნდა!', 'success')
        return redirect(url_for('main.feed'))
    return render_template('posts/create.html', form=form)


@posts_bp.route('/post/<int:post_id>')
@login_required
def view(post_id):
    post = Post.query.get_or_404(post_id)
    comment_form = CommentForm()
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.created_at.desc()).all()
    return render_template('posts/post.html', post=post, form=comment_form, comments=comments)


@posts_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        img_data, img_mime = _read_image(form.image)
        if img_data:
            post.image_data = img_data
            post.image_mimetype = img_mime
        db.session.commit()
        flash('პოსტი განახლდა!', 'success')
        return redirect(url_for('posts.view', post_id=post.id))
    return render_template('posts/edit.html', form=form, post=post)


@posts_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.user_id != current_user.id:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('პოსტი წაიშალა.', 'info')
    return redirect(url_for('main.feed'))


@posts_bp.route('/post/<int:post_id>/like', methods=['POST'])
@login_required
def like(post_id):
    Post.query.get_or_404(post_id)
    existing = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()
    if existing:
        db.session.delete(existing)
    else:
        db.session.add(Like(user_id=current_user.id, post_id=post_id))
    db.session.commit()
    return redirect(request.referrer or url_for('posts.view', post_id=post_id))


@posts_bp.route('/post/<int:post_id>/comment', methods=['POST'])
@login_required
def comment(post_id):
    Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        db.session.add(Comment(content=form.content.data, user_id=current_user.id, post_id=post_id))
        db.session.commit()
    return redirect(url_for('posts.view', post_id=post_id))
