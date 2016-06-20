import re
import datetime
import hmac
import webapp2
# import self implemented modules
from user import User
from post import Post
from comment import Comment
from like_post_relation import LikePostRelation
from global_func import render_str

secret = 'YouYue'

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
        post = Post.by_id(post_id)
        comments = Comment.comments_by_post_id(post.key().id())
        if not post:
            self.redirect('/blog')
            return
        if self.user:
            self.render("permalink.html", post = post, username = self.user.name,comments=comments,user_id=self.user.key().id())
        else:
            self.render("permalink.html", post = post,comments=comments)
    
    def post(self,post_id):

        if not self.user:
            self.redirect('/blog/%s' % post_id)

        subject = self.request.get('subject')
        content = self.request.get('content')
        user_id = self.user.key().id()
        last_modified = datetime.datetime.now()
        post = Post.by_id(post_id)
        if post and post.created_by == user_id:
           Post.update(post_id,subject,content,last_modified)
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
            p = Post.create(subject,content,user_id)
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
            post = Post.by_id(post_id)
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
        post = Post.by_id(post_id)
        
        if post and post.created_by == self.user.key().id():
            Post.delete(post_id)

        self.redirect('/blog')

## Like Post Handler
class LikePost(BlogHandler):
    def get(self):
        post_id = self.request.get('post_id')
        user_id = self.user.key().id()

        if user_id and post_id and not LikePostRelation.check_like_status(user_id,post_id):
            Post.updateLike(post_id)
            like_post_relation = LikePostRelation.create_like_post_relation(user_id,post_id)
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
        Comment.create(created_by=created_by,create_time=create_time,
                       content=content,post_id=post_id)
        self.redirect('/blog/%s' % post_id);


class CommentUpdate(BlogHandler):
    def post(self):
        if not self.user:
            self.redirect('/blog')
        comment_id = self.request.get('comment_id')
        content = self.request.get('comment-content')
        comment = Comment.by_id(comment_id)
        if comment.created_by == self.user.key().id():
            Comment.update(comment_id,content)
            self.redirect('/blog/%s' % comment.post_id)
        else:
            self.redirect('/blog')

class CommentDelete(BlogHandler):
    def get(self):
        if not self.user:
            self.redirect('/blog')
        comment_id = self.request.get('comment_id')
        comment = Comment.by_id(comment_id)
        if comment.created_by == self.user.key().id():
            post_id = comment.post_id
            Comment.delete(comment_id)
            self.redirect('/blog/%s' % post_id)
        else:
            self.redirect('/blog')
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
                               ('/blog/comment/delete',CommentDelete),
                               ('/blog/comment/update',CommentUpdate),
                               ('/login', Login),
                               ('/logout', Logout)
                               ],
                              debug=True)
