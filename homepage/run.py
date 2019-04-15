# -*- coding: utf-8 -*-
import os
from socket import gethostname
from flask_mail import Mail, Message
from flask import Flask, render_template, url_for, request, redirect, flash, session
from forms import ContactForm
from extensions import db
from blogpost import Blogpost



def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def create_app():
    app = Flask(__name__)
    app.config.update(dict(
    SQLALCHEMY_DATABASE_URI=str(os.environ.get('SQLALCHEMY_DATABASE_URI')),
    SQLALCHEMY_POOL_RECYCLE=299,
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SECRET_KEY='development key',
    MAIL_SERVER='smtp.mail.yahoo.com',
    MAIL_PORT = 465,
    MAIL_DEFAULT_SENDER = str(os.environ.get('MAIL_USERNAME')),
    MAIL_USERNAME = str(os.environ.get('MAIL_USERNAME')),
    MAIL_PASSWORD = str(os.environ.get('MAIL_PASSWORD')),
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True
    ))
    register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
# app = Flask(__name__)
# app.config.update(dict(
#     SQLALCHEMY_DATABASE_URI=secret.SQLALCHEMY_DATABASE_URI,
#     SQLALCHEMY_POOL_RECYCLE=299,
#     SQLALCHEMY_TRACK_MODIFICATIONS=False,
#     SECRET_KEY='development key',
#     MAIL_SERVER='smtp.mail.yahoo.com',
#     MAIL_PORT = 465,
#     MAIL_DEFAULT_SENDER = str(os.environ.get('MAIL_USERNAME')),
#     MAIL_USERNAME = str(os.environ.get('MAIL_USERNAME')),
#     MAIL_PASSWORD = str(os.environ.get('MAIL_PASSWORD')),
#     MAIL_USE_TLS = False,
#     MAIL_USE_SSL = True
# ))
# db=SQLAlchemy(app)

app = create_app()
mail = Mail(app)


def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    try:
        mail.send(msg)
        if session.get('lang') == 'pl':
            return 'Wiadomość została wysłana.'
        else:
            return 'Your message has been sent'
    except Exception as e:
        print(e)
        return "Something went wrong x.x!"
    return None


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
            send_mail(request.form['subject'], "kajamiko.webdev@gmail.com", 'mail/message.html',
                    name = request.form['name'],
                    email = request.form['email'],
                    message = request.form['message'])
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

    return render_template('blog_home.html', posts=Blogpost.query.all())

def redirect_url(default='index'):
    return request.referrer

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)

