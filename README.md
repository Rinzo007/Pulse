# Pulse

Pulse is a transport planning and simulation platform for cities and suburbs with public transport as the primary design objective.

## First target

Build a reproducible vertical slice:

**city/network → demand → transit network → passenger trips → SUMO → KPIs → scenario comparison**

SUMO is the traffic microsimulator, not the whole application.

## Architecture

- **Backend:** Python, FastAPI, SQLAlchemy, GeoPandas/Shapely, NetworkX
- **Database:** PostgreSQL + PostGIS
- **Simulation:** SUMO via TraCI/libsumo
- **Frontend:** React + TypeScript + MapLibre
- **Analytics:** Pandas/NumPy
- **Tests:** pytest

## Repository layout

```
backend/      API and domain logic
frontend/     interactive planning UI
infra/        Docker and local infrastructure
data/         generated/downloaded data (not committed)
docs/         architecture and domain documentation
tests/        integration/e2e tests
```

## Development principle

Real data, synthetic data and calibrated model outputs must always be distinguishable. Heuristics must never be presented as proven optima.

## MVP sequence

1. Create a synthetic city.
2. Persist road/transit network in PostGIS.
3. Expose the network through FastAPI.
4. Render/edit routes on the map.
5. Generate a simple OD demand matrix.
6. Build a passenger route chain including walking and transfers.
7. Export a SUMO scenario.
8. Run SUMO and collect travel time, delay, waiting and transit KPIs.
9. Compare baseline vs. one transit-priority scenario.
