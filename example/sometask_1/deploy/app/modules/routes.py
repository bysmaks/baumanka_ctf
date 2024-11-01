import secrets
from flask import Flask,render_template, redirect, render_template_string, url_for, flash, request, abort
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlencode
from sqlalchemy import desc, or_
from requests import post
from re import compile
from json import dumps
import datetime


from modules.functions import save_bg_picture, save_profile_picture, delete_old_images, save_tweet_picture
from modules.modals import User_mgmt, Post, Retweet, Timeline, Bookmark
from modules.forms import Signup, Login, UpdateProfile, createTweet
from modules import app,db

from os import getenv

USERNAME_REGEX = compile("^(?=[a-zA-Z0-9._]{2,20}$)(?!.*[_.]{2})[^_.].*[^_.]$")
OAUTHURL = 'https://oauth.yandex.ru/'
CLIENT_ID = getenv('CLIENT_ID')
CLIENT_SECRET = getenv('CLIENT_SECRET')
BASEURL = getenv('BASEURL')

def usernameValidator(username):
    return USERNAME_REGEX.match(username) is not None


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():

    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form_sign = Signup()
    form_login = Login()

    if form_sign.validate_on_submit():
        if not usernameValidator(form_sign.username.data):
            return render_template('errorV.html')
        hashed_password = generate_password_hash(form_sign.password.data, method='sha256')
        x = datetime.datetime.now()
        creation = str(x.strftime("%B")) +" "+ str(x.strftime("%Y")) 
        new_user = User_mgmt(username=form_sign.username.data, email=form_sign.email.data, password=hashed_password, date=creation)
        db.session.add(new_user)
        db.session.commit()
        return render_template('sign.html')

    if form_login.validate_on_submit():
        user_info = User_mgmt.query.filter_by(username=form_login.username.data).first()
        if user_info:
            if check_password_hash(user_info.password, form_login.password.data):
                login_user(user_info, remember=form_login.remember.data)
                return redirect(url_for('dashboard'))
            else:
                return render_template('errorP.html')
        else:
            return render_template('errorU.html')

    return render_template('start.html',form1=form_sign,form2=form_login)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    update = UpdateProfile()
    profile_pic = url_for('static',filename='Images/Users/profile_pics/' + current_user.image_file)
    bg_pic = url_for('static',filename='Images/Users/bg_pics/' + current_user.bg_file)

    page = request.args.get('page',1,type=int)
    all_posts = Post.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Post.id))\
        .paginate(page=page,per_page=5)
    retweets = Retweet.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Retweet.id))
    
    return render_template('account.html', profile=profile_pic,background=bg_pic,update=update,timeline=all_posts, retweets=retweets)

@app.route('/UpdateInfo',methods=['GET','POST'])
@login_required
def updateInfo():

    update = UpdateProfile()
    if update.validate_on_submit():
        old_img = ''
        old_bg_img = ''

        if update.profile.data:
            profile_img = save_profile_picture(update.profile.data)
            old_img = current_user.image_file
            current_user.image_file = profile_img

        if update.profile_bg.data:
            profile_bg_img = save_bg_picture(update.profile_bg.data)
            old_bg_img = current_user.bg_file
            current_user.bg_file = profile_bg_img

        if update.bday.data:
            current_user.bday = update.bday.data
            
        if not usernameValidator(update.username.data):
            flash('Username contains prohibited characters')
            return redirect(url_for('account'))
        
        current_user.username = update.username.data
        current_user.email = update.email.data
        current_user.bio = update.bio.data
        current_user.notes = update.notes.data
        db.session.commit()

        delete_old_images(old_img, old_bg_img)

        flash('Your account has been updated!','success')
        return redirect(url_for('account'))

    elif request.method == 'GET':

        update.username.data = current_user.username
        update.email.data = current_user.email
        update.bio.data = current_user.bio

    return render_template('updateProfile.html',change_form=update)

