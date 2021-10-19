import socket

from EcbMode import EcbMode
from OfbMode import OfbMode
from commons import AES_decrypt_key, init_vector

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65433  # Port to listen on (non-privileged ports are > 1023)


def get_encrypted_file_content(conn):
    file_size = conn.recv(4)
    encrypted_file = conn.recv(int(str(file_size, 'utf-8')))
    return encrypted_file


def decryption(encrypted_file, mode_of_operation, decrypted_key):
    if mode_of_operation == b'ECB':
        ecb = EcbMode(decrypted_key)
        plaintext = ecb.decryption(encrypted_file)
    elif mode_of_operation == b'OFB':
        ofb = OfbMode(init_vector, decrypted_key)
        plaintext = ofb.decryption(encrypted_file)
    return plaintext


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    conn, addr = s.accept()
    with conn:
        mode_of_operation = conn.recv(1024)
        conn.sendall(b'Received')
        key = conn.recv(16)

        decrypted_key = AES_decrypt_key(key)  # decripteaza cheia primita de la nodul A
        conn.sendall(b'we can start the comunication')

        encrypted_file = get_encrypted_file_content(conn)
        decrypted_file = decryption(encrypted_file, mode_of_operation, decrypted_key)

        print("Mode of operation: ", mode_of_operation.decode("utf-8"), '\n')
        print(decrypted_file.decode("utf-8"))
