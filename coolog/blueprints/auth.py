from flask import Blueprint, render_template, request, current_app, flash, redirect, url_for
from coolog.models import *
from coolog.forms import *
from flask_login import login_user, logout_user, login_required
from coolog.utils import redirect_back

auth_bp=Blueprint("auth", __name__)


# 管理员登陆的视图函数
@auth_bp.route("/login", methods=["POST", "GET"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Admin.query.filter_by(username=form.username.data).first()
		if user is not None and user.validate_password(form.password.data):
			login_user(user, form.remember.data)
			flash("登陆成功", "success")
			return redirect_back()
		else:
			flash("用户名或密码错误", "danger")
	return render_template("auth/login.html", form=form)


# 管理员登出
@auth_bp.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
	logout_user()
	flash("您已登出", "info")
	return redirect_back()

