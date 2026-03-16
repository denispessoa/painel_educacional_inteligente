
from contextlib import asynccontextmanager
from time import perf_counter
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db import Base, engine, get_db
from app.observability import APIMetrics, get_logger, log_event
from app.routers.bi_v1 import router as bi_v1_router
from app.routers.analytics import router as analytics_router
from app.routers.escolas import router as escolas_router
from app.routers.indicadores_trimestrais import router as indicadores_trimestrais_router
from app.routers.municipios import router as municipios_router
from app.routers.turmas import router as turmas_router


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Keeps local environments aligned without a migration tool in this MVP phase.
    Base.metadata.create_all(bind=engine)
    _app.state.metrics = APIMetrics()
    _app.state.logger = get_logger()
    log_event(_app.state.logger, "app_startup")
    yield
    log_event(_app.state.logger, "app_shutdown")


app = FastAPI(
    title="Plataforma Municipal de Inteligência Educacional",
    lifespan=lifespan,
)


@app.middleware("http")
async def observe_request(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid4())
    started = perf_counter()
    response = None
    error = None

    try:
        response = await call_next(request)
        return response
    except Exception as exc:  # pragma: no cover - exercised only on unexpected failures
        error = exc.__class__.__name__
        raise
    finally:
        elapsed_ms = (perf_counter() - started) * 1000
        status_code = response.status_code if response is not None else 500

        if request.url.path != "/metrics":
            request.app.state.metrics.record_request(status_code, elapsed_ms)

        log_event(
            request.app.state.logger,
            "http_request",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=status_code,
            duration_ms=round(elapsed_ms, 2),
            client_ip=request.client.host if request.client else None,
            error=error,
        )

        if response is not None:
            response.headers["x-request-id"] = request_id


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/dependencies")
def health_dependencies(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "degraded", "dependencies": {"database": "error"}},
        ) from exc

    return {"status": "ok", "dependencies": {"database": "ok"}}


@app.get("/metrics")
def metrics(request: Request):
    return request.app.state.metrics.snapshot()


app.include_router(municipios_router)
app.include_router(escolas_router)
app.include_router(turmas_router)
app.include_router(indicadores_trimestrais_router)
app.include_router(analytics_router)
app.include_router(bi_v1_router)
