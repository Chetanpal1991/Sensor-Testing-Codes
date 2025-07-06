import serial
from datetime import datetime
import threading

PORT = "/dev/tty.usbserial-0001"
BAUD_RATE = 9600
TEXT_FILE = "xbee_data.txt"

def read_and_log_serial():
    ser = serial.Serial(PORT, BAUD_RATE, timeout=1)

    with open(TEXT_FILE, mode='a') as file:
        print("📡 Logging data from XBee in background thread. Press Ctrl+C to stop.")
        
        try:
            while True:
                line = ser.readline().decode("utf-8").strip()
                if not line:
                    continue

                # Format: <130.10>,<101100>,<24.0>
                values = [v.strip("<>") for v in line.split(",")]

                if len(values) != 3:
                    continue

                altitude, pressure, temp = values
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                log_line = f"[{timestamp}] Altitude: {altitude}, Pressure: {pressure}, Temp: {temp}\n"
                file.write(log_line)
                file.flush()

                # Optional: also print it
                print(f"Logged: {log_line.strip()}")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            ser.close()

# Start in background thread
t = threading.Thread(target=read_and_log_serial, daemon=True)
t.start()

# Keep main thread alive
try:
    while True:
        pass  # Or do something else in main thread
except KeyboardInterrupt:
    print("\n🛑 Stopping logger.")
