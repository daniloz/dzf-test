from base_handler import BaseHandler

links = dict(homeworks = [])

class RootPage(BaseHandler):
    def get(self):
        self.render('index.html', **links)
