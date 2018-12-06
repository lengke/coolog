from coolog import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


# 创建管理员数据模型
# 本例中，管理员其实只有1个
class Admin(db.Model, UserMixin):
	__tablename__ = "admin"
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(30))
	password_hash = db.Column(db.String(256))
	name = db.Column(db.String(30))
	about = db.Column(db.Text)
	# 博客的大标题
	blog_title = db.Column(db.String(60))
	# 博客的子标题
	blog_sub_title = db.Column(db.String(100))

	# 为管理员生成密码hash值的方法
	def set_password(self,password):
		self.password_hash = generate_password_hash(password)

	# 为管理员校验密码hash值的方法
	def validate_password(self,password):
		return check_password_hash(self.password_hash, password)


# 创建文章分类的数据模型
class Category(db.Model):
	__tablename__= "category"
	id = db.Column(db.Integer, primary_key=True)
	name= db.Column(db.String(30), unique=True)
	# 定义与Post模型的反向关系属性posts
	posts = db.relationship("Post", back_populates="its_category")


# 创建博客文章的数据模型
class Post(db.Model):
	__tablename__= "post"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	body = db.Column(db.Text)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)
	can_comment = db.Column(db.Boolean, default=True)
	# 定义一个外键，跟Category模型的id字段相关联
	category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
	# 定义与Category模型的关系属性its_category
	its_category = db.relationship("Category", back_populates="posts")
	# 定义与Comment模型的关系属性its_comments
	# 并且设置级联操作，删除文章会使其评论也被删除
	its_comments = db.relationship("Comment", back_populates="its_post", cascade="all")


# 创建文章的评论数据模型
class Comment(db.Model):
	__tablename__="comment"
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.Text)
	author = db.Column(db.String(30))
	from_admin = db.Column(db.Boolean, default=False)
	reviewed = db.Column(db.Boolean, default=False)
	timestamp = db.Column(db.DateTime, default=datetime.utcnow)

	# 在评论这一侧，定义与post.id相关联的外键
	post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
	# 定义与Post模型的关系属性its_post
	its_post = db.relationship("Post", back_populates="its_comments")

	# 评论与回复之邻接列表关系的设置
	# 同一张表里建立外键
	replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))

	# replied表示拥有回复的评论，是一的那一侧
	# 所以remote_side要在这里定义
	replied = db.relationship("Comment", back_populates="replies", remote_side=[id])

	# replies是某条评论的全部回复，是多的那一侧
	# 所以cascade级联操作要在这里定义
	replies = db.relationship("Comment", back_populates="replied", cascade="all")

