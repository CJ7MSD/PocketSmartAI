import json
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.auth import current_user
from app.database import get_db
from app.models import Recommendation,User
r=APIRouter(prefix="/api",tags=["history"])
@r.get("/recommendations/{rid}")
def detail(rid:int,u:User=Depends(current_user),db:Session=Depends(get_db)):
    x=db.scalar(select(Recommendation).where(Recommendation.id==rid,Recommendation.user_id==u.id))
    if not x: raise HTTPException(404,"Recommendation not found.")
    return {"id":x.id,"planner_type":x.planner_type,"created_at":x.created_at.isoformat(),"result":json.loads(x.result_json)}
@r.get("/history")
def history(u:User=Depends(current_user),db:Session=Depends(get_db)):
    rows=db.scalars(select(Recommendation).where(Recommendation.user_id==u.id).order_by(Recommendation.created_at.desc()).limit(50)).all()
    return [{"id":x.id,"planner_type":x.planner_type,"created_at":x.created_at.isoformat(),"title":json.loads(x.result_json).get("title","Recommendation")} for x in rows]
@r.get("/history/{rid}")
def history_detail(rid:int,u=Depends(current_user),db:Session=Depends(get_db)): return detail(rid,u,db)
