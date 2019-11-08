from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError
from coolog.extensions import db
from coolog.models import Admin, Category, Post, Comment

fake = Faker("zh_CN")

# 创建虚拟的管理员信息
def fake_admin():
	admin= Admin(
		username= "admin",
		name = "Leng Ke",
		about ="关注我的微信公众号：姓冷名轲（ID:woshilengke）",
		blog_title ="浪子不回头",
		blog_sub_title="Powered by Python Flask"
	)
	admin.set_password("admin")
	db.session.add(admin)
	db.session.commit()

# 创建虚拟的博文类别信息
# 注意类别是unique所以要考虑出错的回滚
def fake_category(count):
	#先创建一个肯定会用到的默认分类
	#新建的博文默认是归到这个分类
	category = Category(name="默认分类")
	db.session.add(category)

	for i in range(count):
		category = Category(name = fake.word())
		db.session.add(category)
		try:
			# 如果提交出错，则回滚
			db.session.commit()
		except IntegrityError:
			db.session.rollback()


# 创建虚拟的博客文章数据
def fake_post(count):
	for i in range(count):
		post = Post(
			title=fake.sentence(),
			body=fake.text(2000),
			timestamp = fake.date_time_this_year(),
			# 每篇博文还必须指定category_id
			# 随机范围上限取决于创建的虚拟分类数量的多少
			category_id = randint(1, Category.query.count())
		)
		db.session.add(post)
	db.session.commit()


# 创建虚拟的博客评论数据
def fake_comment(count):
	# 生成通过审核了的评论
	for i in range(count):
		comment = Comment(
		body = fake.sentence(),
		author = fake.name(),
		reviewed = True,
		timestamp = fake.date_time_this_year(),
		post_id = randint(1, Post.query.count())
		)
		db.session.add(comment)
	db.session.commit()

	salt = int(count * 0.5)
	# 生成未审核的评论
	for i in range(salt):
		comment = Comment(
			body=fake.sentence(),
			author=fake.name(),
			reviewed=False,
			timestamp=fake.date_time_this_year(),
			post_id=randint(1, Post.query.count())
		)
		db.session.add(comment)
	db.session.commit()

	# 生成管理员的评论
	admin=Admin.query.first()
	for i in range(salt):
		comment = Comment(
			body=fake.sentence(),
			author=admin.name,
			reviewed=True,
			from_admin=True,
			timestamp=fake.date_time_this_year(),
			post_id=randint(1, Post.query.count())
		)
		db.session.add(comment)
	db.session.commit()

	#生成对评论的回复
	for i in range(salt):
		comment = Comment(
			body=fake.sentence(),
			author=fake.name(),
			reviewed=True,
			replied_id=randint(1, Comment.query.count()),
			timestamp=fake.date_time_this_year(),
			post_id=randint(1, Post.query.count())
		)
		db.session.add(comment)
	db.session.commit()




