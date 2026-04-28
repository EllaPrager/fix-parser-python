from pydantic import BaseModel
from parser import parse_fix_message
from summary import generate_message_summary
from validator import validate_fix_message

from fastapi import FastAPI

app = FastAPI()

class FixMessageRequest(BaseModel):
    fix_message:str

@app.get("/")
def root():
    return {"message": "Tagora API is running"}

@app.post("/decode")
def decode_fix_message(request: FixMessageRequest):
    
    parsed = parse_fix_message(request.fix_message)
    summary = generate_message_summary(parsed)
    validation = validate_fix_message(parsed, request.fix_message)
    
    return {
        "parsed": parsed,
        "summary": summary,
        "validation": validation
    }
    