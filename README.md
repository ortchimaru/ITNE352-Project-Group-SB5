# ITNE352-Project-Group-SB5

## Project Title
Multithreaded Flight arrival Client/Server Information System

## Project Description
This project is a client-server based system developed using Python's socket and threading libraries. It retrieves real-time flight information via the AviationStack API and allows users to query flight statuses such as arrived flights, delayed flights, and specific flight details. The server handles multiple clients concurrently and processes various types of requests. The client interacts with a simple menu-driven interface.

## Semester
2024-2025, 2nd Semester

## Group

Group Name: SB5

Course Code: ITNE352

Section: 2

Students:

Khalid Abdulaziz Alhedaithy (ID: 202201331)

Abdullah Mohammad Jalal (ID: 202100452)

## Table of Contents

Project Title

Project Description

Semester

Group Information

Requirements

How to Run

The Scripts

Additional Concepts

Acknowledgments

Conclusion

## Requirements
To run this project locally, we used:

1. Python
Download and install Python from https://www.python.org

Ensure Python is added to your PATH (so it can be used and known from visual studio code)



2. pip install requests. to handle requests from client.py
type pip install requests in the terminal to install it

Files Required:

server.py

client.py

SB5.json (This is auto-created if not found on server start)

3. AviationStack API
Sign up at aviationstack.com for an API key
Replace the API key in server.py


## How to Run

Start the Server:

python server.py

If SB5.json is missing, the server will ask for an ICAO airport code to fetch flight data.

Start the Client:
In a separate terminal:

python client.py

Enter your name

Use the menu to interact with the server:

View arrived flights

View delayed flights

View specific flight details

Quit

## The Scripts

server.py:

Main Features: Handles client requests, fetches and loads flight data, supports multithreading. We added Object Oriented Programming as an additional concept

Key Libraries Used: socket, threading, requests, json, os.

Main Classes and Functions:

FlightServer: Initializes socket server, handles client threads.

fetch_data(): Fetches flight data from AviationStack.

process_request(): Parses commands like ARRIVED, DELAYED, DETAILS.

client.py:

Main Features: Sends user input to server, displays server responses. We added Object Oriented Programming as an additional concept

Key Libraries Used: socket

Main Classes and Functions:

FlightClient: Manages socket connection and user interaction.

connect_to_server(): Connects and sends client name.

show_menu(): Displays menu and processes user choices.

Sample Code Snippet:

# Example from server.py
if req == "ARRIVED":
result = ""
    for f in self.flights:
        if f.get("flight_status") == "landed":
            result += "Flight: " + str(f["flight"]["iata"]) + "\n"

I. Additional Concept: OOP (Object-Oriented Programming)
This project implements OOP principles through the use of custom classes:

FlightServer: Encapsulates server functionality, socket setup, and threading.

FlightClient: Encapsulates client operations including connection and UI.

Advantages:

Code reuse and modularity

Clear separation of concerns

Easier to maintain and extend

J. Acknowledgments

AviationStack for providing a free API to retrieve live flight data.

Python Software.

Visual Studio Code for development.

Github for management of the progress.

K. Conclusion
This project demonstrates practical usage of socket programming and API integration in Python. It offers real-time interaction between multiple clients and a server, showcasing how network communication, data fetching, and user interaction can be handled efficiently. The use of object-oriented programming improved the structure and readability of the code, making it an effective learning experience for us in network-based application development.
