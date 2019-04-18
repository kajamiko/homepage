# -*- coding: utf-8 -*-
import os
from socket import gethostname
from flask import Flask, render_template, url_for, request, redirect, flash, session
from forms import ContactForm
from flask_sqlalchemy import SQLAlchemy
import datetime



app = Flask(__name__)
app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=str(os.environ.get('SQLALCHEMY_DATABASE_URI')),
    SQLALCHEMY_POOL_RECYCLE=299,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY=str(os.environ.get('SECRET_KEY')),

    ))

db=SQLAlchemy(app)

class Blogpost(db.Model):

    __tablename__ = "blogposts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    date_created = db.Column(db.DateTime,  default=datetime.datetime.utcnow)




@app.route('/')
def index():

    if session.get('lang') == 'pl':
        return render_template("index_pl.html")
    else:
        return render_template("index.html")
    
@app.route('/contact', methods=('GET', 'POST'))
def contact():
    form = ContactForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            # send_mail(request.form['subject'], "kajamiko.webdev@gmail.com", 'mail/message.html',
            #         name = request.form['name'],
            #         email = request.form['email'],
            #         message = request.form['message'])
            return redirect(url_for('success'))
    if session.get('lang') == 'pl':
        return render_template('contact_form_pl.html', form=form)
    else:
        return render_template('contact_form.html', form=form)
    
@app.route('/success')
def success():
    if session.get('lang') == 'pl':
        return render_template("success_pl.html")
    else:
        return render_template('success.html')
    

@app.route('/offer')
def offer():
    if session.get('lang') == 'pl':
        return render_template("offer_pl.html")
    else:
        return render_template('offer.html')
        
@app.route('/portfolio')
def portfolio():
    if session.get('lang') == 'pl':
        return render_template("portfolio_pl.html")
    else:
        return render_template('portfolio.html')
    
@app.route('/<lang>')
def set_lang(lang='eng'):
    session['lang'] = lang
    return redirect(redirect_url())

@app.route('/blog')
def blog_home():
    #return posts
    raw_posts = Blogpost.query.order_by(Blogpost.date_created.desc()).all()
    # for each post, split content in paragraphs
    for raw_post in raw_posts:
        raw_post.content = raw_post.content.split("<p>")
    return render_template('blog_home.html', posts=raw_posts)

def redirect_url(default='index'):
    return request.referrer

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

