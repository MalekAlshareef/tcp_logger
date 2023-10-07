import socket
import time

# Define host and port for the server
HOST = '0.0.0.0'  # Listen on all available network interfaces
PORT = 12345      # Choose a port for the logger

# Define log file name and open it for appending
log_file_name = 'log.txt'
with open(log_file_name, 'a') as log_file:
    log_file.write("\n\n-- Log started at " + time.ctime() + " --\n")

# Define log level colors
LOG_COLORS = {
    'INFO': '\033[92m',    # Green
    'WARNING': '\033[93m', # Yellow
    'ERROR': '\033[91m'    # Red
}

# Reset console color
RESET_COLOR = '\033[0m'

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))
    print(f"Listening on {HOST}:{PORT}")

    # Listen for incoming connections
    server_socket.listen()

    # Accept connections and log messages
    while True:
        conn, addr = server_socket.accept()
        with conn:
            print(f"Connected by {addr}")
            data = conn.recv(1024)
            if not data:
                break

            # Get the current timestamp
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Decode the received message
            message = data.decode().strip()

            # Split the message into log level and content
            parts = message.split(':', 1)
            if len(parts) == 2:
                log_level, log_content = parts
            else:
                log_level, log_content = 'INFO', message

            # Log the message to the console with color
            log_message = f"[{timestamp}] {LOG_COLORS.get(log_level, '')}{log_level}:{RESET_COLOR} {log_content}"
            print(log_message)

            # Log the message to a file
            with open(log_file_name, 'a') as log_file:
                log_file.write(log_message + '\n')
