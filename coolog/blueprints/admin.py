from flask import Blueprint, render_template, url_for, redirect, request, flash
from coolog.models import *
from coolog.forms import *
from coolog.utils import redirect_back
from flask_login import login_required


admin_bp = Blueprint("admin", __name__)


# 管理博文的视图函数，包括：
# 1、管理文章（展示、新建、删除）
# 2、新建文章
# 3、删除文章
# 4、修改文章


# 管理博客文章
@admin_bp.route("/post/manage")
@login_required
def manage_post():
	page = request.args.get("page", 1, type=int)
	per_page = current_app.config["MANAGE_POST_PER_PAGE"]
	pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
	posts = pagination.items
	return render_template("admin/manage_post.html", pagination=pagination, posts=posts)


# 新建博文
@admin_bp.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
	form = PostForm()
	# 神操作预警
	# sqlalchemy查询数据库需要应用上下文，所以放到这个视图函数里
	# 既然category是在PostForm()中的一个属性，那么就用form.category来取出它并赋值！
	form.category.choices = [(item.id, item.name) for item in Category.query.order_by(Category.name).all()]

	if form.validate_on_submit():
		post = Post(
			title = form.title.data,
			body = form.body.data,
			category_id = form.category.data
		)
		db.session.add(post)
		db.session.commit()
		flash("新文章发表成功", "success")
		return redirect(url_for("blog.show_post", post_id = post.id))

	return render_template("admin/new_post.html", form=form)


#删除博文
@admin_bp.route("/post/delete/<int:post_id>", methods=["POST"])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	db.session.delete(post)
	db.session.commit()
	flash("文章删除成功", "success")
	return redirect_back()


#修改博文
@admin_bp.route("/post/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):
	form = PostForm()
	# 先从数据库里查出来这篇文章的现有内容
	# 渲染在表格中
	form.category.choices = [(item.id, item.name) for item in Category.query.order_by(Category.name).all()]
	post = Post.query.get_or_404(post_id)

	# 注意if代码块的顺序不能变，否则编辑不会生效
	if form.validate_on_submit():
		post.title = form.title.data,
		post.body = form.body.data,
		post.category_id =form.category.data
		db.session.commit()
		flash("文章编辑成功", "success")
		return redirect(url_for("blog.show_post", post_id=post.id))

	form.title.data = post.title
	form.category.data = post.category_id
	form.body.data = post.body
	return render_template("admin/edit_post.html", form=form)


# 管理分类的视图函数，包括：
# 1、管理分类（展示、新建、删除）
# 2、删除分类
# 3、编辑分类
# 注意默认分类是不可被删除和修改的，也不可被重名

# 管理分类
@admin_bp.route("/category/manage", methods=["POST", "GET"])
@login_required
def manage_category():
	form = CategoryForm()

	#新建分类的处理
	if form.validate_on_submit():
		# 判断新建分类的名字是否已经重复
		# 若重复则不允许创建
		if Category.query.filter_by(name=form.name.data).first() is not None:
			flash("分类名称重复，创建失败", "danger")
			return redirect(url_for("admin.manage_category"))
		else:
			category = Category(
				name = form.name.data
			)
			db.session.add(category)
			db.session.commit()
			flash("新分类创建成功", "success")
			return redirect(url_for("admin.manage_category"))

	return render_template("admin/manage_category.html", form=form)


#删除分类
@admin_bp.route("/category/delete/<int:category_id>", methods=["POST"])
@login_required
def delete_category(category_id):
	# 再次判断，保证默认分类不被删除
	if category_id == 1:
		flash("默认分类不能被删除", "danger")
		return redirect(url_for("admin.manage_category"))

	category = Category.query.get_or_404(category_id)

	# 将删除的分类所属的文章变更为默认分类
	if category.posts:
		print(category.posts)
		for post in category.posts:
			post.category_id = 1
			print(post.category_id)
			db.session.commit()

	db.session.delete(category)
	db.session.commit()
	flash("分类删除成功", "success")
	return redirect_back()


#编辑分类名称
@admin_bp.route("/category/edit/<int:category_id>", methods=["GET","POST"])
@login_required
def edit_category(category_id):
	if category_id==1:
		flash("默认分类不可编辑", "danger")
		return redirect_back()
	form = CategoryForm()
	category = Category.query.get_or_404(category_id)
	if form.validate_on_submit():
		if form.name.data == "默认分类":
			flash("修改失败！默认分类只能有一个", "danger")
			return redirect_back()
		category.name = form.name.data
		db.session.commit()
		flash("分类名称修改成功", "success")
		return redirect_back()

	form.name.data = category.name
	return render_template("admin/edit_category.html", form = form)


# 管理评论的视图函数，包括：
# 1、管理评论（含展示、审核、禁评、删除）
# 2、删除评论
# 3、审核评论


# 管理评论
@admin_bp.route("/comment/manage", methods=["POST", "GET"])
@login_required
def manage_comment():
	page = request.args.get("page", 1, type=int)
	per_page = current_app.config["MANAGE_COMMENT_PER_PAGE"]
	pagination = Comment.query.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
	comments = pagination.items
	return render_template("admin/manage_comment.html", pagination=pagination, comments=comments)


# 删除评论
@admin_bp.route("/comment/delete/<int:comment_id>", methods=["POST"])
@login_required
def delete_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	db.session.delete(comment)
	db.session.commit()
	flash("评论删除成功", "success")
	return redirect_back()


# 审核评论
@admin_bp.route("/comment/review/<int:comment_id>", methods=["POST","GET"])
@login_required
def review_comment(comment_id):
	comment = Comment.query.get_or_404(comment_id)
	comment.reviewed = not comment.reviewed
	db.session.commit()
	flash("评论审核状态已改变", "success")
	return redirect_back()


#关闭或开启博文的评论
@admin_bp.route("/post/close/<int:post_id>", methods=["POST","GET"])
@login_required
def close_comment(post_id):
	post = Post.query.get_or_404(post_id)
	post.can_comment = not post.can_comment
	db.session.commit()
	flash("成功操作了评论区", "success")
	return redirect_back()

