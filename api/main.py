from pydantic import BaseModel
from parser import parse_fix_message
from summary import generate_message_summary
from validator import validate_fix_message
from log_parser import parse_fix_log
from fastapi import HTTPException

from fastapi import FastAPI

app = FastAPI()

class FixMessageRequest(BaseModel):
    fix_message:str

class FixLogRequest(BaseModel):
    log_text: str

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
    
@app.post("/decode-log")
def decode_fix_log(request: FixLogRequest):
    
    if not request.log_text.strip():
        raise HTTPException(
            status_code=400,
            detail="log_text cannot be empty"
        )
    
    parsed_messages = parse_fix_log(request.log_text)
    
    result = []
    
    for message in parsed_messages:
        summary = generate_message_summary(message)
        validation = validate_fix_message(message, "")
        
        result.append({
            "parsed": message,
            "summary": summary,
            "validation": validation
        })
    
    return {
        "count": len(result),
        "messages": result
        }