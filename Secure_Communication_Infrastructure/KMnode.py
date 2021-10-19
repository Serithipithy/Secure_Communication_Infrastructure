import socket

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from commons import KPrime

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


def AES_encrypt_key(key):
    aes = AES.new(KPrime, AES.MODE_ECB)
    encrypted_key = aes.encrypt(key)
    return encrypted_key


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    key = get_random_bytes(16)

    conn, addr = s.accept()
    with conn:
        mode_of_operation = conn.recv(1024)
        key_to_send = AES_encrypt_key(key)

        print('Node A requested the random key K =', key_to_send)
        conn.send(key_to_send)
        conn.close()
