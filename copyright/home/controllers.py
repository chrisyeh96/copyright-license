from flask import Blueprint, request, render_template, jsonify, redirect, url_for, session

from copyright.models import *
from copyright.home.forms import LoginForm, SignupForm, ContactForm, UpdateUserForm

from sqlalchemy import desc
from math import ceil

import sys

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

# to print debug statements to Heroku console:
# import sys
# print "statement"
# sys.stdout.flush()
# source: http://stackoverflow.com/questions/12504588/

homeRoutes = Blueprint('homeRoutes', __name__)
app = homeRoutes

images_per_page = 15

@homeRoutes.record
def record_params(setup_state):
  global app
  app = setup_state.app


@homeRoutes.route('/')
def index():
    return render_template('index.html')


@homeRoutes.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect(url_for('homeRoutes.profile'))

    login_form = LoginForm()

    # validate_on_submit() checks if it is POST request and if the form is valid
    if login_form.validate_on_submit():
        session['email'] = login_form.email.data
        return redirect(url_for('homeRoutes.profile'))
    else:
        return render_template('login.html', login_form=login_form)


@homeRoutes.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'email' in session:
        return redirect(url_for('homeRoutes.profile'))

    signup_form = SignupForm()

    # validate_on_submit() checks if it is POST request and if the form is valid
    if signup_form.validate_on_submit():
        newuser = User(signup_form.firstname.data, signup_form.lastname.data, signup_form.email.data, signup_form.password.data)
        db.session.add(newuser)
        db.session.commit()
        session['email'] = newuser.email

        try:
            fromaddr = "copyrightfeedback@gmail.com"
            toaddr = newuser.email
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Welcome to License Exchange"
            body = "Hello, %s %s! Welcome to License Exchange." % (newuser.firstname, newuser.lastname)
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(fromaddr, app.config['EMAIL_PASSWORD'])
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
        except:  
            print 'Something went wrong with sending the signup confirmation email...'
            print sys.exc_info()[0]
            sys.stdout.flush()

        return redirect(url_for('homeRoutes.profile'))
    else:
        return render_template('signup.html', signup_form=signup_form)


@homeRoutes.route('/logout')
def signout():
    if 'email' not in session:
        return redirect(url_for('homeRoutes.login'))

    session.pop('email', None)
    return redirect(url_for('homeRoutes.index'))


@homeRoutes.route('/profile')
def profile():
    if 'email' not in session:
        return redirect(url_for('homeRoutes.login'))

    update_user_form = UpdateUserForm()
 
    user = User.query.filter_by(email = session['email']).first()
    if user is None:
        return redirect(url_for('homeRoutes.login'))
    else:
        return render_template('profile.html', user=user, update_user_form=update_user_form, images=user.created_images)


@homeRoutes.route('/update_user', methods=['POST'])
def update_user():
    if 'email' not in session:
        return redirect(url_for('homeRoutes.login'))
    user = User.query.filter_by(email = session['email']).first()
    if user is None:
        return redirect(url_for('homeRoutes.login'))

    update_user_form = UpdateUserForm()
    if update_user_form.validate_on_submit():
        tempUser = User(update_user_form.firstname.data, update_user_form.lastname.data, update_user_form.email.data, update_user_form.password.data)
        user.pwdhash = tempUser.pwdhash
        user.plus_id = update_user_form.plus_id.data

        tempStripeID = update_user_form.stripe_id.data.strip()
        if tempStripeID != "":
            user.stripe_id = tempStripeID
            ## TODO: validate stripe ID

        db.session.commit()

        redirect(url_for('homeRoutes.profile'))
    else:
        return render_template('profile.html', user=user, update_user_form=update_user_form)


@homeRoutes.route('/search')
def search():
    searchText = '%' + request.args.get('searchText') + '%'
    category = request.args.get('category')

    # use ilike() to get case-insensitive search
    images = Image.query.filter(Image.keywords.ilike(searchText))

    if category and int(category) != -1:
        images = images.filter(Image.categories.any(id=int(category)))

    images = images.order_by(desc(2*Image.num_purchases + Image.num_clicks)) \
                   .all()
    pages = list(range(1, int(ceil(len(images) / float(images_per_page)) + 1)))
    return render_template('search.html', images=images[0:images_per_page], pages=pages)


@homeRoutes.route('/page')
def page():
    page_num = int(request.args.get('page'))
    images = Image.query.filter_by().all()
    result = []
    start = (page_num - 1) * images_per_page
    end = min(page_num * images_per_page, len(images))
    for i in range(start, end):
        result.append({
            'id' : images[i].id,
            'url': images[i].url_thumb,
        })
    return jsonify(result=result)


@homeRoutes.route('/about', methods=['GET'])
def about():
    contact_form = ContactForm()
    return render_template('about.html', contact_form=contact_form)


@homeRoutes.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    contact_form = ContactForm()

    # validate_on_submit() checks if it is POST request and if the form is valid
    if contact_form.validate_on_submit():
        newFeedback = Feedback(contact_form.name.data, contact_form.email.data, contact_form.message.data)
        db.session.add(newFeedback)
        db.session.commit()

        try:  
            msg = MIMEMultipart()
            fromaddr = "copyrightfeedback@gmail.com"
            toaddr = "chrisyeh@stanford.edu"
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Copyright License Website Feedback"
            body = "Name: %s\nEmail: %s\nMessage: %s" % (newFeedback.name, newFeedback.email, newFeedback.message)
            msg.attach(MIMEText(body, 'plain'))
            text = msg.as_string()

            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(fromaddr, app.config['EMAIL_PASSWORD'])
            server.sendmail(fromaddr, toaddr, text)
            server.quit()

            print "Submitted Feedback!"
            print body
            sys.stdout.flush()

        except:  
            print 'Something went wrong with sending the feedback...'
            print sys.exc_info()[0]
            sys.stdout.flush()

        return redirect(url_for('homeRoutes.about'))
    else:
        print "Error in feedback"
        sys.stdout.flush()
        return render_template('about.html', contact_form=contact_form)


@homeRoutes.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404