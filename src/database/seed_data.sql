/*
 * Database: aviation_pipeline
 * Description: Initial seed data for dimension tables (Virtual Fleet: SkyBridge Air)
 */
-- 1. Virtual manufacturer
INSERT INTO dim_manufacturers (manufacturer_name, country, contact_email)
VALUES (
        'Aerocraft Global',
        'USA',
        'mike111@aerocraft.com'
    ),
    (
        'Titan Engines',
        'Germany',
        'susan_young@titan.com'
    ),
    (
        'AvioSens Inc.',
        'France',
        'dino102030@aviosens.com'
    );
-- 2. Virtual airports
INSERT INTO dim_airports (iata_code, airport_name, city, timezone)
VALUES (
        'TPE',
        'Taiwan Taoyuan International Airport',
        'Taipei',
        'Asia/Taipei'
    ),
    (
        'NRT',
        'Narita International Airport',
        'Tokyo',
        'Asia/Tokyo'
    ),
    (
        'SIN',
        'Changi Airport',
        'Singapore',
        'Asia/Singapore'
    ),
    (
        'LHR',
        'London Heathrow Airport',
        'London',
        'Europe/London'
    ),
    (
        'SFO',
        'San Francisco International Airport',
        'San Francisco',
        'America/Los_Angeles'
    );
-- 3. Virtual fleet
INSERT INTO dim_aircraft_fleet (
        tail_number,
        aircraft_type,
        total_flight_hours,
        status
    )
VALUES ('SB-101', 'A350-900', 120.5, 'Active'),
    ('SB-102', 'A350-900', 45.0, 'Active'),
    ('SB-201', 'A321neo', 300.2, 'Active'),
    ('SB-202', 'A321neo', 10.0, 'Active'),
    ('SB-801', 'B787-10', 0.0, 'Maintenance');
-- 4. Original components
INSERT INTO dim_components (
        part_number,
        component_name,
        aircraft_id,
        manufacturer_id,
        install_date,
        expected_lifespan_hours
    )
VALUES (
        'ENG-T1000-01',
        'Titan-X High Thrust Engine',
        1,
        2,
        '2026-01-01',
        5000
    ),
    (
        'SENS-AV-99',
        'Avio-Pitot Static Tube',
        1,
        3,
        '2026-02-15',
        1000
    );