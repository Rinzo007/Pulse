from fastapi import FastAPI

app = FastAPI(
    title="Pulse API",
    version="0.1.0",
    description="Transport planning and simulation API",
)


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
