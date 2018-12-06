from flask_wtf import FlaskForm
from flask import current_app
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, Length
from flask_ckeditor import CKEditorField
from coolog.models import Category


# 普通用户评论表单
class CommentForm(FlaskForm):
	author = StringField("你的名字", validators=[DataRequired(), Length(1,30)])
	body = TextAreaField("你的评论", validators=[DataRequired()])
	submit = SubmitField("提交")


# 管理员专用的评论表单
class AdminCommentForm(CommentForm):
	author = HiddenField()


# 管理员的登陆表单
class LoginForm(FlaskForm):
	username = StringField("用户名", validators=[DataRequired(), Length(1,60)])
	password = PasswordField("密码", validators=[DataRequired(), Length(1,128)])
	remember = BooleanField("记住我")
	submit = SubmitField("登陆")


# 修改或新建博文的表单
class PostForm(FlaskForm):
	title = StringField("标题", validators=[DataRequired()])
	# 这个category的choices属性在视图函数admin.new_post()设置
	# 因为sqlalchemy查询数据库需要应用上下文，而这里没有
	category = SelectField("分类", coerce=int, default=1)
	body = CKEditorField("正文", validators=[DataRequired()])
	submit = SubmitField("提交")


# 新建分类的表单
class CategoryForm(FlaskForm):
	name = StringField("输入分类名", validators=[DataRequired(), Length(1,20)])
	submit = SubmitField("提交")
