import socket

Server settings
host = "127.0.0.1"
port = 5050

Create socket and connect to server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((host, port))

Send username
name = input("Enter your name: ")
client_socket.send(name.encode())

Main loop
while True:
    print("\n--- Menu ---")
    print("1. Arrived Flights")
    print("2. Delayed Flights")
    print("3. Specific Flight Details")
    print("4. Quit")

    choice = input("Enter your choice (1-4): ")

    if choice == "1":
        client_socket.send("ARRIVED".encode())
    elif choice == "2":
        client_socket.send("DELAYED".encode())
    elif choice == "3":
        code = input("Enter flight IATA code (e.g. GF501): ").strip().upper()
        client_socket.send(("DETAILS:" + code).encode())
    elif choice == "4":
        client_socket.send("QUIT".encode())
        break
    else:
        print("Invalid choice. Try again.")
        continue

    # Receive and display server response
    response = client_socket.recv(10000).decode()
    print("\n--- Server Response ---")
    print(response)

Close connection
client_socket.close()
print("Disconnected.")
