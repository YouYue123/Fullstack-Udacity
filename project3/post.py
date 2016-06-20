from google.appengine.ext import db
from user import User
from global_func import render_str
from like_post_relation import LikePostRelation
##### post stuff
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

    #create function
    @classmethod
    def create(cls,subject,content,created_by,like=0):
        post = Post(parent = blog_key(), subject = subject, content = content,created_by = created_by,like=like)
        post.put()
        return post

    #read function
    @classmethod
    def by_id(cls,post_id):
        return Post.get_by_id(int(post_id),parent=blog_key())

    #update function
    @classmethod
    def update(cls,post_id,subject,content,last_modified):
        post = Post.by_id(post_id)
        post.subject = subject
        post.content = content
        post.last_modified = last_modified
        post.put()
        return
    @classmethod
    def updateLike(cls,post_id):
        post = Post.by_id(post_id)
        post.like += 1
        post.put()
        return

    #delete function
    @classmethod
    def delete(cls,post_id):
        post = Post.by_id(int(post_id))
        db.delete(post)
        db.delete(post)
        return

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
