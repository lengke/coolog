import click, time
from coolog.fakes import fake_admin, fake_category, fake_comment, fake_post
from coolog.extensions import db
from coolog.models import *

"""
flask cleardb 清空重建数据库，无任何实际数据生成，慎用
flask fakeall 清空重建数据库，并用假数据填充 默认用户名和密码是admin admin
flask init 初始化项目，用户名和密码自定义输入
"""

def register_commands(app):
	# 清空数据库并重建的命令
	@app.cli.command()
	@click.option("--drop", is_flag=True, help="delete all tables")
	def cleardb(drop):
		if drop:
			db.drop_all()
			click.echo("databases drop_all succeed!")
			time.sleep(1)
			click.echo("now re-create all tables!")
			db.create_all()
			click.echo("Work is Done!")

	# 为数据库生成假数据的命令
	@app.cli.command()
	@click.option("--category", default=10, help="number of categories")
	@click.option("--post", default=30, help="number of posts")
	@click.option("--comment", default=500, help="number of comments")
	def fakeall(category, post, comment):
		db.drop_all()
		db.create_all()
		# 创建管理员
		click.echo("creating admin data")
		fake_admin()
		# 创建文章分类
		click.echo("creating %d categories data" % category)
		fake_category(category)
		# 创建博文
		click.echo("creating %d posts data" % post)
		fake_post(post)
		#创建评论
		click.echo("creating %d comments data" % comment)
		fake_comment(comment)
		click.echo("All fake data created! Work is Done!")

	# 初始化管理员账号密码或默认分类的命令
	@app.cli.command()
	@click.option("--username", prompt=True, help="输入管理员用户名")
	@click.password_option("--password", prompt=True, help="输入管理员密码")
	def init(username, password):
		click.echo("首先重新生成数据库")
		db.drop_all()
		db.create_all()

		admin= Admin.query.first()

		# 创建博文默认分类
		click.echo("正在新建博文的默认分类")
		category = Category(name="默认分类")
		db.session.add(category)
		click.echo("数据库和默认分类初始化完成")

		click.echo("正在新建管理员账号和密码")
		admin = Admin(
			username = username,
			name = "Leng Ke",
			about="关注我的微信公众号：姓冷名轲（ID:woshilengke）",
			blog_title="浪子不回头",
			blog_sub_title="Powered by Python Flask"
		)
		admin.set_password(password)
		db.session.add(admin)

		db.session.commit()


