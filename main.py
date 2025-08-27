from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from enum import Enum

from pydantic_settings import BaseSettings

from fastapi.middleware.cors import CORSMiddleware

class Body(BaseModel):
    message: str 
    
class CategoryEnum(str, Enum):
   bug = "bug"
   billing = "billing" 
   feature = "feature"
   other = "other"

class OpenAIResponse(BaseModel):
    category: CategoryEnum
    explanation: str
    
class Settings(BaseSettings):
    openai_api_key: str
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
app = FastAPI()
origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
        allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.post("/triage")
def read_root(body: Body):

    client = OpenAI(api_key=settings.openai_api_key)

    response = client.responses.parse(
      model="gpt-4.1",
      input=body.message,
      text_format=OpenAIResponse
    )

    return response.output_parsed

