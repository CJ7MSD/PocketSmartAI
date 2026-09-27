import os
os.environ['DATABASE_URL']='sqlite:///./test_pocketsmart.db';os.environ['SECRET_KEY']='test-secret';os.environ['GEMINI_API_KEY']=''
from fastapi.testclient import TestClient
from app.main import app
client=TestClient(app)
def test_health(): assert client.get('/health').json()['status']=='ok'
def test_flow():
    assert client.post('/api/auth/register',json={'email':'tester@example.com','password':'strongpass123'}).status_code==200
    r=client.post('/api/planners/home',json={'budget':30000,'rooms':['Living Room'],'style':'Modern','items':['lights']}); assert r.status_code==200; assert r.json()['result']['source_mode']=='fallback'
    assert client.get('/api/history').status_code==200
