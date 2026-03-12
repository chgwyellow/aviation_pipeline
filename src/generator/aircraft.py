import random

from src.generator.config import AIRCRAFT_PERFORMANCE


class Aircraft:
    def __init__(self, tail_number, aircraft_type, initial_location, initial_fuel):
        self.tail_number = tail_number
        self.aircraft_type = aircraft_type
        self.current_location = initial_location
        self.total_hours = 0.0
        self.is_flying = False
        self.last_landed_at = None
        self.current_dep_time = None
        self.current_fuel = initial_fuel
        self.last_origin = initial_location

        specs = AIRCRAFT_PERFORMANCE.get(aircraft_type, {})
        self.max_fuel_capacity = specs.get("max_fuel", 50000)
        self.fuel_burn_rate = specs.get("burn_rate", 3000)

    def take_off(self, destination, dep_time):
        if destination == self.current_location:
            print(f"Error: {self.tail_number} already at {destination}")
            return False

        if self.is_flying:
            print(f"Error: {self.tail_number} is already in the air")
            return False

        if self.current_fuel < 5000:
            print(f"Error: {self.tail_number} low fuel ({self.current_fuel:.1f}kg)")
            return False

        self.last_origin = self.current_location  # keep the departure airport
        print(
            f"{self.tail_number} gets ready to take off from {self.last_origin} to {destination}"
        )
        self.current_dep_time = dep_time
        self.is_flying = True
        self.current_location = "IN_FLIGHT"
        return True

    def land(self, destination, arr_time):
        # The subtract of datetime gets timedelta, using total_seconds to convert
        duration = (arr_time - self.current_dep_time).total_seconds() / 3600
        burn_fuel = self._consume_fuel(duration)

        # Prepare the data for ingestion layer
        event_data = {
            "tail_number": self.tail_number,
            "dep_airport": self.last_origin,
            "arr_airport": destination,
            "actual_departure": self.current_dep_time.isoformat(),
            "actual_arrival": arr_time.isoformat(),
            "fuel_burn_kg": round(burn_fuel, 2),
            "telemetry_data": self.get_telemetry_snapshot(),
        }
        self.current_location = destination
        self.total_hours += duration
        self.is_flying = False
        self.last_landed_at = arr_time

        print(f"{self.tail_number} landed. Burned: {burn_fuel:.1f}kg")
        return event_data

    def _consume_fuel(self, duration):
        """
        Calculate burned  fuel
        """
        burn = duration * self.fuel_burn_rate
        self.current_fuel -= burn
        if self.current_fuel < 0:
            self.current_fuel = 0
        return burn

    def get_telemetry_snapshot(self):
        """
        Create a json telemetry data
        """
        return {
            "engine_temp": random.randint(600, 850),
            "oil_pressure": random.uniform(40, 60),
            "vibration_level": (
                "Normal" if self.total_hours < 1000 else "Check Required"
            ),
        }

    def refuel(self, amount=None):
        # fuel to full
        if amount is None:
            fuel_to_add = self.max_fuel_capacity - self.current_fuel
        else:
            fuel_to_add = amount

        if self.current_fuel + fuel_to_add > self.max_fuel_capacity:
            fuel_to_add = self.max_fuel_capacity - self.current_fuel

        self.current_fuel += fuel_to_add
        print(f"{self.tail_number} refueled: +{fuel_to_add:.1f}kg")
