from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Mail
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


bootstrap = Bootstrap()
moment = Moment()
mail = Mail()
login_manager = LoginManager()
ckeditor = CKEditor()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()

login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = "请先登录"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
	from coolog.models import Admin
	user = Admin.query.get(int(user_id))
	return user
