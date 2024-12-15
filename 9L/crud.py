from sqlalchemy.orm import Session
from models import User, Post

def create_user(db: Session, username: str, email: str, password: str):
    user = User(username=username, email=email, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db: Session):
    return db.query(User).all()

def create_post(db: Session, title: str, content: str, user_id: int):
    post = Post(title=title, content=content, user_id=user_id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

def get_posts(db: Session):
    return db.query(Post).all()

def get_posts_by_user(db: Session, user_id: int):
    return db.query(Post).filter(Post.user_id == user_id).all()

def update_user_email(db: Session, user_id: int, email: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = email
        db.commit()
    return user

def update_post_content(db: Session, post_id: int, content: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = content
        db.commit()
    return post

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
    return post

def delete_user_and_posts(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.query(Post).filter(Post.user_id == user_id).delete()
        db.delete(user)
        db.commit()
    return user
