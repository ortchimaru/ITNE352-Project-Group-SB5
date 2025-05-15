import socket

class FlightClient:
    def __init__(self, host="127.0.0.1", port=5050):
        # Set up connection settings
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        # Connect to the server and send client name
        self.client_socket.connect((self.host, self.port))
        name = input("Enter your name: ")
        self.client_socket.send(name.encode())

    def send_request(self, request):
        # Send a request to the server and receive the response
        self.client_socket.send(request.encode())
        response = self.client_socket.recv(10000).decode()
        print("\n--- Server Response ---")
        print(response)

    def show_menu(self):
        # Display the menu and handle user choices
        while True:
            print("\n--- Menu ---")
            print("1. Arrived Flights")
            print("2. Delayed Flights")
            print("3. Specific Flight Details")
            print("4. Quit")

            choice = input("Enter your choice (1-4): ")

            if choice == "1":
                self.send_request("ARRIVED")
            elif choice == "2":
                self.send_request("DELAYED")
            elif choice == "3":
                code = input("Enter flight IATA code (e.g. GF501): ").strip().upper()
                self.send_request("DETAILS:" + code)
            elif choice == "4":
                self.send_request("QUIT")
                break
            else:
                print("Invalid choice. Try again.")

        self.client_socket.close()
        print("Disconnected.")

# ======== Main program =========
if __name__ == "_main_":
    client = FlightClient()
    client.connect_to_server()
    client.show_menu()
