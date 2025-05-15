import socket
import threading
import json
import os
import requests

class FlightServer:
    def __init__(self, host="127.0.0.1", port=5050):
        # Server settings
        self.host = host
        self.port = port
        self.api_key = "15317cf0631f9d6a63f7064a2156cc1c"
        self.url = "http://api.aviationstack.com/v1/flights"
        self.flights = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def fetch_data(self):
        # Fetch flight data from API if SB5.json does not exist
        if not os.path.exists("SB5.json"):
            code = input("SB5.json not found. Enter ICAO airport code (example: OBBI): ")
            params = {
                "access_key": self.api_key,
                "arr_icao": code.strip().upper(),
                "limit": 100
            }
            print("Fetching data from API...")
            response = requests.get(self.url, params=params)
            if response.status_code == 200:
                with open("SB5.json", "w") as f:
                    json.dump(response.json(), f, indent=4)
                print("SB5.json created successfully.\n")
            else:
                print("Failed to fetch data. Exiting.")
                exit()

    def load_flights(self):
        # Load flight data from SB5.json into memory
        with open("SB5.json", "r") as f:
            data = json.load(f)
            self.flights = data.get("data", [])

    def start_server(self):
        # Start the server and begin accepting client connections
        self.fetch_data()
        self.load_flights()
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print("Server is running and waiting for connections...")

        while True:
            client_socket, address = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client, args=(client_socket, address))
            thread.start()

    def handle_client(self, client_socket, address):
        # Handle communication with a single client
        name = client_socket.recv(1024).decode()
        print("Client connected:", name, "| Address:", address)

        while True:
            try:
                request = client_socket.recv(1024).decode().strip()
                if not request or request.upper() == "QUIT":
                    print("Client disconnected:", name)
                    break

                print("Request from", name + ":", request)
                response = self.process_request(request)
                client_socket.send(response.encode())
            except:
                break

        client_socket.close()

    def process_request(self, request):
        # Process the client's request and return the appropriate flight data
        req = request.upper()

        if req == "ARRIVED":
            result = ""
            for f in self.flights:
                if f.get("flight_status") == "landed":
                    result += "Flight: " + str(f["flight"]["iata"]) + "\n"
                    result += "From: " + str(f["departure"]["airport"]) + "\n"
                    result += "Arrival: " + str(f["arrival"]["actual"]) + "\n"
                    result += "Terminal: " + str(f["arrival"]["terminal"]) + "\n"
                    result += "Gate: " + str(f["arrival"]["gate"]) + "\n"
                    result += "-----\n"
            return result if result else "No arrived flights found."

        elif req == "DELAYED":
            result = ""
            for f in self.flights:
                delay = f["arrival"].get("delay")
                if delay and delay > 0:
                    result += "Flight: " + str(f["flight"]["iata"]) + "\n"
                    result += "From: " + str(f["departure"]["airport"]) + "\n"
                    result += "Scheduled: " + str(f["departure"]["scheduled"]) + "\n"
                    result += "ETA: " + str(f["arrival"]["estimated"]) + "\n"
                    result += "Delay: " + str(delay) + " min\n"
                    result += "Terminal: " + str(f["arrival"]["terminal"]) + "\n"
                    result += "Gate: " + str(f["arrival"]["gate"]) + "\n"
                    result += "-----\n"
            return result if result else "No delayed flights found."

        elif req.startswith("DETAILS:"):
            code = req.split(":")[1].strip().upper()
            for f in self.flights:
                if f["flight"]["iata"] == code:
                    result = "Flight: " + str(f["flight"]["iata"]) + "\n"
                    result += "From: " + str(f["departure"]["airport"]) + "\n"
                    result += "Gate: " + str(f["departure"]["gate"]) + "\n"
                    result += "Terminal: " + str(f["departure"]["terminal"]) + "\n"
                    result += "To: " + str(f["arrival"]["airport"]) + "\n"
                    result += "Arrival Gate: " + str(f["arrival"]["gate"]) + "\n"
                    result += "Arrival Terminal: " + str(f["arrival"]["terminal"]) + "\n"
                    result += "Status: " + str(f["flight_status"]) + "\n"
                    result += "Scheduled Departure: " + str(f["departure"]["scheduled"]) + "\n"
                    result += "Scheduled Arrival: " + str(f["arrival"]["scheduled"]) + "\n"
                    return result
            return "Flight not found."

        else:
            return "Invalid request."

# ========= Entry Point =========
if __name__ == "__main__":
    server = FlightServer()
    server.start_server()
