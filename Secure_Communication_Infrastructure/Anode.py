import socket

from EcbMode import EcbMode
from OfbMode import OfbMode
from commons import AES_decrypt_key, init_vector

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT_KM = 65432  # The port used by the node KM
PORT_B = 65433  # The port used by the node B
decrypted_key = b''


def get_text_from_file(f):
    try:
        text_file = f.read()
        return text_file
    except PermissionError:
        print("No permission to read from the file")


def send_file_size(sock, text_file):
    file_size = len(text_file)*2
    sock.sendall(bytes(str(file_size), 'utf-8'))


def encryption(text_file):
    if mode_of_operation == 1:
        ecb = EcbMode(decrypted_key)
        ciphertext = ecb.encryption(text_file)
    else:
        ofb = OfbMode(init_vector, decrypted_key)
        ciphertext = ofb.encryption(text_file)
    return ciphertext


if __name__ == '__main__':
    key = ''
    global mode_of_operation
    while True:
        mode_of_operation = int(input("Choose one of the operation modes to communicate with the other node B:\n\t("
                                      "1)ECB\n\t(2)OFB\nPlease enter the digit: "))
        if 3 > mode_of_operation > 0:
            break
        else:
            print("Wrong input. Please try again!")

    # communication with KM node
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_KM))
        s.sendall(bytes(mode_of_operation))
        key = s.recv(1024)
        print('Received encrypted key K=', repr(key))
        s.close()

    # communication with B node
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_B))

        if mode_of_operation == 1:
            s.sendall(b'ECB')
        else:
            s.sendall(b'OFB')

        response = s.recv(1024)
        if response == b'Received':
            s.sendall(key)
        else:
            print("Something went wrong")

        decrypted_key = AES_decrypt_key(key)  # decripteaza cheia primita de la nodul KM

        response = s.recv(1024)
        if response == b'we can start the comunication':
            try:

                with open("file.txt", "rb") as f:
                    text_file = get_text_from_file(f)
                    send_file_size(s, text_file)  # trimite dimentiunea textului catre nodul B
                    ciphertext = encryption(text_file)  # cripteaza fisierul
                    s.sendall(ciphertext)

            except FileNotFoundError:
                print("Did not find the requested file")