@app.route('/deactivate_confirmation')
@login_required
def deactivate_confirm():
    return render_template('deact_conf.html')

@app.route('/account_deleted/<int:account_id>',methods=['POST'])
@login_required
def delete_account(account_id):

    if account_id != current_user.id:
        return abort(403)

    all_retweets = Retweet.query.filter_by(user_id=current_user.id)
    for i in all_retweets:
        db.session.delete(i)
    all_post = Post.query.filter_by(user_id=current_user.id)
    for i in all_post:
        db.session.delete(i)

    del_acc = User_mgmt.query.filter_by(id=account_id).first()
    db.session.delete(del_acc)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user_tweet = createTweet()
    if user_tweet.validate_on_submit():

        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))

        if user_tweet.tweet_img.data:
            tweet_img = save_tweet_picture(user_tweet.tweet_img.data)
            post = Post(tweet=user_tweet.tweet.data, stamp=currentTime, author=current_user, post_img=tweet_img)
        else:
            post = Post(tweet=user_tweet.tweet.data, stamp=currentTime, author=current_user)

        db.session.add(post)
        db.session.commit()

        to_timeline = Timeline(post_id=post.id)
        db.session.add(to_timeline)
        db.session.commit()

        flash('The Tweet was added to your timeline!','success')
        return redirect(url_for('dashboard'))

    page = request.args.get('page',1,type=int)
    timeline = Timeline.query\
        .order_by(desc(Timeline.id))\
        .paginate(page=page,per_page=5)
    return render_template('dashboard.html',name = current_user.username,tweet = user_tweet, timeline=timeline)

@app.route('/view_profile/<int:account_id>',methods=['GET','POST'])
@login_required
def viewProfile(account_id):
    if account_id == current_user.id:
        return redirect(url_for('account'))

    get_user = User_mgmt.query.filter_by(id=account_id).first()
    profile_pic = url_for('static',filename='Images/Users/profile_pics/' + get_user.image_file)
    bg_pic = url_for('static',filename='Images/Users/bg_pics/' + get_user.bg_file)

    page = request.args.get('page',1,type=int)
    all_posts = Post.query\
        .filter_by(user_id=get_user.id)\
        .order_by(desc(Post.id))\
        .paginate(page=page,per_page=5)
    retweets = Retweet.query\
        .filter_by(user_id=get_user.id)\
        .order_by(desc(Retweet.id))

    return render_template('view_profile.html',profile=profile_pic,background=bg_pic,timeline=all_posts,user=get_user,retweets=retweets)

@app.route('/bookmark/<int:post_id>',methods=['GET','POST'])
def save_post(post_id):
    saved_post = Bookmark(post_id=post_id,user_id=current_user.id)
    db.session.add(saved_post)
    db.session.commit()
    flash('Saved tweet to bookmark!','success')
    return redirect(url_for('dashboard'))

@app.route('/unsaved_posts/<int:post_id>',methods=['GET','POST'])
def unsave_post(post_id):
    removed_post = Bookmark.query\
        .filter_by(post_id=post_id)\
        .first()
    db.session.delete(removed_post)
    db.session.commit()
    flash('Post removed from bookmark!','success')
    return redirect(url_for('dashboard'))

@app.route('/saved_posts/')
def bookmarks():
    posts = Bookmark.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Bookmark.id))
    empty = False
    if posts == None:
        empty = True
    return render_template('bookmarks.html',posts=posts, empty=empty)

@app.route('/notes')
def notes():
    update = UpdateProfile()
    return render_template('notes.html', update=update)

@app.route('/retweet/<int:post_id>',methods=['GET','POST'])
@login_required
def retweet(post_id):

    post = Post.query.get_or_404(post_id)
    new_tweet = createTweet()

    if new_tweet.validate_on_submit():

        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))

        retweet = Retweet(tweet_id=post.id,user_id=current_user.id,retweet_stamp=currentTime,retweet_text=new_tweet.tweet.data)
        db.session.add(retweet)
        db.session.commit()

        to_timeline = Timeline(retweet_id=retweet.id)
        db.session.add(to_timeline)
        db.session.commit()

        msg = 'You retweeted @'+post.author.username+"'s tweet!"
        flash(msg,'success')
        return redirect(url_for('dashboard'))

    return render_template('retweet.html',post=post, tweet=new_tweet)

