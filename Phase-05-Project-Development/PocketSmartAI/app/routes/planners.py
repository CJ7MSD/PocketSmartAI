import json
from fastapi import APIRouter,Depends,File,Form,HTTPException,UploadFile
from sqlalchemy.orm import Session
from app.auth import current_user
from app.database import get_db
from app.models import User,Recommendation
from app.schemas import HomeRequest,PartyRequest,JewelryRequest
from app.services.recommend import generate
r=APIRouter(prefix="/api/planners",tags=["planners"])
def save(db,u,kind,data,result):
    row=Recommendation(user_id=u.id,planner_type=kind,request_json=json.dumps(data),result_json=result.model_dump_json()); db.add(row); db.commit(); db.refresh(row); return row
@r.post("/home")
def home(p:HomeRequest,u:User=Depends(current_user),db:Session=Depends(get_db)):
    x=generate("home",p.model_dump()); row=save(db,u,"home",p.model_dump(),x); return {"id":row.id,"result":x.model_dump()}
@r.post("/party")
def party(p:PartyRequest,u:User=Depends(current_user),db:Session=Depends(get_db)):
    x=generate("party",p.model_dump()); row=save(db,u,"party",p.model_dump(),x); return {"id":row.id,"result":x.model_dump()}
@r.post("/jewelry")
async def jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("Elegant"),outfit_description:str=Form(""),outfit_image:UploadFile|None=File(None),u:User=Depends(current_user),db:Session=Depends(get_db)):
    p=JewelryRequest(budget=budget,occasion=occasion,style=style,outfit_description=outfit_description); data=p.model_dump(); raw=None; mime=None
    if outfit_image and outfit_image.filename:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Use JPG, PNG or WEBP.")
        raw=await outfit_image.read()
        if len(raw)>8*1024*1024: raise HTTPException(413,"Image must be 8 MB or smaller.")
        mime=outfit_image.content_type
    x=generate("jewelry",data,raw,mime); row=save(db,u,"jewelry",data,x); return {"id":row.id,"result":x.model_dump()}
