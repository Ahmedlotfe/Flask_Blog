from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required
from .forms import PostForm
from flaskblog.models import Post
from flaskblog import db




posts = Blueprint('posts', __name__)




@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        flash('Your Post has been created!', category='success')
        return redirect(url_for('main.home_page'))
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('create_post.html', title='New Post', form=form, legend='New Post', image_file=image_file)


@posts.route('/post/<int:post_id>')
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('post.html', title=post.title, post=post, image_file=image_file)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Done! Your post has been updated', category='success')
        return redirect(url_for('posts.post', post_id=post_id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', image_file=image_file)



@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    flash('Done! Your post has been deleted', category='success')
    return redirect(url_for('main.home_page'))