@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    return render_template('delete_post.html',post=post)

@app.route('/delete_retweet/<int:post_id>')
@login_required
def delete_retweet(post_id):
    retweet = Retweet.query.get_or_404(post_id)
    if retweet.retwitter != current_user:
        abort(403)
    return render_template('delete_post.html',retweet=retweet)

@app.route('/delete_post/<int:post_id>',methods=['POST'])
@login_required
def delete_tweet(post_id):

    post_bk = Bookmark.query.filter_by(post_id=post_id)
    if post_bk != None:
        for i in post_bk:
            db.session.delete(i)
            db.session.commit()

    remove_from_timeline = Timeline.query.filter_by(post_id=post_id).first()
    if remove_from_timeline.from_post.author != current_user:
        abort(403)
    db.session.delete(remove_from_timeline)
    db.session.commit()

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash('Your tweet was deleted!','success')
    return redirect(url_for('dashboard'))

@app.route('/delete_retweeted_post/<int:post_id>',methods=['POST'])
@login_required
def delete_retweeted_tweet(post_id):

    post_bk = Bookmark.query.filter_by(post_id=post_id)
    if post_bk != None:
        for i in post_bk:
            db.session.delete(i)
            db.session.commit()

    remove_from_timeline = Timeline.query.filter_by(retweet_id=post_id).first()
    if remove_from_timeline.from_retweet.retwitter != current_user:
        abort(403)
    db.session.delete(remove_from_timeline)
    db.session.commit()

    retweet = Retweet.query.get_or_404(post_id)
    if retweet.retwitter != current_user:
        abort(403)
    db.session.delete(retweet)
    db.session.commit()

    flash('Your tweet was deleted!','success')
    return redirect(url_for('dashboard'))

@app.route('/api/info', methods=['GET'])
@login_required
def test():
    
    count_posts = Post.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Post.id)).count()
        
    count_retweets = Retweet.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Retweet.id)).count()
    
    
    
    answer = {
        "username" : current_user.username,
        "email" : current_user.email,
        "posts_count" : count_posts,
        "retweets_count" : count_retweets
        }
    
    return render_template_string(dumps(answer))

@app.route('/oauth')
def yalogin():
    return redirect(OAUTHURL + f"authorize?response_type=code&client_id={CLIENT_ID}")

@app.route('/oauth/yandex/info')
def oauthInfo():
    if request.args.get('token', False):
        access_token = request.args.get('token')
        result = post("https://login.yandex.ru/info", headers={"Authorization": f"bearer {access_token}"}).json()
        username = result['real_name']
        email = result['default_email']
        user = User_mgmt.query.filter_by(email = email).first()
        print(f"User {user}")
        if not user:
            x = datetime.datetime.now()
            creation = str(x.strftime("%B")) +" "+ str(x.strftime("%Y"))
            user = User_mgmt(username=username, email=email, password=secrets.token_hex(16), date=creation)
            db.session.add(user)
            db.session.commit()
        login_user(user, True)  
        return redirect(url_for('dashboard'))       
    else:
        return render_template_string("Error!")

@app.route('/oauth/yandex/callback/')
def oauthLogin():
    if request.args.get('code', False):
        data = {
            'grant_type': 'authorization_code',
            'code': request.args.get('code'),
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        data = urlencode(data)
        token = post(OAUTHURL + "token", data).json()
        try:
            access_token = token['access_token']
        except:
            return render_template_string("Error!")
        return redirect(f"/oauth/yandex/info?token={access_token}")
    return render_template_string("Error!")
