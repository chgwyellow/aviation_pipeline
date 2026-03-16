import json
import os
import random
from datetime import datetime, timedelta

import src.generator.aircraft as aircraft
from src.generator.config import AIRCRAFT_PERFORMANCE, ROUTES, SIMULATION_SETTINGS
from src.utils.db_utils import fetch_fleet

fleet = []

# Define the start and end time
current_sim_time = datetime(2026, 3, 9, 0, 0)
end_sim_time = current_sim_time + timedelta(days=7)
# step length
time_step = timedelta(minutes=SIMULATION_SETTINGS["time_step_minutes"])

os.makedirs("data/land_logs", exist_ok=True)

if __name__ == "__main__":
    # Retrieve the fleet data
    for plane in fetch_fleet():
        p_obj = aircraft.Aircraft(
            tail_number=plane["tail_number"],
            aircraft_type=plane["aircraft_type"],
            initial_location="TPE",
            initial_fuel=AIRCRAFT_PERFORMANCE[plane["aircraft_type"]]["max_fuel"],
        )
        p_obj.last_landed_at = current_sim_time - timedelta(hours=2)

        if plane["status"] == "Maintenance":
            p_obj.is_flying = False
            p_obj.current_location = "HANGAR"

        fleet.append(p_obj)
    print(len(fleet))

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

                    timestamp = current_sim_time.strftime("%Y%m%d_%H%M%S")
                    file_path = f"data/land_logs/{plane.tail_number}_{timestamp}.json"

                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(event_data, f, indent=4)
            # is_flying == False
            else:
                ground_time = (
                    current_sim_time - plane.last_landed_at
                ).total_seconds() / 60
                if ground_time > 60:
                    possible_routes = [
                        r for r in ROUTES if r[0] == plane.current_location
                    ]
                    selected_route = random.choice(possible_routes)

                    speed = AIRCRAFT_PERFORMANCE[plane.aircraft_type]["avg_speed_kmh"]
                    duration = selected_route[2] / speed
                    plane.take_off(selected_route[1], current_sim_time, duration)
                else:
                    plane.refuel()

            current_sim_time += timedelta(
                minutes=SIMULATION_SETTINGS["time_step_minutes"]
            )
