from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


from application.api.schemas import ErrorDescriptionSchema, ErrorSchema
from application.exceptions import ApplicationException
from application.services.keycloak import ForbiddenException, UnauthorizedException


async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content=ErrorSchema(
            detail=ErrorDescriptionSchema(error=exc.message)
        ).model_dump(),
    )


async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content=ErrorSchema(
            detail=ErrorDescriptionSchema(error=exc.message)
        ).model_dump(),
    )


async def application_exception_handler(request: Request, exc: ApplicationException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorSchema(
            detail=ErrorDescriptionSchema(error=exc.message)
        ).model_dump(),
    )


async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=ErrorSchema(detail=ErrorDescriptionSchema(error=str(exc))).model_dump(),
    )
