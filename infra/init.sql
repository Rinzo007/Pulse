CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS transport_zones (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    population INTEGER NOT NULL DEFAULT 0,
    geom geometry(MultiPolygon, 4326) NOT NULL
);

CREATE TABLE IF NOT EXISTS road_nodes (
    id TEXT PRIMARY KEY,
    geom geometry(Point, 4326) NOT NULL
);

CREATE TABLE IF NOT EXISTS road_edges (
    id TEXT PRIMARY KEY,
    from_node_id TEXT NOT NULL REFERENCES road_nodes(id),
    to_node_id TEXT NOT NULL REFERENCES road_nodes(id),
    mode_mask TEXT[] NOT NULL DEFAULT '{}',
    lanes INTEGER NOT NULL DEFAULT 1,
    speed_kmh NUMERIC NOT NULL DEFAULT 30,
    length_m NUMERIC NOT NULL DEFAULT 0,
    geom geometry(LineString, 4326) NOT NULL
);

CREATE TABLE IF NOT EXISTS stops (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    modes TEXT[] NOT NULL DEFAULT '{}',
    wheelchair_accessible BOOLEAN NOT NULL DEFAULT TRUE,
    geom geometry(Point, 4326) NOT NULL
);

CREATE TABLE IF NOT EXISTS routes (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    mode TEXT NOT NULL,
    headway_seconds INTEGER NOT NULL DEFAULT 600,
    capacity INTEGER NOT NULL DEFAULT 80
);

CREATE INDEX IF NOT EXISTS idx_transport_zones_geom ON transport_zones USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_road_nodes_geom ON road_nodes USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_road_edges_geom ON road_edges USING GIST (geom);
CREATE INDEX IF NOT EXISTS idx_stops_geom ON stops USING GIST (geom);
