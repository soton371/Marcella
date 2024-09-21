from fastapi.responses import JSONResponse
from typing import Any
from fastapi import status

def successResponse(status_code: int, message: str, data: Any | None = None, token: str | None = None):
    response_content = {
        "success": True,
        "message": message
    }
    
    if data is not None:
        response_content["data"] = data

    if token is not None:
        response_content["token"] = token

    return JSONResponse(status_code=status_code, content=response_content)

def failedResponse(status_code: int, message: str):
    return JSONResponse(status_code= status_code, content={
            "success": False,
            "message": message
        })

def unauthorizedResponse():
    return JSONResponse(status_code= status.HTTP_401_UNAUTHORIZED, content={
            "success": False,
            "message": 'Unauthorized request'
        })