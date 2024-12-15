from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
# http://127.0.0.1:8000/docs#/
from crud import (
    create_user,
    get_users,
    create_post,
    get_posts,
    get_posts_by_user,
    update_user_email,
    update_post_content,
    delete_post,
    delete_user_and_posts,
)
init_db()

app = FastAPI()
templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@app.get("/users/new", response_class=HTMLResponse)
def create_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request})

@app.post("/users/")
def add_user(username: str = Form(...), email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    return create_user(db, username, email, password)

@app.get("/posts/new", response_class=HTMLResponse)
def create_post_form(request: Request):
    return templates.TemplateResponse("post_form.html", {"request": request})

@app.post("/posts/")
def add_post(title: str = Form(...), content: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    return create_post(db, title, content, user_id)

@app.get("/users/", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    users = get_users(db)
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

@app.get("/posts/", response_class=HTMLResponse)
def list_posts(request: Request, db: Session = Depends(get_db)):
    posts = get_posts(db)
    return templates.TemplateResponse("post_list.html", {"request": request, "posts": posts})