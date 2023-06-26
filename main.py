from fastapi import FastAPI, Request, Depends, Form, status
from fastapi.templating import Jinja2Templates
import models
from database import engine, sessionlocal
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse

 
models.Base.metadata.create_all(bind=engine)
 
templates = Jinja2Templates(directory="templates")
 
app = FastAPI()



def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()
 

 
@app.get("/")
async def home(request: Request, db: Session = Depends(get_db)):
    users = db.query(models.User).order_by(models.User.id.desc())
    return templates.TemplateResponse("index.html", {"request": request, "users": users})

@app.post("/add_user")
async def add_user(request: Request,
                   name: str = Form(...),
                   email: str = Form(...),
                   phone: str = Form(...),
                   db: Session = Depends(get_db)
                   ):
    user = models.User(name=name, email=email,phone=phone)
    db.add(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)

@app.get("/{user_id}")
async def get_user_by_id(request: Request,user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return templates.TemplateResponse("index.html", {"request": request, "user": user})

@app.post("/update/{user_id}")
async def update_user(request: Request,
                      user_id: int,
                      name: str = Form(...),
                      email: str = Form(...),
                      phone: str = Form(...),
                      db: Session = Depends(get_db)
                      ):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    user.name = name
    user.email = email
    user.phone = phone
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"),status_code=status.HTTP_303_SEE_OTHER)

@app.get("/delete/{user_id}")
async def delete(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(user)
    db.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)

