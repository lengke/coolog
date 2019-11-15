# [重要]

1、正式上线应将.flaskenv和wsgi.py里面的development改为production

2、还要把./coolg/__init__.py里面的create_app()的默认config改为production，否则上线会出bug。

bug产生的原因是flask init命令生效时，__init__.py里面默认的config是development，所以该命令实际上初始化了coolog_dev这个数据库而不是我们需要的pro数据库


