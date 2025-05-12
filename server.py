import socket
import threading
import json
import os
import requests

# Fetch data if SB5.json doesn't exist.
api_key = "15317cf0631f9d6a63f7064a2156cc1c"
url = "http://api.aviationstack.com/v1/flights"

if not os.path.exists("SB5.json"):
    icao_code = input("SB5.json not found. Enter ICAO airport code (example: OBBI): ")
    params = {
        "access_key": api_key,
        "arr_icao": icao_code.strip().upper(),
        "limit": 100
    }

    print("Fetching data from API...")
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        file = open("SB5.json", "w")
        json.dump(data, file, indent=4)
        file.close()
        print("SB5.json created successfully.\n")
    else:
        print("Failed to fetch data. Exiting.")
        exit()

# Load data.
file = open("SB5.json", "r")
data = json.load(file)
file.close()
flights = data.get("data", [])

# Setup TCP Server.
host = "127.0.0.1"
port = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

print("Server is running and waiting for connections...")

# Handle Clients.
def handle_client(client_socket, address):
    name = client_socket.recv(1024).decode()
    print("Client connected:", name, "| Address:", address)

    while True:
        try:
            request = client_socket.recv(1024).decode().strip()
            if not request or request.upper() == "QUIT":
                print("Client disconnected:", name)
                break

            print("Request from", name + ":", request)

            # --- ARRIVED flights ---
            if request.upper() == "ARRIVED":
                result = ""
                for flight in flights:
                    if flight.get("flight_status") == "landed":
                        result += "Flight: " + str(flight["flight"]["iata"]) + "\n"
                        result += "From: " + str(flight["departure"]["airport"]) + "\n"
                        result += "Arrival: " + str(flight["arrival"]["actual"]) + "\n"
                        result += "Terminal: " + str(flight["arrival"]["terminal"]) + "\n"
                        result += "Gate: " + str(flight["arrival"]["gate"]) + "\n"
                        result += "-----\n"
                if result == "":
                    result = "No arrived flights found."
                client_socket.send(result.encode())

            # --- DELAYED flights ---
            elif request.upper() == "DELAYED":
                result = ""
                for flight in flights:
                    delay = flight["arrival"].get("delay")
                    if delay and delay > 0:
                        result += "Flight: " + str(flight["flight"]["iata"]) + "\n"
                        result += "From: " + str(flight["departure"]["airport"]) + "\n"
                        result += "Scheduled: " + str(flight["departure"]["scheduled"]) + "\n"
                        result += "ETA: " + str(flight["arrival"]["estimated"]) + "\n"
                        result += "Delay: " + str(delay) + " min\n"
                        result += "Terminal: " + str(flight["arrival"]["terminal"]) + "\n"
                        result += "Gate: " + str(flight["arrival"]["gate"]) + "\n"
                        result += "-----\n"
                if result == "":
                    result = "No delayed flights found."
                client_socket.send(result.encode())

            # --- DETAILS for specific flight ---
            elif request.upper().startswith("DETAILS:"):
                code = request.split(":")[1].strip().upper()
                found = False
                for flight in flights:
                    if flight["flight"]["iata"] == code:
                        result = ""
                        result += "Flight: " + str(flight["flight"]["iata"]) + "\n"
                        result += "From: " + str(flight["departure"]["airport"]) + "\n"
                        result += "Gate: " + str(flight["departure"]["gate"]) + "\n"
                        result += "Terminal: " + str(flight["departure"]["terminal"]) + "\n"
                        result += "To: " + str(flight["arrival"]["airport"]) + "\n"
                        result += "Arrival Gate: " + str(flight["arrival"]["gate"]) + "\n"
                        result += "Arrival Terminal: " + str(flight["arrival"]["terminal"]) + "\n"
                        result += "Status: " + str(flight["flight_status"]) + "\n"
                        result += "Scheduled Departure: " + str(flight["departure"]["scheduled"]) + "\n"
                        result += "Scheduled Arrival: " + str(flight["arrival"]["scheduled"]) + "\n"
                        client_socket.send(result.encode())
                        found = True
                        break
                if not found:
                    client_socket.send("Flight not found.".encode())

            else:
                client_socket.send("Invalid request.".encode())

        except:
            break

    client_socket.close()

# Accept Incoming Clients. 
while True:
    client_socket, address = server_socket.accept()
    thread = threading.Thread(target=handle_client, args=(client_socket, address))
    thread.start()
