from base_handler import BaseHandler
import handlers_root

handlers_root.links['homeworks'].append(dict(href = "/unit3/blog", caption = "Unit3: Blog"))
handlers_root.links['homeworks'].append(dict(href = "/unit3/blog/newpost", caption = "Unit3: Blog NewPost"))

class BlogPage(BaseHandler):
    def get(self):
        self.render('u3-blog-blog.html')


class NewPost(BaseHandler):
    def get(self):
        self.render('u3-blog-newpost.html')
