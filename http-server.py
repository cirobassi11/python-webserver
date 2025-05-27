# Ciro Bassi 0001113916 - Traccia 1

import socket
import mimetypes
import logging

HOST = 'localhost'
PORT = 8080
WWW_DIRECTORY = './www'

def run_server(): # Avvia il server, ascoltando sulla porta 8080
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s') # Configura il logging

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            connection, addr = server_socket.accept()
            with connection:
                print(f"Connected with {addr}")
                handle_request(connection)

def handle_request(connection): # Gestisce una singola richiesta da parte di un client
    request = connection.recv(1024).decode()

    if not request:
        return
    
    splitted_request = request.split()
    if len(splitted_request) > 0:
        method = splitted_request[0]
        path = splitted_request[1]

        logging.info(f"{method} {path}") # Log della richiesta

        if method == 'GET':
            if path == '/':
                path = '/index.html'
            
            filename = WWW_DIRECTORY + path

            try:
                with open(filename, 'rb') as file: # Apertura del file
                    response_body = file.read()
                response_header = 'HTTP/1.1 200 OK\r\n'
                
                content_type, _ = mimetypes.guess_type(filename) # Ottiene il tipo di contenuto del file
                if content_type is None:
                    content_type = 'application/octet-stream'

            except FileNotFoundError: # File non trovato
                response_body = b'File non trovato'
                response_header = 'HTTP/1.1 404 Not Found\r\n'
                content_type = 'text/plain'

            response_header += 'Content-Length: {}\r\n'.format(len(response_body))
            response_header += f'Content-Type: {content_type}\r\n'
            response_header += '\r\n'

            connection.sendall(response_header.encode() + response_body) # Invia l'header e il corpo della risposta

run_server() # Avvia il server