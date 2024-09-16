from fastapi.responses import JSONResponse


def successResponse(status_code: int, message: str, data: any):
    return JSONResponse(status_code= status_code, content={
            "success": True,
            "message": message,
            "data": data
        })

def failedResponse(status_code: int, message: str):
    return JSONResponse(status_code= status_code, content={
            "success": False,
            "message": message
        })