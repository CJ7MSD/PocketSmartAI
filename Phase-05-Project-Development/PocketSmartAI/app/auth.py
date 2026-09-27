from datetime import datetime,timedelta,timezone
import jwt
from pwdlib import PasswordHash
from fastapi import Depends,HTTPException,Request,status
from sqlalchemy.orm import Session
from app.config import get_settings
from app.database import get_db
from app.models import User
ph=PasswordHash.recommended(); s=get_settings(); COOKIE="pocketsmart_access_token"
def hash_password(p): return ph.hash(p)
def verify_password(p,h): return ph.verify(p,h)
def token(uid): return jwt.encode({"sub":str(uid),"exp":datetime.now(timezone.utc)+timedelta(minutes=s.access_token_expire_minutes)},s.secret_key,algorithm="HS256")
def current_user(request:Request,db:Session=Depends(get_db)):
    t=request.cookies.get(COOKIE)
    if not t: raise HTTPException(401,"Login required.")
    try: uid=int(jwt.decode(t,s.secret_key,algorithms=["HS256"])["sub"])
    except Exception: raise HTTPException(401,"Invalid session.")
    u=db.get(User,uid)
    if not u: raise HTTPException(401,"User not found.")
    return u
