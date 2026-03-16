AIRCRAFT_PERFORMANCE = {
    "A350-900": {"max_fuel": 110000, "burn_rate": 5800, "avg_speed_kmh": 900},
    "A321neo": {"max_fuel": 23000, "burn_rate": 2200, "avg_speed_kmh": 830},
    "B787-10": {"max_fuel": 101000, "burn_rate": 5400, "avg_speed_kmh": 870},
}

SIMULATION_SETTINGS = {
    "min_ground_time_minutes": 60,
    "fuel_safety_margin": 5000,
    "time_step_minutes": 15,
}

ROUTES = [
    # (dep, arr, distance)
    ("TPE", "NRT", 2100),
    ("NRT", "TPE", 2100),
    ("TPE", "SIN", 3200),
    ("SIN", "TPE", 3200),
    ("SFO", "TPE", 10000),
]
