import src.generator.aircraft as aircraft
from src.generator.config import SIMULATION_SETTINGS
from src.utils.db_utils import fetch_fleet

fleet = []

if __name__ == "__main__":
    for plane in fetch_fleet():
        p_obj = aircraft.Aircraft(
            tail_number=plane["tail_number"],
            aircraft_type=plane["aircraft_type"],
            initial_location="TPE",
            initial_fuel=10000,
        )

        if plane["status"] == "Maintenance":
            p_obj.is_flying = False
            p_obj.current_location = "HANGAR"

        fleet.append(p_obj)
    print(len(fleet))
