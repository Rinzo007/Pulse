# Pulse architecture

## Core principle

Pulse owns planning, demand, passenger behavior, operations, scenario management and analytics. SUMO owns microscopic road traffic dynamics.

## Initial bounded contexts

### Geography
City boundary, suburbs, land use, population and transport zones.

### Network
Road graph, pedestrian graph, cycling graph and transit infrastructure.

### Public transport
Stops, platforms, routes, patterns, trips, timetables, vehicles and depots.

### Demand
Synthetic population, activity generation, OD matrices and mode choice.

### Passenger
Door-to-door journey chains, waiting, walking, transfers, crowding and denied boarding.

### Simulation
SUMO scenario generation, execution and result import.

### Evaluation
Travel time, reliability, waiting, transfers, passenger load, bunching, accessibility, emissions and cost.

### Scenarios
Immutable baseline + versioned interventions, reproducible parameters and comparable results.

## First database entities

`transport_zones`, `road_nodes`, `road_edges`, `stops`, `routes`, `route_patterns`, `trips`, `vehicles`, `depots`, `od_matrices`, `passenger_trips`, `scenarios`, `simulation_runs`, `kpis`.

## Next implementation step

Replace the temporary in-memory route API with SQLAlchemy/PostGIS repositories and a migration system, then add a synthetic city generator and a SUMO scenario exporter.
