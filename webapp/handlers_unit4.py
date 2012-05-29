import re
import logging
from base_handler import BaseHandler, User
import handlers_root

handlers_root.links['homeworks'].append(dict(href = "/unit4/signup", caption = "Unit4: SignUp"))
handlers_root.links['homeworks'].append(dict(href = "/unit4/login", caption = "Unit4: Login"))
handlers_root.links['homeworks'].append(dict(href = "/unit4/logout", caption = "Unit4: Logout"))

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def validate_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def validate_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def validate_email(email):
    return not email or EMAIL_RE.match(email)


class SignUpPage(BaseHandler):
    def get(self):
        self.render('u4-signup-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        logging.info('username = %s, password = %s, verify = %s, email = %s' % (username, password, verify, email))

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

        u = User.by_name(username)

        logging.info("Got user: %s" % u)
        if u:
            params['username_error'] = "The user already exists."
            has_error = True

        if has_error:
            self.render('u4-signup-form.html', **params)
        else:
            # TODO: Do password hashing+salting
            # insert new user into DB
            u = User.register(username, password, email)
            u.put()

            self.login(u)
            self.redirect('/unit4/welcome')

class LogoutPage(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/unit4/signup')

class LoginPage(BaseHandler):
    def get(self):
        self.render('u4-login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        logging.info('username = %s, password = %s' % (username, password))

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/unit4/welcome')
        else:
            msg = 'Invalid login'
            self.render('u4-login-form.html', login_error = msg)

class SignUpWelcomePage(BaseHandler):
    def get(self):
        if self.user:
            self.render('u4-signup-welcome.html', username = self.user.username)
        else:
            self.redirect('/unit4/signup')

