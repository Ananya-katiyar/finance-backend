from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes import auth, records, dashboard
from app.database import create_db_and_tables

app = FastAPI()

# clean validation error responses
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " → ".join(str(x) for x in error["loc"]),
            "message": error["msg"]
        })
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation failed", "errors": errors}
    )

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth.router)
app.include_router(records.router)
app.include_router(dashboard.router)