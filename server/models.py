from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('phone_number')
    def validate_phone_number(self, key, number):
        just_number = [n for n in number if n.isdigit()]

        if not len(just_number) == 10:
            raise ValueError("Phone number must be 10 digits")

        return number
    
    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name must be defined for author")
        
        for auth in Author.query.all():
            if auth.name == name:
                raise ValueError("Same name cannot be used.")
            
        return name
    
    
    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('category')
    def validates_post_category(self, key, post_category):
        if not (post_category == "Fiction" or post_category == "Non-Fiction"):
            raise ValueError("Category must be either Fiction or Non-Fiction")
        return post_category
    
    @validates('content')
    def validates_post_content_char(self, key, post_content):
        if not len(post_content) >= 250:
            raise ValueError('Post content must be greater than or equal to 250 characters.')
        return post_content
    
    @validates('summary')
    def validates_post_summary(self, key, post_summary):
        if not len(post_summary) <= 250:
            raise ValueError("Post summary must be less than 250 characters.")
        return post_summary
    
    @validates('title')
    def validates_post_title(self, key, post_title):
        words_to_use_bank = ["Won't Believe", "Secret", "Top", "Guess"]
        count = 0
        for words in words_to_use_bank:
            if words in post_title:
                count += 1
        
        if count == 0:
            raise ValueError("Post title must have click bait-inducing words.")
            
        return post_title


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
