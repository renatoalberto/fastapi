from fastapi import FastAPI

from core.configs import settings
from api.v1.api import api_router

app = FastAPI(title='Curso API - Segurança')
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level='info', reload=True)


"""
Login de acesso:
"email": "renato.alb@gmail.com","id": 3,
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjc0NTY0NTg5LCJpYXQiOjE2NzM5NTk3ODksInN1YiI6IjMifQ.WfBkQYd2ernXOSHQ3gPTF8gwAiKRH-T2t2rFvBlIFwg",
  "toke_type": "bearer"
}

"email": "theo.alb@gmail.com","id": 1,
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjc0NTY0OTU4LCJpYXQiOjE2NzM5NjAxNTgsInN1YiI6IjEifQ.jNYVhQdL3TfMURsXkxfLg0CtKiroKsaJru3MGttdz3s",
  "toke_type": "bearer"
}
"""    
