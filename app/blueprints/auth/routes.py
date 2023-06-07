from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask import request
from app.forms import CommissionForm, ContactForm
from app.models import User, Commission
from flask_login import current_user
import pandas as pd

from . import bp
from app.forms import RegisterForm
from app.forms import SigninForm

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            flash(f'Welcome back, {form.username.data}. You are signed in.', "success")
            login_user(user)
            return redirect(url_for('main.home'))
        else:
            flash(f"{form.username.data}/password not found", "warning")
    return render_template('signin.jinja', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out', 'success')
    return redirect(url_for('main.home'))

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        user = User.query.filter_by(username=form.username.data).first()
        email = User.query.filter_by(email=form.email.data).first()
        if not email and not user:
            u = User(username=form.username.data,email=form.email.data,first_name=form.first_name.data,last_name=form.last_name.data)
            u.password = u.hash_password(form.password.data)
            u.add_token()
            u.commit()
            flash(f"{form.username.data} registered!", "success")
            return redirect(url_for("auth.signin"))
        if user:
            flash(f'{form.username.data} is already taken, please try again', 'warning')
        else:
            flash(f'{form.email.data} is already taken, please try again', 'warning')
    return render_template('register.jinja', form=form)

@bp.route('/commission', methods=["GET","POST"])
@login_required
def get_commission():
    form = CommissionForm()
    if form.validate_on_submit():
        c = Commission(name=form.name.data,email=form.email.data,subject=form.subject.data,request=form.message.data,budget=form.budget.data)
        c.user_id = current_user.user_id
        c.commit()
        flash('Request Sent!', 'success')
        return redirect(url_for('social.user_page', username=current_user.username))
    else:
        return render_template('commission.jinja', form=form)

@bp.route('/contactus', methods=["GET", "POST"])
def get_contact():
    form = ContactForm()
    if request.method == 'POST':
        name = request.form["name"]
        email = request.form["email"]
        subject = request.form["subject"]
        message = request.form["message"]
        res = pd.DataFrame({'name': name, 'email': email, 'subject': subject, 'message': message}, index=[0])
        res.to_csv('./contactusMessage.csv')
        flash('Message Sent!', 'success')
        return redirect(url_for('social.user_page', username=current_user.username))
    else:
        return render_template('contact.jinja', form=form)
