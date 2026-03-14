import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()


def get_db_connection():
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")

    try:
        conn = psycopg.connect(
            conninfo=f"host={host} "
            f"port={port} "
            f"dbname={db} "
            f"user={user} "
            f"password={password}",
            row_factory=dict_row,
        )
        return conn
    except Exception as e:
        print(f"Connection failed: {e}")
        return None


def fetch_fleet():
    query = """
        SELECT tail_number, aircraft_type, total_flight_hours, status
        FROM dim_aircraft_fleet;
    """

    conn = get_db_connection()
    if conn is None:
        return []

    with conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchall()


if __name__ == "__main__":
    fleet = fetch_fleet()
    for plane in fleet:
        print(f"Find plane: {plane['tail_number']} ({plane['aircraft_type']})")
