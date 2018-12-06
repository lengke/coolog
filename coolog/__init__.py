from flask import Flask, render_template
from coolog.extensions import *
from flask_login import current_user
from coolog.blueprints.blog import blog_bp
from coolog.blueprints.auth import auth_bp
from coolog.blueprints.admin import admin_bp
from coolog.settings import configlist
from coolog.commands import register_commands
from coolog.models import *
from flask_wtf.csrf import CSRFError


# 创建工厂函数
def create_app(config_name="development"):

	app = Flask("coolog")
	# 设置当前启用的config对象
	current_config = configlist.get(config_name)
	app.config.from_object(current_config)
	print("The current_config is %s" % current_config)

	register_extensions(app)
	register_blueprints(app)
	register_commands(app)
	register_template_context(app)
	register_errors(app)
	return app


# 将所有拓展注册到app上面
def register_extensions(app):
	bootstrap.init_app(app)
	moment.init_app(app)
	migrate.init_app(app)
	login_manager.init_app(app)
	db.init_app(app)
	csrf.init_app(app)
	ckeditor.init_app(app)


#将蓝本注册到app上面
def register_blueprints(app):
	app.register_blueprint(blog_bp)
	app.register_blueprint(auth_bp, url_prefix="/auth")
	app.register_blueprint(admin_bp, url_prefix="/admin")


#注册模板上下文
#使admin和categories在全局模板中可直接使用
#免除了每个视图函数渲染的麻烦
def register_template_context(app):
	@app.context_processor
	def make_template_context():
		admin = Admin.query.first()
		categories = Category.query.order_by(Category.name).all()
		# 如果管理员已登陆则查出未审核评论的数量
		if current_user.is_authenticated:
			unread_comments = Comment.query.filter_by(reviewed=False).count()
		else:
			unread_comments = None
		return dict(admin=admin, categories=categories, unread_comments=unread_comments)


# 注册错误处理视图函数
def register_errors(app):

	@app.errorhandler(404)
	def error_404(e):
		return render_template("errors/404.html"), 404

	@app.errorhandler(400)
	def error_400(e):
		return render_template("errors/400.html"), 400

	@app.errorhandler(500)
	def error_500(e):
		return render_template("errors/500.html"), 500

	@app.errorhandler(CSRFError)
	def error_csrf(e):
		return render_template("errors/400.html", description = e.description),400

