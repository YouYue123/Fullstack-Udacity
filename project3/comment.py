from google.appengine.ext import db
from user import User
from global_func import render_str
#### comment stuff
def comment_key(name='default'):
    return db.Key.from_path('comments',name)
## Comment Model
class Comment(db.Model):
    created_by = db.IntegerProperty(required=True)
    create_time = db.DateTimeProperty(auto_now_add=True)
    content = db.StringProperty(required=True)
    post_id = db.IntegerProperty(required=True)

    @classmethod
    def create(cls,created_by,create_time,content,post_id):
        comment = Comment(parent=comment_key(),created_by=created_by,create_time=create_time,
                       content=content,post_id=int(post_id))
        comment.put()
        comment.put()
        return comment

    @classmethod
    def comments_by_post_id(cls,post_id):
        post_id = int(post_id)
        return Comment.all().filter('post_id =',post_id).order('-create_time')
    @classmethod
    def by_id(cls,comment_id):
        return Comment.get_by_id(int(comment_id),parent=comment_key())
    @classmethod
    def update(cls,comment_id,content):
        comment = Comment.by_id(comment_id)
        comment.content = content
        comment.put()
        comment.put()
        return comment

    @classmethod
    def delete(cls,comment_id):
        comment = Comment.by_id(comment_id)
        db.delete(comment)
        db.delete(comment)
        return


    def render(self,user_id):
        author_name = User.by_id(int(self.created_by)).name
        if self.created_by == user_id: 
            is_author = True
        else:
            is_author = False
        return render_str("comment.html",comment=self,author_name = author_name,is_author=is_author)
