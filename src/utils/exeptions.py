from http.client import responses
from starlette.exceptions import HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

class CustomApiException(HTTPException):
    """
    Кастомное исключение для вывода ошибок при работе с API
    """
    pass

async def custom_api_exception_handler(request: Request, exc: HTTPException):
    """
    Обработчик ошибок для исключения при работе с API
    """
    return JSONResponse(
        {
            "result": False,
            "error_type": f"{exc.status_code}",
            "error_message": str(exc.detail),
        },
        status_code=exc.status_code,
    )
