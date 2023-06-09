from flask import Flask, render_template, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required
from flask import request
from app.forms import ContactForm
from app.models import User
from flask_login import current_user
import pandas as pd
import hashlib
import pendulum
import requests
import time
import os
from . import bp
from app.forms import RegisterForm
from app.forms import SigninForm


# - ROUTE FOR COMIC SEARCH PAGE ===========================================
@bp.route('/comic_search')
@login_required
def comic_search_page():
    return render_template('comic_search.jinja')

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

# LOGOUT ROUTE/FUNCTION =========================================
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out', 'success')
    return redirect(url_for('main.home'))

# REGISTER ROUTE/FUNCTION =========================================
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


# CONTACT ROUTE/FUNCTION =========================================
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



# GET MARVEL COMIC API ==========================================

def get_marvel_comic(title):
    # Get public_key from environment variables =================
    public_key = os.environ.get('PUBLIC_KEY')
    # Get timestamp for Marvel API Call =============================
    ts = pendulum.now('UTC')
    ts = ts.to_iso8601_string()
    # Create Hash for Marvel API Call =============================
    hash = hashlib.md5()
    hash.update(ts.encode('utf-8'))
    hash.update(os.environ.get('PRIVATE_KEY').encode('utf-8'))
    hash.update(os.environ.get('PUBLIC_KEY').encode('utf-8'))
    # Set Params for Marvel API Call =============================
    params = {
        'apikey': public_key,
        'ts': ts,
        'hash': hash.hexdigest(),
        'title': title
    }
    # API Call ===============================================================
    response = requests.get(
        'https://gateway.marvel.com:443/v1/public/comics', params=params)
    if response.status_code == 200:
        print(response.json())
        data = response.json()
        try:
            # Create Variables from JSON data ===============================
            title_name = data["data"]["results"][0]["title"]
            description = data["data"]["results"][0]["description"]
            on_sale = data["data"]["results"][0]["dates"][0]["date"]
            comic_resource = data["data"]["results"][0]["urls"][0]["url"]
            thumbnail = data["data"]["results"][0]["thumbnail"]["path"]
            extension = data["data"]["results"][0]["thumbnail"]["extension"]
            thumbnail = f"{thumbnail}.{extension}"
            print({"title": title_name, "Description": description, "First Available": on_sale,
                  "View at Marvel": comic_resource, "thumbnail": thumbnail})
            # FORMAT VARIABLES FOR RENDERING ============================
            dis_title = f'<strong>{title_name}</strong>'
            dis_desc = f'<font color="white">Description:</font> {description}'
            dis_date = f'<font color="white">Available Date:</font> {on_sale}'
            dis_link = f'<font color="white">{title_name} Comic Collection via</font><font color="red"> MARVEL</font><font color="white">:</font><br/><a href="{comic_resource}" target="_blank">{comic_resource}</a>'
            thumbnail = f"{thumbnail}"
            # Return Formatted Variables ============================
            return {"title": dis_title, "Description": dis_desc, "First Available": dis_date, "View at Marvel": dis_link, "thumbnail": thumbnail}
        # Error Handling =================================================
        except:
            return None
    else:
        flash(
            f'Error {response.status_code}: {response.text}. Please try again.', 'warning')

@bp.route('/comic_search', methods=['GET','POST'])
@login_required
def title_page_post():
    if request.method == 'POST':
        title = request.form.get('search_title')
        if not title:
            flash(f"Error, Please Enter a Comic Title.", "warning")
        data = get_marvel_comic(title)
        if data:
            return render_template('comic_search.jinja', data=data)
        if data == None:
            flash(f'Invalid Comic or Comic Not Found.', "warning")
            return render_template('comic_search.jinja')
    else:
        return render_template('comic_search.jinja')