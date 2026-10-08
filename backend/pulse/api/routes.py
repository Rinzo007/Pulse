from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/routes", tags=["routes"])


@router.get("")
def list_routes() -> list[dict]:
    # Temporary in-memory endpoint; PostgreSQL/PostGIS repository comes next.
    return []
