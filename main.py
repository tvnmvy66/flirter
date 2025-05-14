from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = OpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class msg(BaseModel):
    user : str
    message : str

class ArrayData(BaseModel):
    relation : str
    messages:List[msg]

@app.get("/ping")
async def pong():
    return {"pong"}

@app.post("/api/suggest")
async def receive_array(payload: ArrayData):
    print("Received relation:", payload.relation)
    for message in payload.messages:
        print(f"User: {message.user} | Message: {message.message}")

    system_prompt = f'''
    You are an helpful ai assistant in suggesting reply based on relation and previous message provided to you.
    You will suggest reply message thinking you are person named Tanmay.The message will short and accent will be based on tanmay's
    previous provided messages. Always see the realtion first and then decide the way to answer it.

    relation : {payload.relation}

    previous message : {payload.messages}
    '''

    completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "Hello!"}
        ]
    )
    return {"suggestion" : completion.choices[0].message.content}

