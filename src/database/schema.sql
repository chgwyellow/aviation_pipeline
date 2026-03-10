/* * Database: aviation_pipeline
 * Schema: public
 */
-- 1. Airports dim table
CREATE TABLE IF NOT EXISTS dim_airports (
    airport_id SERIAL PRIMARY KEY,
    iata_code CHAR(3) UNIQUE NOT NULL,
    airport_name VARCHAR(100),
    city VARCHAR(100),
    timezone VARCHAR(50)
);
-- 2. Aircraft fleet dim table
CREATE TABLE IF NOT EXISTS dim_aircraft_fleet (
    aircraft_id SERIAL PRIMARY KEY,
    tail_number VARCHAR(10) UNIQUE NOT NULL,
    aircraft_type VARCHAR(20),
    total_flight_hours NUMERIC(10, 2) DEFAULT 0,
    last_maintenance_date DATE,
    status VARCHAR(20) DEFAULT 'Active'
);
-- 3. Manufacturer dim table
CREATE TABLE IF NOT EXISTS dim_manufacturers (
    manufacturer_id SERIAL PRIMARY KEY,
    manufacturer_name VARCHAR(200) UNIQUE NOT NULL,
    country VARCHAR(50),
    contact_email VARCHAR(100)
);
-- 4. Components dim table
CREATE TABLE IF NOT EXISTS dim_components (
    component_id SERIAL PRIMARY KEY,
    part_number VARCHAR(50) UNIQUE NOT NULL,
    component_name VARCHAR(100),
    aircraft_id INTEGER REFERENCES dim_aircraft_fleet(aircraft_id),
    manufacturer_id INTEGER REFERENCES dim_manufacturers(manufacturer_id),
    install_date DATE,
    expected_lifespan_hours INTEGER
);
-- 5. Flights fact table
CREATE TABLE IF NOT EXISTS fact_flight_events (
    event_id SERIAL PRIMARY KEY,
    tail_number VARCHAR(10) REFERENCES dim_aircraft_fleet(tail_number),
    flight_number VARCHAR(10),
    dep_airport_id INTEGER REFERENCES dim_airports(airport_id),
    arr_airport_id INTEGER REFERENCES dim_airports(airport_id),
    actual_departure TIMESTAMPTZ,
    actual_arrival TIMESTAMPTZ,
    fuel_burn_kg NUMERIC(10, 2),
    telemetry_data JSONB,
    CONSTRAINT check_flight_time CHECK (actual_arrival > actual_departure)
);