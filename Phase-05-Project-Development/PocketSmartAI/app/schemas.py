from typing import Literal
from pydantic import BaseModel,Field,field_validator
class RegisterRequest(BaseModel):
    email:str; password:str=Field(min_length=8,max_length=128)
    @field_validator("email")
    @classmethod
    def email_ok(cls,v):
        v=v.strip().lower()
        if "@" not in v: raise ValueError("Enter a valid email address.")
        return v
class LoginRequest(BaseModel): email:str; password:str
class HomeRequest(BaseModel): budget:float=Field(gt=0,le=10000000); rooms:list[str]=Field(min_length=1); style:str="Modern"; items:list[str]=[]
class PartyRequest(BaseModel): budget:float=Field(gt=0,le=10000000); guest_count:int=Field(gt=0,le=10000); event_type:str=Field(min_length=1,max_length=100); venue_details:str=""; city:str="India"
class JewelryRequest(BaseModel): budget:float=Field(gt=0,le=10000000); occasion:str=Field(min_length=1,max_length=100); style:str="Elegant"; outfit_description:str=""
class RecommendationItem(BaseModel): name:str; category:str; platform:str; price:float=Field(ge=0); quantity:int=Field(default=1,ge=1); reason:str; url:str
class RecommendationResult(BaseModel):
    planner_type:Literal["home","party","jewelry"]; title:str; summary:str; budget:float; estimated_total:float=Field(ge=0); budget_remaining:float; allocation:dict[str,float]={}; items:list[RecommendationItem]=[]; notes:list[str]=[]; source_mode:Literal["live","gemini","fallback"]
