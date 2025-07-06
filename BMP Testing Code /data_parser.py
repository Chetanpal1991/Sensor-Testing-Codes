import time
import os
import csv

def get_last_time_stamping():
    try:
        with open("data.csv", mode='r') as f:
            reader = csv.reader(f)
            headers = next(reader, None)
            last_row = None
            for row in reader:
                if row:
                    last_row = row
            if last_row:
                return last_row[1]
    except FileNotFoundError:
        return None
    return None

def stream_data(file_path="Testing_file/data_packets.txt"):
    with open(file_path, "r") as file:
        for line in file:
            line = line.strip().strip("<>")
            values = line.split(",")

            if len(values) < 3:
                continue  

            altitude, pressure, temp = values
            yield {
                "altitude": altitude,
                "pressure": pressure,
                "temp": temp,
            }

            time.sleep(1)

if __name__ == "__main__":
    for data in stream_data():
        print(f"Altitude: {data['altitude']} m")
        print(f"Pressure: {data['pressure']} Pa")
        print(f"Temperature: {data['temp']} °C")
        print("-" * 40)
