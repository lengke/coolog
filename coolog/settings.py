import os


class BaseConfig():
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SECRET_KEY = os.getenv("SECRET_KEY", "itissecrETyCantGuESs")
	CKEDITOR_SERVE_LOCAL = True
	POST_PER_PAGE = 5
	COMMENT_PER_PAGE = 15
	MANAGE_POST_PER_PAGE = 10
	MANAGE_COMMENT_PER_PAGE = 30
	MAIL_SERVER = "smtp.qq.com"
	MAIL_SUPPRESS_SEND = False
	MAIL_PORT = 465
	MAIL_USE_SSL = True
	MAIL_USE_TLS = False
	MAIL_USERNAME = "20167591@qq.com"
	MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
	MAIL_DEFAULT_SENDER = ("20167591@qq.com")


class DevelopmentConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")



class ProductionConfig(BaseConfig):
	SQLALCHEMY_DATABASE_URI = os.getenv("DB_URI")


configlist = {
	"development": DevelopmentConfig,
	"production": ProductionConfig
}

