from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from models import Post

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@login_required
def feed():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=9, error_out=False
    )
    return render_template('index.html', posts=posts)


@main_bp.route('/search')
@login_required
def search():
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('main.feed'))
    posts = Post.query.filter(
        Post.title.ilike(f'%{q}%') | Post.description.ilike(f'%{q}%')
    ).order_by(Post.created_at.desc()).all()
    return render_template('search.html', posts=posts, q=q)
