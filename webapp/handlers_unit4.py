import re
import logging
from base_handler import BaseHandler
import handlers_root
from google.appengine.ext import db

handlers_root.links['homeworks'].append(dict(href = "/unit4/signup", caption = "Unit4: SignUp"))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def validate_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validate_email(email):
    return not email or EMAIL_RE.match(email)

def user_key(name = 'default'):
    return db.Key.from_path('users', name)

class User(db.Model):
    username = db.StringProperty(required = True)
    email = db.StringProperty(required = False)
    password = db.StringProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)


class SignUpPage(BaseHandler):
    def get(self):
        self.render('u4-signup-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username,
                      email = email)

        has_error = False

        if not validate_username(username):
            params['username_error'] = "That's not a valid username."
            has_error = True

        if not validate_password(password):
            params['password_error'] = "That wasn't a valid password."
            has_error = True
        elif password != verify:
            params['verify_error'] = "Your passwords didn't match."
            has_error = True

        if not validate_email(email):
            params['email_error'] = "That's not a valid email."
            has_error = True

        query = "SELECT * FROM User WHERE username = '%s'" % username
        existingUser = db.GqlQuery(query)
        if existingUser:
            params['username_error'] = "The user already exists."
            has_error = True

        if has_error:
            self.render('u4-signup-form.html', **params)
        else:
            # TODO: Do password hashing+salting
            # insert new user into DB
            newUser = User(parent = user_key(),
                           username = username, email = email, password = password)
            newUser.put()

            # set a cookie on the user's side
            # TODO: Do cookie hashing
            cookie_value = str(username)
            logging.info("COOKIE: user=%s" % cookie_value)
            self.response.headers.add_header("Set-Cookie", "user=%s; Path=/" % cookie_value)
            self.redirect('/unit4/signup/welcome')

class SignUpWelcomePage(BaseHandler):
    def get(self):
        username = self.request.cookies.get('user')
        if validate_username(username):
            self.render('u4-signup-welcome.html', username = username)
        else:
            self.redirect('/unit4/signup')

