from fastapi import FastAPI

from pulse.api.routes import router as routes_router

app = FastAPI(
    title="Pulse API",
    version="0.1.0",
    description="Transport planning and simulation API",
)

app.include_router(routes_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/v1")
def api_info() -> dict[str, str]:
    return {
        "name": "Pulse",
        "version": "0.1.0",
        "focus": "public-transport-first transport planning",
    }
