from flask import Flask, request, jsonify, render_template
from requests import get
import hashlib
import os
import urllib.request, json
from . import bp
from app.models import Post, User
from app.blueprints.api.helpers import token_required



@bp.route('/char_page')
def char_page():
    return render_template('char_page.jinja')

@bp.route('/char_page', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        char_name = request.form["search_char"]
        Marvel_Char(char_name)
    else:
        return render_template("/char_page")

class Marvel_Char():
    def __init__(self,char_name):
        self.name = char_name
        self.image = None
        self.call_marvel_api()

    def call_marvel_api(self):
        if isinstance(self.name, str) and self.name.isalpha():
            self.name = self.name.lower()
        response = get(f'https://metron.cloud/api/character/?name={self.name}')
        if response.status_code == 200:
            print('Success')
            data = response.json()
            self.name = data.results[0]["name"]
            self.image = data.results[0]["cover"]
            if not self.image:
                self.image = None
        else:
            print(f'Error status code {response.status_code}')
        return self.name

## def get_character(PUBLIC_KEY,PRIVATE_KEY,name):
##    now=pendulum.now('UTC')
##    now=now.to_iso8601_string()
##
##   m=hashlib.md5()
##   m.update(now.encode('utf8'))
##   m.update(os.environ.get({PRIVATE_KEY}).encode('utf8'))
##   m.update(os.environ.get({PUBLIC_KEY}).encode('utf8'))
##
##   endpoint = f'https://gateway.marvel.com:443/v1/public/characters?nameStartsWith={name}&limit=1'
##   resp = requests.get(endpoint, params={"apikey": PUBLIC_KEY, "ts": now, "hash": m.hexdigest()}).json()
##
##   try:
##      name = resp["data"]["results"][0]["name"]
##      description = resp["data"]["results"][0]["description"]
##      thumbnail = resp["data"]["results"][0]["thumbnail"]["path"]
##      extension = resp["data"]["results"][0]["thumbnail"]["extension"]
##      thumbnail = f"{thumbnail}/landscape_incredible.{extension}"
##      print({"name": name, "description": description, "thumbnail": thumbnail})
##      return {"name": name, "description": description, "thumbnail": thumbnail}
##   except IndexError:
##      return render_template("/char_page")
   
##@bp.route('/char_page', methods=["GET", "POST"])
##def index():
##    if request.method == "POST":
##        name = request.form["search"]
##        data = get_character(os.environ.get('PUBLIC_KEY'),os.environ.get('PRIVATE_KEY'), name)
##        return render_template("/char_page", data=data)
    
##    return render_template("/char_page")


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

