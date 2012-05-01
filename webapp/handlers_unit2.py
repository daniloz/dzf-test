import re
from base_handler import BaseHandler
import handlers_root

handlers_root.links['homeworks'].append(dict(href = "/unit2/rot13", caption = "Unit2: ROT13"))
handlers_root.links['homeworks'].append(dict(href = "/unit2/signup", caption = "Unit2: SignUp"))

class Rot13Page(BaseHandler):
    def get(self):
        self.render('u2-rot13-form.html')
        
    def post(self):
        user_text = self.request.get('text')
        text_rot13ed = user_text.encode('rot13')
        params = dict(usertext = text_rot13ed);
        self.render('u2-rot13-form.html', **params)


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
        self.render('u2-signup-form.html')
    
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

        if has_error:
            self.render('u2-signup-form.html', **params)
        else:            
            self.redirect('/unit2/signup/welcome?username=' + username)

class SignUpWelcomePage(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if validate_username(username):
            self.render('u2-signup-welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

