from flask import Blueprint, render_template, url_for, request
from flask_login import current_user, login_required
from flaskblog.models import Post


main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
@login_required
def home_page():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page = 5, page=page)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('home.html', posts=posts, image_file=image_file)


@main.route('/about')
@login_required
def about_page():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('about.html', title='About', image_file=image_file)


