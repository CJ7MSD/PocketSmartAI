from fastapi import APIRouter,Depends,HTTPException,Response,Request
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterRequest,LoginRequest
from app.auth import hash_password,verify_password,token,current_user,COOKIE
r=APIRouter(prefix="/api/auth",tags=["auth"])
@r.post("/register")
def register(p:RegisterRequest,res:Response,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==p.email)): raise HTTPException(409,"An account with this email already exists.")
    u=User(email=p.email,password_hash=hash_password(p.password)); db.add(u); db.commit(); db.refresh(u); return {"created":True,"user":{"id":u.id,"email":u.email}}
@r.post("/login")
def login(p:LoginRequest,res:Response,db:Session=Depends(get_db)):
    u=db.scalar(select(User).where(User.email==p.email.strip().lower()))
    if not u or not verify_password(p.password,u.password_hash): raise HTTPException(401,"Invalid email or password.")
    res.set_cookie(COOKIE,token(u.id),httponly=True,samesite="lax",max_age=86400); return {"user":{"id":u.id,"email":u.email}}
@r.post("/logout")
def logout(res:Response): res.delete_cookie(COOKIE); return {"message":"Logged out."}
@r.get("/session-info")
def info(req:Request,db:Session=Depends(get_db)):
    try: u=current_user(req,db); return {"authenticated":True,"user":{"id":u.id,"email":u.email}}
    except HTTPException: return {"authenticated":False,"user":None}
@r.get("/session-data")
def data(u=Depends(current_user)): return {"user_id":u.id,"email":u.email}
