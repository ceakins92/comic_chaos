# - IMPORT MODULES =======================================================

from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from flask_login import login_required
import requests
import hashlib
import pendulum
import os
import urllib.request, json
from . import bp
from app.models import Post, User
from app.blueprints.api.helpers import token_required


# - ROUTE FOR char_page ===================================================

@bp.route('/char_page')
@login_required
def char_page():
    return render_template('char_page.jinja')

# - Character search API ==================================================

def get_marvel_character(name):
    print(name)
    # - Get Public Key from env ==
    public_key = os.environ.get('PUBLIC_KEY')
    # - Get Timestamp for Marvel API requirement ========
    ts = pendulum.now('UTC')
    ts = ts.to_iso8601_string()
    # - Generate Hash for Marvel API requirement ====
    hash = hashlib.md5()
    hash.update(ts.encode('utf-8'))
    hash.update(os.environ.get('PRIVATE_KEY').encode('utf-8'))
    hash.update(os.environ.get('PUBLIC_KEY').encode('utf-8'))
    # - Set required Params ======
    params = {
        'apikey': public_key,
        'ts': ts,
        'hash': hash.hexdigest(),
        'name': name
    }
    # - API call =========
    response = requests.get(
        'http://gateway.marvel.com/v1/public/characters', params=params)
    # - Check Response code and generate data from json response ====
    if response.status_code == 200:
        print(response.json())
        data = response.json()
        # - Format data to retrieve desired output ======
        try:
            # - Create Variables for Data=========
            char_name = data["data"]["results"][0]["name"]
            description = data["data"]["results"][0]["description"]
            comics_avail = data["data"]["results"][0]["comics"]["available"]
            comic_resource = data["data"]["results"][0]["urls"][2]["url"]
            thumbnail = data["data"]["results"][0]["thumbnail"]["path"]
            extension = data["data"]["results"][0]["thumbnail"]["extension"]
        # - Format Variables as Strings========
            name_title = f'<strong>{char_name}</strong>'
            desc_title = f'<font color="white">Description:</font> {description}'
            comic_num = f'<font color="white">Comics Appeared In:</font> {comics_avail}'
            comic_res = f'<font color="white">{char_name} Comic Collection via</font><font color="red"> MARVEL</font><font color="white">:</font><br/><a href="{comic_resource}" target="_blank">{comic_resource}</a>'
            thumbnail = f"{thumbnail}/landscape_incredible.{extension}"
        # - Return Data=============
            return {"Character Name": name_title, "Description (if available)": desc_title, "Comics Appeared In": comic_num, "Comic Collection via Marvel": comic_res,"thumbnail": thumbnail}
    # - Error handling========
        except:
            return None
    # - Error handling for API Response====
    else:
        flash(f'Error {response.status_code}: {response.text}. Please try again.', 'warning')


# User input and error handling ========================================

@bp.route('/char_page', methods=['GET','POST'])
@login_required
def char_page_post():
    if request.method == 'POST':
        name = request.form.get('search_char')
        if not name:
            flash(f"Error, Please Enter a Character Name.", "warning")
        data = get_marvel_character(name)
        if data:
            return render_template('char_page.jinja', data=data)
        if data == None:
            flash(f'Invalid Character or Character Not Found.', "warning")
            return render_template('char_page.jinja')
    else:
        return render_template('char_page.jinja')


# On Sale Function/API, Not Implemented =============================
def on_sale():
   url = "https://www.comics.org/on_sale_weekly/?_export=json"
   response = urllib.request.urlopen(url)
   print(response,'response')
   sales_data = response.read()
   print(sales_data,'sales_data')
   sdict = json.loads(sales_data)
   print(sdict, 'sdict')
   for issues in sdict:
        print(issues,'issues')
        return render_template('marketplace.jinja', cover=issues["Covers"], publisher=issues["Publisher"], issue=issues["Issue"], sale_date=issues["On-sale Date"])
      

# - Output user posts local API ===============================================

@bp.get('/posts')
@token_required
def api_posts(user):
    result = []
    posts = Post.query.all()
    for post in posts:
        result.append({
            'id':post.id,
            'subject':post.subject,
            'body':post.body,
            'related_comics':post.related_comics,
            'related_characters':post.related_characters,
            'mentions':post.mentions,
            'timestamp':post.date_created, 
            'author':post.user_id
            })
    return jsonify(result), 200

# - Posts by Username local =================================================

@bp.get('/posts/<username>')
@token_required
def user_posts(user,username):
    user = User.query.filter_by(username=username).first()
    if user:
      return jsonify([{
            'id':post.id,
            'subject':post.subject,
            'body':post.body,
            'related_comics':post.related_comics,
            'related_characters':post.related_characters,
            'mentions':post.mentions,
            'timestamp':post.date_created, 
            'author':post.user_id
              } for post in user.posts]), 200
    return jsonify([{'message':'Invalid Username'}]), 404 

# - Posts by ID local ======================================================

@bp.get('/post/<id>')
@token_required
def get_post(user,post_id):
    try:
      post = Post.query.get(post_id)
      return jsonify([{
            'id':post.id,
            'subject':post.subject,
            'body':post.body,
            'related_comics':post.related_comics,
            'related_characters':post.related_characters,
            'mentions':post.mentions,
            'timestamp':post.date_created, 
            'author':post.user_id
                }])
    except: 
      return jsonify([{'message':'Invalid Post Id'}]), 404
    
    
# - Post Creation ======================================================

@bp.post('/post')
@token_required
def make_post(user):
    try:
        content = request.json
        post = Post(char_name=content.get('char_name'),user_id=user.user_id)
        post.commit()
        return jsonify([{'message':'Post Created','body':post.body}])
    except:
       jsonify([{'message':'invalid form data'}]), 401

