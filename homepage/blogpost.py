from extensions import db 

class Blogpost(db.Model):

    __tablename__ = "Blogposts"

    id = db.Column(db.Integer, primary_key=True)
    
    content = db.Column(db.String(4096))