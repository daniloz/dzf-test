#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import re
import webapp2
import logging
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)		

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))



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

class RootPage(BaseHandler):
    def get(self):        
        self.render('index.html', **links)

links = dict(homeworks = [])
links['homeworks'].append(dict(href="/unit2/rot13",caption="Unit2: ROT13"))
links['homeworks'].append(dict(href="/unit2/signup",caption="Unit2: SignUp"))
		
app = webapp2.WSGIApplication([('/',RootPage),
                               ('/unit2/rot13',Rot13Page),
                               ('/unit2/signup',SignUpPage),
                               #('/unit2/rot13',Rot13Page(None,None, dict(href="/unit2/rot13",caption="Unit2: ROT13"))),
                               #('/unit2/signup',SignUpPage(None,None, dict(href="/unit2/signup",caption="Unit2: SignUp"))),
                               ('/unit2/signup/welcome',SignUpWelcomePage)],
                              debug=True)
