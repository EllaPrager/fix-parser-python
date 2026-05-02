"""
FastAPI application for the Tagora FIX Decoder API.

This module exposes API endpoints for:
- Health check
- Decoding a single FIX message
- Decoding a FIX log containing multiple messages
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from parser import parse_fix_message
from summary import generate_message_summary
from validator import validate_fix_message
from log_parser import parse_fix_log


app = FastAPI(
    title="Tagora FIX API",
    description="API for decoding, summarizing, and validating FIX messages.",
    version="1.0.0"
)


class FixMessageRequest(BaseModel):
    """
    Request model for decoding a single FIX message.
    """

    fix_message: str


class FixLogRequest(BaseModel):
    """
    Request model for decoding a FIX log containing multiple FIX messages.
    """

    log_text: str


@app.get("/")
def root():
    """
    Health check endpoint.

    Returns a simple response to confirm that the API is running.
    """

    return {"message": "Tagora API is running"}


@app.post("/decode")
def decode_fix_message(request: FixMessageRequest):
    """
    Decode, summarize, and validate a single FIX message.
    """

    if not request.fix_message.strip():
        raise HTTPException(
            status_code=400,
            detail="fix_message cannot be empty"
        )

    fix_message = request.fix_message

    parsed = parse_fix_message(fix_message)
    summary = generate_message_summary(parsed)
    validation = validate_fix_message(parsed, fix_message)

    return {
        "parsed": parsed,
        "summary": summary,
        "validation": validation
    }


@app.post("/decode-log")
def decode_fix_log(request: FixLogRequest):
    """
    Decode, summarize, and validate multiple FIX messages from a log.
    """

    if not request.log_text.strip():
        raise HTTPException(
            status_code=400,
            detail="log_text cannot be empty"
        )

    parsed_messages = parse_fix_log(request.log_text)

    results = []

    for message in parsed_messages:
        summary = generate_message_summary(message)
        validation = validate_fix_message(message, "")

        results.append({
            "parsed": message,
            "summary": summary,
            "validation": validation
        })

    return {
        "count": len(results),
        "messages": results
    }