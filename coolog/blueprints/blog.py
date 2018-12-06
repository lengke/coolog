from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from coolog.models import *
from coolog.forms import *
from flask_login import current_user


blog_bp = Blueprint("blog", __name__)


# 博客首页
@blog_bp.route("/", methods=["GET", "POST"])
def index():
	page = request.args.get("page", 1, type=int)
	per_page = current_app.config["POST_PER_PAGE"]
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
	posts = pagination.items
	return render_template("blog/index.html", pagination=pagination, posts=posts)


# 文章详情页
@blog_bp.route("/post/<int:post_id>", methods=["GET", "POST"])
def show_post(post_id):
	post = Post.query.get_or_404(post_id)
	page = request.args.get("page", 1, type=int)
	per_page = current_app.config["COMMENT_PER_PAGE"]
	pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page, per_page)
	comments = pagination.items
	admin = Admin.query.first()
	# 针对已登陆管理员用户的评论请求处理
	if current_user.is_authenticated:
		form = AdminCommentForm()
		from_admin = True
		reviewed = True
		form.author.data = current_user.name
	# 针对普通用户评论的post请求处理
	else:
		form = CommentForm()
		from_admin = False
		reviewed = False

	# 避免普通用户用admin的名字发评论
	if form.validate_on_submit():

		if current_user.is_authenticated is False and form.author.data == admin.name:
			flash("不可以山寨作者的名字", "danger")
			return redirect(url_for("blog.show_post", post_id=post.id))

		comment= Comment(
			body = form.body.data,
			author = form.author.data,
			from_admin = from_admin,
			reviewed = reviewed,
			post_id = post.id
		)
		# 如果这条评论是对其他评论的回复
		# 则为comment对象添加replied_id属性
		replied_id = request.args.get("replied_comment_id")
		if replied_id:
			comment.replied_id = replied_id

		db.session.add(comment)
		db.session.commit()
		if current_user.is_authenticated:
			flash("管理员，您的评论已成功发表", "success")
		else:
			flash("评论已进入审核队列", "success")
		return redirect(url_for("blog.show_post", post_id=post.id))
	return render_template("blog/post.html", post=post, pagination=pagination, comments=comments, form=form)


# 处理对评论进行回复的视图函数
# 主要是将被回复的评论id和作者名通过url传递回show_post视图函数
@blog_bp.route("/reply/comment/<int:comment_id>")
def reply_comment(comment_id):
	replied_comment = Comment.query.get_or_404(comment_id)
	return redirect(url_for("blog.show_post", post_id=replied_comment.its_post.id, replied_comment_id =comment_id, replied_author=replied_comment.author)+"#comment-form")


# 关于我页面
@blog_bp.route("/about")
def about():
	return render_template("blog/about.html")


# 查看分类文章页面
@blog_bp.route("/category/<int:category_id>")
def show_category(category_id):
	category = Category.query.get_or_404(category_id)
	page = request.args.get("page", 1, type=int)
	per_page = current_app.config["POST_PER_PAGE"]
	pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
	posts = pagination.items
	return render_template("blog/category.html", category=category, pagination=pagination, posts=posts)