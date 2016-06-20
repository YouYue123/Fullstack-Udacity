from google.appengine.ext import db
#### like_post_relation stuff
def like_post_relation_key(name='default'):
    return db.Key.from_path('likes',name)

## LikePostRelation Model
class LikePostRelation(db.Model):
    like_by = db.IntegerProperty(required=True)
    post_id = db.IntegerProperty(required=True)

    @classmethod
    def create_like_post_relation(cls,like_by,post_id):
    	return LikePostRelation(parent=like_post_relation_key(),like_by = int(like_by),post_id=int(post_id))

    @classmethod
    def check_like_status(cls,user_id,post_id):
        user_id = int(user_id)
        post_id = int(post_id)
        q = db.GqlQuery("SELECT * FROM LikePostRelation WHERE like_by = :user_id and post_id = :post_id",user_id = user_id,post_id = post_id)
        return q.get()