import webapp2

import handlers_root
import handlers_unit2
import handlers_unit3
import handlers_unit4

SITE_URLS = [# Root Page
             webapp2.Route(r'/', handlers_root.RootPage),
             # Unit 2
             webapp2.Route(r'/unit2/rot13', handlers_unit2.Rot13Page),
             webapp2.Route(r'/unit2/signup', handlers_unit2.SignUpPage),
             webapp2.Route(r'/unit2/signup/welcome', handlers_unit2.SignUpWelcomePage),
             # Unit 3
             webapp2.Route(r'/unit3/blog', handlers_unit3.BlogPage),
             webapp2.Route(r'/unit3/blog/<post_id:\d{1,}>', handlers_unit3.BlogPost),
             webapp2.Route(r'/unit3/blog/newpost', handlers_unit3.NewPost),
             # Unit 4
             webapp2.Route(r'/unit4/signup', handlers_unit4.SignUpPage),
             webapp2.Route(r'/unit4/login', handlers_unit4.LoginPage),
             webapp2.Route(r'/unit4/logout', handlers_unit4.LogoutPage),
             webapp2.Route(r'/unit4/welcome', handlers_unit4.SignUpWelcomePage),
]
