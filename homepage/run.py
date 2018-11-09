import os
from socket import gethostname
from flask_mail import Mail, Message
from flask import Flask, render_template, url_for, request, redirect, flash
from forms import ContactForm



def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


app = Flask(__name__)
app.config.update(dict(
    SECRET_KEY='development key',
    MAIL_SERVER='smtp.mail.yahoo.com',
    MAIL_PORT = 465,
    MAIL_DEFAULT_SENDER = str(os.environ.get('MAIL_USERNAME')),
    MAIL_USERNAME = str(os.environ.get('MAIL_USERNAME')),
    MAIL_PASSWORD = str(os.environ.get('MAIL_PASSWORD')),
    MAIL_USE_TLS = False,
    MAIL_USE_SSL = True
))

mail = Mail(app)

def send_mail(subject, recipient, template, **kwargs):
    msg = Message(subject, sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[recipient])
    msg.html = render_template(template, **kwargs)
    try:
        mail.send(msg)
        return 'Your message has been sent'
    except Exception as e:
        print(e)
        return "Something went wrong x.x!"
    return None

@app.route('/')
def index():
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
    return render_template('contact_form.html', form=form)
    
@app.route('/success')
def success():
    
    return render_template('success.html')
    

@app.route('/offer')
def offer():
    
    return render_template('offer.html')

if __name__ == '__main__':
    if 'liveconsole' not in gethostname():
        app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True)