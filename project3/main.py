import os
import re
import time
import random
import hashlib
import hmac
import datetime
from string import letters
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

secret = 'YouYue'

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def make_secure_val(val):
    return '%s|%s' % (val, hmac.new(secret, val).hexdigest())

def check_secure_val(secure_val):
    val = secure_val.split('|')[0]
    if secure_val == make_secure_val(val):
        return val
## Basic BlogHandler
class BlogHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_val(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

def render_post(response, post):
    response.out.write('<b>' + post.subject + '</b><br>')
    response.out.write(post.content)

##### user stuff
def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (salt, h)

def valid_pw(name, password, h):
    salt = h.split(',')[0]
    return h == make_pw_hash(name, password, salt)

def users_key(group = 'default'):
    return db.Key.from_path('users', group)
 
class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    email = db.StringProperty()

    @classmethod
    def by_id(cls, uid):
        return User.get_by_id(uid, parent = users_key())

    @classmethod
    def by_name(cls, name):
        return User.all().filter('name =', name).get()


    @classmethod
    def register(cls, name, pw, email = None):
        pw_hash = make_pw_hash(name, pw)
        return User(parent = users_key(),
                    name = name,
                    pw_hash = pw_hash,
                    email = email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u


##### blog stuff

def blog_key(name = 'default'):
    return db.Key.from_path('blogs', name)
## Post Model
class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    created_by = db.IntegerProperty(required = True)
    like = db.IntegerProperty(required=True)
    last_modified = db.DateTimeProperty(auto_now = True)

    @classmethod
    def by_id(cls,post_id):
        return Post.get_by_id(post_id,parent=blog_key())

    def render(self,username):
        self._render_text = self.content.replace('\n', '<br>')
        user = User.by_id(int(self.created_by))
        author_name =  user.name
        like_status = ""
        if LikePostRelation.check_like_status(user.key().id(),self.key().id()):
            like_status = "disabled"

        return render_str("post.html", post = self,author_name=author_name,username = username,like_status=like_status)


    def render_preview(self):
        user = User.by_id(int(self.created_by))
        author_name =  user.name
        return render_str("post-preview.html", post = self,author_name= author_name)

#### comment stuff
def comment_key(name='default'):
    return db.Key.from_path('comments',name)
## Comment Model
class Comment(db.Model):
    created_by = db.IntegerProperty(required=True)
    create_time = db.DateTimeProperty(auto_now_add=True)
    content = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)
    
    def render(self):
        author_name = User.by_id(int(self.created_by)).name
        return render_str("comment.html",comment=self,author_name = author_name)

    @classmethod
    def comments_by_post_id(cls,post_id):
        post_id = int(post_id)
        return Comment.all().filter('post_id =',post_id).order('-create_time')

#### like_post_relation stuff
def like_post_relation_key(name='default'):
    return db.Key.from_path('likes',name)

## LikePostRelation Model
class LikePostRelation(db.Model):
    like_by = db.IntegerProperty(required=True)
    post_id = db.IntegerProperty(required=True)

    @classmethod
    def check_like_status(cls,user_id,post_id):
        user_id = int(user_id)
        post_id = int(post_id)
        q = db.GqlQuery("SELECT * FROM LikePostRelation WHERE like_by = :user_id and post_id = :post_id",user_id = user_id,post_id = post_id)
       
        return q.get()
            

## Blog Front Page Handler
class BlogFront(BlogHandler):
    def get(self):
        posts = Post.all().order('-created')
    	
        if self.user:
           self.render('front.html', posts = posts,username = self.user.name)
        else:
            self.render('front.html', posts = posts)

## Post Page Handler
class PostPage(BlogHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        comments = Comment.comments_by_post_id(post.key().id())
        if not post:
            self.redirect('/blog')
            return
        if self.user:
            self.render("permalink.html", post = post, username = self.user.name,comments=comments)
        else:
            self.render("permalink.html", post = post,comments=comments)
    
    def post(self,post_id):

        if not self.user:
            self.redirect('/blog/%s' % post_id)

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = self.user.key().id()
        last_modified = datetime.datetime.now()
        post = Post.by_id(int(post_id))
        if post and post.created_by == user_id:
           post.subject = subject
           post.content = content
           post.last_modified = last_modified
           post.put()
        self.redirect('/blog/%s' % post_id)
    
## New Post Handler
class NewPost(BlogHandler):
    def get(self):
        if self.user:
            username = self.user.name
            self.render("newpost.html",username=username)
        else:
            self.redirect("/login")

    def post(self):

        if not self.user:
            self.redirect('/blog')

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = int(self.read_secure_cookie('user_id'))

        if subject and content:
            p = Post(parent = blog_key(), subject = subject, content = content,created_by = user_id,like=0)
            p.put()
            self.redirect('/blog/%s' % str(p.key().id()))
        else:
            error = "subject and content, please!"
            self.render("newpost.html", subject=subject, content=content, error=error)

#### validation stuff
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

## Signup Handler
class Signup(BlogHandler):
    def get(self):
        self.render("register-form.html")

    def post(self):
        have_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.verify = self.request.get('verify')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_username(self.username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(self.password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif self.password != self.verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(self.email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('register-form.html', **params)
        else:
            self.done()

    def done(self, *a, **kw):
        raise NotImplementedError
## Register Handler
class Register(Signup):
    def done(self):
        u = User.by_name(self.username)
        if u:
            msg = 'That user already exists.'
            self.render('register-form.html', error_username = msg)
        else:
            u = User.register(self.username, self.password, self.email)
            u.put()

            self.login(u)
            self.redirect('/blog')

## Login Handler
class Login(BlogHandler):
    def get(self):
        self.render('login-form.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/blog')
        else:
            msg = 'Invalid login'
            self.render('login-form.html', error = msg)

## Logout Handler
class Logout(BlogHandler):
    def get(self):
        self.logout()
        self.redirect('/blog')

## Welcome Page Handler
class Welcome(BlogHandler):
    def get(self):
        self.redirect('/blog')

## Edit Post Handler
class EditPost(BlogHandler):
    def get(self):
        post_id = self.request.get('post_id')
        if post_id:
            post = Post.by_id(int(post_id))
            if self.user.key().id() == post.created_by:
                self.render("edit.html",username=self.user.name,post=post)
            else:
                self.redirect('/blog')
        else:
            self.redirect('/blog')

## Delete Post Handler
class DeletePost(BlogHandler):
    def get(self):
        post_id = self.request.get('post_id')
        if not self.user or not post_id:
            self.redirect('/blog/%s' % post_id)
        post = Post.by_id(int(post_id))
        if post and post.created_by == self.user.key().id():
            db.delete(post)
            db.delete(post)
        self.redirect('/blog')

## Like Post Handler
class LikePost(BlogHandler):
    def get(self):
        post_id = self.request.get('post_id')
        user_id = self.user.key().id()

        if user_id and post_id and not LikePostRelation.check_like_status(user_id,post_id):
            post = Post.by_id(int(post_id))
            post.like += 1
            post.put()

            like_post_relation = LikePostRelation(parent=like_post_relation_key(),like_by=int(user_id),post_id=int(post_id))
            like_post_relation.put()

        self.redirect('/blog/%s' % post_id)

## Comment Post Handler
class CommentPost(BlogHandler):
    def post(self):
        if not self.user:
            self.redirect('/blog')
        post_id = self.request.get('post_id')
        content = self.request.get('commment-content')
        created_by = self.user.key().id()
        create_time = datetime.datetime.now()
        comment = Comment(parent=comment_key(),created_by=created_by,create_time=create_time,
                          content=content,post_id=int(post_id))
        comment.put()
        comment.put()

        self.redirect('/blog/%s' % post_id);


## Router Configuration
app = webapp2.WSGIApplication([
                               ('/',Welcome),
                               ('/blog/?', BlogFront),
                               ('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/blog/edit',EditPost),
                               ('/blog/delete',DeletePost),
                               ('/blog/like',LikePost),
                               ('/register', Register),
                               ('/blog/comment',CommentPost),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
