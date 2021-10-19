# se genereaza ciphertextul pentru un singur bloc de text cu xor pe vectorul de initailizare si cheie, apoi pe bloc
# def xor_ofb(block, iv, key):
#     iv_xor_key = bytes(a ^ b for (a, b) in zip(iv, key))
#     ciphertext = bytes(a ^ b for (a, b) in zip(block, iv_xor_key))
#     return ciphertext
from Crypto.Cipher import AES


def ofb_enc_dec(iv, key):
    aes = AES.new(key,AES.MODE_ECB)
    ofb_block = aes.encrypt(iv)
    return ofb_block


class OfbMode:
    def __init__(self, init_vector, key):
        self.init_vector = init_vector
        self.key = key

    def encryption(self, plaintext):
        ciphertext = b''
        padding = 16 - len(plaintext) % 16
        plaintext = plaintext + bytes([padding] * padding) #adauga padding daca este cazul

        # vor fi luati primii 16 biti din plaintext pentru a genera ciphertextul pentru acel bloc si se vor sterge
        # acestia pentru a continua criptarea restului de text si tot odata se va actualiza vectorul de initializare
        while plaintext:
            block = plaintext[0:16]
            plaintext = plaintext[16:]

            ofb_block = ofb_enc_dec(self.init_vector, self.key)
            self.init_vector = ofb_block                        # actualizam vectorul de initializare
            encrypt_result = bytes(a ^ b for (a, b) in zip(block, ofb_block))

            ciphertext += encrypt_result
        return ciphertext

    def decryption(self, ciphertext):
        if len(ciphertext) % 16 != 0:
            print('incorrect ciphertext')
            return
        plaintext = b''
        # asemenea criptarii se va genera plaintextul din ciphertext pentru decriptare luand blocuri de cate 16 biti
        while ciphertext:
            block = ciphertext[0:16]
            ciphertext = ciphertext[16:]

            ofb_block = ofb_enc_dec(self.init_vector, self.key)
            self.init_vector = ofb_block  # actualizam vectorul de initializare
            decrypt_result = bytes(a ^ b for (a, b) in zip(ofb_block, block))

            plaintext += decrypt_result
        # cauta padding in cazul in care exista
        count = 0
        current_pad = 0
        for c in plaintext[-16:]:
            if c != current_pad:
                current_pad = c
                count = 1
            else:
                count += 1
        if count != current_pad:
            print('Incorrect padding')
            return
        return plaintext[:-count]