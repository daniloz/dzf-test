from base_handler import BaseHandler, render_str
import handlers_root

from google.appengine.ext import db

handlers_root.links['homeworks'].append(dict(href = "/unit3/blog", caption = "Unit3: Blog"))

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    title = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.body.replace('\n', '<br>')
        return render_str('u3-post.html', post = self)


class BlogPage(BaseHandler):
    def get(self):
        #posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        posts = Post.all().order('-created')
        self.render('u3-blog-front.html', posts = posts)

class BlogPost(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent = blog_key())
        post = db.get(key)
        #post = Post.get_by_id(int(post_id))

        if not post:
            self.error(404)
            return

        self.render('u3-blog-post.html', post = post)

class NewPost(BaseHandler):
    def get(self):
        self.render('u3-blog-newpost.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            post = Post(parent = blog_key(), title = subject, body = content)
            post.put()

            post_key = post.key().id()

            self.redirect('/unit3/blog/%s' % str(post_key))
        else:
            error = 'subject and content, please!'
            self.render('u3-blog-newpost.html', title = subject, body = content, error = error)


