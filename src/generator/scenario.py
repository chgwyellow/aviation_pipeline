import src.generator.aircraft as aircraft
from src.generator.config import SIMULATION_SETTINGS, ROUTES
from src.utils.db_utils import fetch_fleet
from datetime import datetime, timedelta

fleet = []

if __name__ == "__main__":
    # Retrieve the fleet data
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

    # Define the start and end time
    current_sim_time = datetime(2026, 3, 9, 0, 0)
    end_sim_time = current_sim_time + timedelta(days=7)
    # step length
    time_step = timedelta(minutes=SIMULATION_SETTINGS["time_step_minutes"])

    # Main loop
    while current_sim_time < end_sim_time:
        for plane in fleet:
            # In maintenance, skipping
            if plane.current_location == "HANGAR":
                continue
            # is_flying == True
            if plane.is_flying:
                # check the current time passing ETA or not
                if current_sim_time >= plane.next_arrival_time:
                    event_data = plane.land(plane.next_destination, current_sim_time)
            # is_flying == False
            else:
                if (
                    timedelta(minutes=(plane.current_sim_time - plane.last_landed_at))
                    > 60
                ):
                    plane.take_off(plane.next_destination, current_sim_time, 2.5)
                else:
                    plane.refuel()
